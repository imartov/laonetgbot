'''
This module contains event handlers for the user's private messages
'''

import os

from aiogram import Router, types, F, Bot
from aiogram.filters import CommandStart, Command, or_f
from aiogram.types import Message
from sqlalchemy import select
from sqlalchemy import desc
from sqlalchemy.exc import IntegrityError
from dotenv import find_dotenv, load_dotenv

from kbrds.inline import inline_kb
from kbrds.reply import main_kb
from service import check_vend_code, get_info_from_message
import db
from sendmes.productinfo import send_subscribe_info

load_dotenv(find_dotenv())
bot = Bot(os.getenv("TG_TOKEN"))
user_router = Router()

@user_router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """ This handler receives messages with `/start` command """
    with open('messages//start.txt', "r", encoding="utf-8") as file:
        text = file.read()
    await message.answer(text=text.format(user_name=message.from_user.full_name),
                         reply_markup=main_kb)


@user_router.message(or_f(Command("menu"), (F.text.lower() == "меню")))
async def menu_cmd(message: Message):
    ''' This handler receives messages with `/menu` command '''
    with open('messages//show_menu.txt', "r", encoding="utf-8") as file:
        text = file.read()
    await message.answer(text=text, reply_markup=main_kb, )


@user_router.message(F.text.lower() == "получить информацию по товару")
async def get_product_info_reply(message: Message) -> None:
    ''' This handler receives messages with `/получить информацию по товару` command '''
    with open('messages//get_goods_info.txt', "r", encoding="utf-8") as file:
        text = file.read()
    await message.answer(text=text, reply_markup=types.ReplyKeyboardRemove())


@user_router.message(F.text.isdigit())
async def get_vend_code(message: Message) -> None:
    ''' This handler receives messages with vendor code command '''
    if message.text.isdigit():
        vend_code = ''.join(x for x in message.text if x.isdigit())
        info = check_vend_code(vend_code=vend_code)
        
        if not info:
            with open('messages//error_vend_code.txt', "r", encoding="utf-8") as file:
                text = file.read()
            await message.answer(text=text)
            return

        with open('messages//give_product_info.txt', "r", encoding="utf-8") as file:
            text = file.read().format(**info)
        await message.answer(text=text, reply_markup=inline_kb)
        insert_data = {
            "request_data": message.date,
            "user_id": message.from_user.id,
            "vend_code": vend_code
        }
        await db.insert_data(insert_data=insert_data, table_name=db.product_requests)


@user_router.message(F.text.lower() == "остановить уведомления")
async def stop_notify_subscribe(message: Message) -> None:
    ''' This handler receives messages with '/остановить уведомления' command '''
    with open('messages//cancel_subscribe.txt', "r", encoding="utf-8") as file:
        text = file.read()
    await message.answer(text=text, reply_markup=main_kb)
    await db.delete_subscribe(chat_id=message.from_user.id)


@user_router.message(F.text.lower() == "получить информацию из бд")
async def get_info_from_db(message: Message) -> None:
    ''' This handler receives messages with '/получить информацию из бд' command '''
    with open('messages//last_five_rows.txt', "r", encoding="utf-8") as file:
        text = file.read()
    await message.answer(text=text, reply_markup=main_kb)
    with db.engine.connect() as connection:
        stmt = select(db.product_requests)\
            .where(db.product_requests.c.user_id==message.from_user.id)\
            .order_by(desc(db.product_requests.c.request_data))\
            .limit(5)
        last_five_minutes_rows = list(connection.execute(stmt))
    if last_five_minutes_rows[0]:
        for row in last_five_minutes_rows:
            await send_subscribe_info(chat_id=message.from_user.id, vend_code=row[3])


@user_router.callback_query(F.data == "subscribe")
async def process_button(callback: types.CallbackQuery):
    ''' This handler receives messages with '/subscribe' command '''
    product_info = get_info_from_message(message=callback.message.text,
                                         key_words=["Артикул", "Название"])
    try:
        insert_data = {
            "chat_id": int(callback.from_user.id),
            "vend_code": product_info["Артикул"]
        }
        await db.insert_data(insert_data=insert_data, table_name=db.subscribe_products)
        with open('messages//subscribe.txt', "r", encoding="utf-8") as file:
            text = file.read().format(product_name=product_info["Название"],
                                      vend_doce=product_info["Артикул"])
    except IntegrityError:
        with open('messages//subscribe_exist.txt', "r", encoding="utf-8") as file:
            text = file.read().format(product_name=product_info["Название"],
                                      vend_doce=product_info["Артикул"])
    finally:
        await bot.send_message(chat_id=callback.from_user.id, text=text)


@user_router.message()
async def error_command(message: Message) -> None:
    ''' This handler receives messages with any command '''
    with open('messages//error_command.txt', "r", encoding="utf-8") as file:
        text = file.read()
    await message.answer(text=text, reply_markup=main_kb)
    