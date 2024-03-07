import os
import asyncio
import sys
import logging
from aiogram import Bot, Dispatcher, Router, types
from aiogram.types import BotCommandScopeAllPrivateChats
from aiogram.types import BotCommand
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold
from dotenv import find_dotenv, load_dotenv
import config


load_dotenv(find_dotenv())
dp = Dispatcher()
ALLOWED_UPDATES = ['message', 'edited_message']

# private = [
#     BotCommand(command="Получить информацию по товару", description="Принимает артукул товара и возвращает его название, артикул, цену, рейтинг и количество товара на всех складах."),
#     BotCommand(command="Остановить уведомления", description="Остановить уведомления"),
#     BotCommand(command="Получить информацию из БД",description="Получить информацию о последних 5 запрошенных товарах")
# ]

private = [
    BotCommand(command="One", description="Принимает артукул товара и возвращает его название, артикул, цену, рейтинг и количество товара на всех складах."),
    BotCommand(command="Two", description="Остановить уведомления"),
    BotCommand(command="Three", description="Получить информацию о последних 5 запрошенных товарах")
]

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    await message.answer(f"Hello, {hbold(message.from_user.full_name)}!")

@dp.message()
async def echo(message: Message, bot: Bot) -> None:
    await bot.send_message(chat_id=message.from_user.id, text=message.text)
    await message.answer(text=message.text)
    await message.reply(text=message.text)


async def main() -> None:
    # bot = Bot(os.getenv("TG_TOKEN"), parse_mode=ParseMode.HTML)
    bot = Bot(os.getenv("TG_TOKEN"))
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_my_commands(commands=private, scope=types.BotCommandScopeAllPrivateChats())
    await dp.start_polling(bot, allowed_updates=ALLOWED_UPDATES)


if __name__ == "__main__":
    # logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
