import os

from aiogram import Bot
from sqlalchemy import select
from dotenv import load_dotenv
from dotenv import find_dotenv
load_dotenv(find_dotenv())

from service import get_product_info
import db


bot = Bot(token=os.getenv("TG_TOKEN"))

# TODO: make async
async def send_info(chat_id:int, vend_code:int) -> None:
    info = get_product_info(vend_code=vend_code)
    with open('messages//give_product_info.txt', "r", encoding="utf-8") as file:
        text = file.read().format(**info)
    await bot.send_message(chat_id=chat_id, text=text)

# TODO: make async
async def send_subscribe_info(chat_id:int, vend_code:int) -> None:
    info = get_product_info(vend_code=vend_code)
    with open('messages//periodic_subscribe.txt', "r", encoding="utf-8") as file:
        text = file.read().format(**info)
    await bot.send_message(chat_id=chat_id, text=text)


# TODO: make async
async def service_send_info() -> None:
    with db.engine.connect() as connection:
        stmt = select(db.subscribe_products)
        all_subscribe_rows = list(connection.execute(stmt))
    for subscribe_row in all_subscribe_rows:
        chat_id = subscribe_row[1]
        vend_code = subscribe_row[2]
        await send_subscribe_info(chat_id, vend_code)