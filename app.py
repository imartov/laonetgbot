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


load_dotenv(find_dotenv())
dp = Dispatcher()

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    with open('messages//start.txt', "r", encoding="utf-8") as file:
        text = file.read()
    print(message.date)
    await message.answer(text=text.format(user_name=message.from_user.full_name), reply_markup=main_kb)


@dp.message()
async def echo(message: Message, bot: Bot) -> None:
    msg = message.text.lower()

    if msg == "получить информацию по товару":
        with open('messages//get_goods_info.txt', "r", encoding="utf-8") as file:
            text = file.read()
        await message.answer(text=text)

    if msg.isdigit():
        vend_code = ''.join(x for x in msg if x.isdigit())
        # TODO: asyncio
        info = get_product_info(vend_code=vend_code)
        with open('messages//give_product_info.txt', "r", encoding="utf-8") as file:
            text = file.read().format(**info)
        await message.answer(text=text, reply_markup=inline_kb)
        insert_data = {
            "request_data": message.date,
            "user_id": message.from_user.id,
            "vend_code": vend_code
        }

async def main() -> None:
    bot = Bot(os.getenv("TG_TOKEN"), parse_mode=ParseMode.HTML)
    await bot.delete_webhook(drop_pending_updates=True)
    # await bot.set_my_commands(commands=private, scope=types.BotCommandScopeAllPrivateChats())
    await dp.start_polling(bot)


if __name__ == "__main__":
    # logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
