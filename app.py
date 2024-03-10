import os
import asyncio
import sys
import logging
from aiogram import Bot, Dispatcher, Router, types, F
from aiogram.types import BotCommandScopeAllPrivateChats
from aiogram.types import BotCommand
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold
from dotenv import find_dotenv, load_dotenv
import config
from keyboards import main_kb, inline_kb
from productsinfo import get_product_info
import db
from datetime import timedelta
from sqlalchemy import select
from sqlalchemy import desc


load_dotenv(find_dotenv())
bot = Bot(os.getenv("TG_TOKEN"), parse_mode=ParseMode.HTML)
dp = Dispatcher()
router = Router()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    with open('messages//start.txt', "r", encoding="utf-8") as file:
        text = file.read()
    await message.answer(text=text.format(user_name=message.from_user.full_name), reply_markup=main_kb)


@dp.message()
async def echo(message: Message, bot: Bot) -> None:
    msg = message.text.lower()

    if msg == "получить информацию по товару":
        with open('messages//get_goods_info.txt', "r", encoding="utf-8") as file:
            text = file.read()
        await message.answer(text=text)

    elif msg.isdigit():
        vend_code = ''.join(x for x in msg if x.isdigit())
        # TODO: asyncio
        info = get_product_info(vend_code=vend_code)
        with open('messages//give_product_info.txt', "r", encoding="utf-8") as file:
            text = file.read().format(**info)
        await message.answer(text=text, reply_markup=inline_kb)
        # TODO: pass to utils method
        insert_data = {
            "request_data": message.date,
            "user_id": message.from_user.id,
            "vend_code": vend_code
        }
        db.insert_data(insert_data=insert_data, table_name=db.product_requests)

    elif msg == "остановить уведомления":
        with open('messages//cancel_subscribe.txt', "r", encoding="utf-8") as file:
            text = file.read()
        await message.answer(text=text)
        db.delete_subscribe(chat_id=message.from_user.id)

    elif msg == "получить информацию из бд":
        with open('messages//last_five_rows.txt', "r", encoding="utf-8") as file:
            text = file.read()
        await message.answer(text=text)
        with db.engine.connect() as connection:
            stmt = select(db.product_requests).where(db.product_requests.c.user_id==message.from_user.id)\
                .order_by(desc(db.product_requests.c.request_data))\
                .limit(5)
            last_five_minutes_rows = list(connection.execute(stmt))
        if last_five_minutes_rows[0]:
            for row in last_five_minutes_rows:
                vend_code = row[3]
                chat_id = message.from_user.id
                await send_info(chat_id=chat_id, vend_code=vend_code)

async def send_info(chat_id:int, vend_code:int) -> None:
    info = get_product_info(vend_code=vend_code)
    with open('messages//give_product_info.txt', "r", encoding="utf-8") as file:
        text = file.read().format(**info)
    await bot.send_message(chat_id=chat_id, text=text, reply_markup=inline_kb)

async def service_send_info() -> None:
    with db.engine.connect() as connection:
        stmt = select(db.subscribe_products)
        all_subscribe_rows = list(connection.execute(stmt))
    for subscribe_row in all_subscribe_rows:
        chat_id = subscribe_row[1]
        vend_code = subscribe_row[2]
        print(chat_id, vend_code)
        await send_info(chat_id, vend_code)

@router.callback_query(F.data == "subscribe")
async def process_button(callback: types.CallbackQuery):
    # TODO: method for get vend_code from callback or another data
    # TODO: method for run celery
    with open('messages//subscribe.txt', "r", encoding="utf-8") as file:
        text = file.read()
    await bot.send_message(chat_id=callback.from_user.id, text=text)
    insert_data = {
        "chat_id": callback.from_user.id,
        "vend_code": 138791513
    }
    db.insert_data(insert_data=insert_data, table_name=db.subscribe_products)


async def main() -> None:
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    # await bot.set_my_commands(commands=private, scope=types.BotCommandScopeAllPrivateChats())
    await dp.start_polling(bot)


if __name__ == "__main__":
    # logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())

# TODO: ограничения телеграм по отправляемым смс сообщениям
