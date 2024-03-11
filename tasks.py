from celery import Celery
from aiogram import Bot, types
import asyncio
from app import bot
from productsinfo import get_product_info
import db
from sqlalchemy import select
from aiogram import exceptions


app = Celery('tasks', broker='pyamqp://guest@localhost//')
app.control.purge()
app.conf.update(
    result_expires=3600,
)
app.conf.timezone = 'UTC'

# def send_telegram_message_sync():
#     loop = asyncio.new_event_loop()
#     asyncio.set_event_loop(loop)
#     loop.run_until_complete(send_info())


async def send_info() -> None:
    try:
        with db.engine.connect() as connection:
            stmt = select(db.subscribe_products)
            all_subscribe_rows = list(connection.execute(stmt))
        for subscribe_row in all_subscribe_rows:
            chat_id = subscribe_row[1]
            vend_code = subscribe_row[2]
            info = get_product_info(vend_code=vend_code)
            with open('messages//give_product_info.txt', "r", encoding="utf-8") as file:
                text = file.read().format(**info)
            await bot.send_message(chat_id=chat_id, text=text)
    except Exception as ex:
        print(str(ex))


@app.task
def send_telegram_message():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(send_info())


app.conf.beat_schedule = {
    'send_telegram_message': {
        'task': 'tasks.send_telegram_message',
        'schedule': 30,  # every 10 seconds
    },
}

def main() -> None:
    pass

if __name__ == '__main__':
    pass
