 
import os
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy import Column
from sqlalchemy import Table
import sqlalchemy as db
import config
from dotenv import load_dotenv
from sqlalchemy import select
from sqlalchemy import delete
from datetime import timedelta
import pytz
from sqlalchemy import desc

load_dotenv()

# TODO: использовать .env вместо config
# engine = create_engine(f'postgresql+psycopg2://{os.getenv("DB_USER")}:{os.getenv("DB_PASSWORD")}@{os.getenv("DB_HOSTNAME")}/{os.getenv("DB_NAME")}')

# engine = create_engine(f'postgresql+psycopg2://laoneuser:laonepassword@localhost:5432/laonedb')
engine = create_engine(f'postgresql+psycopg2://laoneuser:laonepassword@postgres:5432/laonedb') # Docker

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
    Column("vend_code", db.Integer)
    # TODO: связанный ключ chat_id и vend_code
)

metadata_obj.create_all(engine)

# TODO: asyncio
def insert_data(insert_data: dict, table_name: Table | None = product_requests) -> None:
    with engine.connect() as connection:
        connection.execute(table_name.insert(), insert_data)
        connection.commit()

# TODO: asyncio
def select_data(table_name: Table, *args) -> list:
    with engine.connect() as connection:
        stmt = select(table_name.c[*args])
        result = list(connection.execute(stmt))
    return result

# TODO: asyncio
def delete_subscribe(chat_id: int) -> None:
    with engine.connect() as connection:
        stmt = delete(subscribe_products).where(subscribe_products.c.chat_id == chat_id)
        connection.execute(stmt)
        connection.commit()

def main() -> None:
    with engine.connect() as connection:
        stmt = select(product_requests).where(product_requests.c.user_id==640814744)\
            .order_by(desc(product_requests.c.request_data))\
            .limit(5)
        last_fivet_minutes_rows = list(connection.execute(stmt))
    print(last_fivet_minutes_rows)


if __name__ == "__main__":
    main()