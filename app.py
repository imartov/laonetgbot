'''
This module is the main module for launching and managing a telegram bot
'''

import os
import sys
import logging
import asyncio

from aiogram import Bot, Dispatcher, types

from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())

from handlers.private import user_router
from common.bot_cmds_list import private


bot = Bot(os.getenv("TG_TOKEN"))

dp = Dispatcher() # по умолчанию используется хранилище оперативной памяти для хранения состояний
dp.include_router(user_router)

async def main() -> None:
    ''' the method implements a sequence of commands to launch a telegram bot '''
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.delete_my_commands(scope=types.BotCommandScopeAllPrivateChats())
    await bot.set_my_commands(commands=private, scope=types.BotCommandScopeAllPrivateChats())
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
