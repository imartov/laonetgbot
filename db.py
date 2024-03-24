'''
This module contains connection configurations,
database object classes, and methods for interacting with it
'''

import os
from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy import Column
from sqlalchemy import Table
import sqlalchemy as db
from sqlalchemy import select
from sqlalchemy import delete
from sqlalchemy import UniqueConstraint
from dotenv import load_dotenv

load_dotenv()

url_db = f'postgresql+psycopg2://{os.getenv("DB_USER")}:{os.getenv("DB_PASSWORD")}@{os.getenv("DB_HOST")}:{os.getenv("DB_PORT")}/{os.getenv("DB_NAME")}'
engine = create_engine(url_db)

metadata_obj = MetaData()

product_requests = Table(
    "product_requests",
    metadata_obj,
    Column("id", db.Integer, primary_key=True, autoincrement=True),
    Column("user_id", db.Integer),
    Column("request_data", db.DateTime),
    Column("vend_code", db.Integer)
)

subscribe_products = Table(
    "subscribe_products",
    metadata_obj,
    Column("id", db.Integer, primary_key=True, autoincrement=True),
    Column("chat_id", db.Integer),
    Column("vend_code", db.Integer),
    UniqueConstraint("chat_id", "vend_code", name="uniq_product"),
)

metadata_obj.create_all(engine)


async def insert_data(data: dict,
                      table_name: Table | None = product_requests) -> None:
    ''' This method inserts data into the database '''
    with engine.connect() as connection:
        connection.execute(table_name.insert(), data)
        connection.commit()


async def select_data(table_name: Table, *args) -> list:
    ''' This method extracts data from the database '''
    with engine.connect() as connection:
        stmt = select(table_name.c[*args])
        result = list(connection.execute(stmt))
        # result = connection.execute(stmt)
    return result


async def delete_subscribe(chat_id: int) -> None:
    ''' This method removes data from the 'subscribe_products' table
        and describes the user from subscribed products '''
    with engine.connect() as connection:
        stmt = delete(subscribe_products).where(subscribe_products.c.chat_id == chat_id)
        connection.execute(stmt)
        connection.commit()


if __name__ == "__main__":
    pass
    