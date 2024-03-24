'''
This module contains methods for sending messages with product information
'''

import os

from aiogram import Bot
from sqlalchemy import select
from dotenv import load_dotenv
from dotenv import find_dotenv

from service import check_vend_code
import db

load_dotenv(find_dotenv())

bot = Bot(token=os.getenv("TG_TOKEN"))

async def send_info(chat_id:int, vend_code:int) -> None:
    ''' This method receives information about the product and sends a message '''
    info = check_vend_code(vend_code=vend_code)
    with open('messages//give_product_info.txt', "r", encoding="utf-8") as file:
        text = file.read().format(**info)
    await bot.send_message(chat_id=chat_id, text=text)


async def send_subscribe_info(chat_id:int, vend_code:int) -> None:
    ''' This method requests information about the signed product
        and sends a message '''
    info = check_vend_code(vend_code=vend_code)
    with open('messages//periodic_subscribe.txt', "r", encoding="utf-8") as file:
        text = file.read().format(**info)
    await bot.send_message(chat_id=chat_id, text=text)


async def service_send_info() -> None:
    ''' This method extracts information about signed products
        and passes it to a function for sending a message '''
    with db.engine.connect() as connection:
        stmt = select(db.subscribe_products)
        all_subscribe_rows = list(connection.execute(stmt))
    for subscribe_row in all_subscribe_rows:
        chat_id = subscribe_row[1]
        vend_code = subscribe_row[2]
        await send_subscribe_info(chat_id, vend_code)
