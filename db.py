 
import os
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy import Column
from sqlalchemy import Table
import sqlalchemy as db
import config
from dotenv import load_dotenv

load_dotenv()

# TODO: использовать .env вместо config
# engine = create_engine(f'postgresql+psycopg2://{os.getenv("DB_USER")}:{os.getenv("DB_PASSWORD")}@{os.getenv("DB_HOSTNAME")}/{os.getenv("DB_NAME")}')
engine = create_engine(f'postgresql+psycopg2://laonetgbot:12345-laone@localhost:5432/laonedb')
metadata_obj = MetaData()

product_requests = Table(
    "product_requests",
    metadata_obj,
    Column("id", db.Integer, primary_key=True, autoincrement=True),
    Column("user_id", db.Integer),
    Column("request_data", db.DateTime),
    Column("vend_code", db.Integer)
)

metadata_obj.create_all(engine)

# TODO: asyncio
def insert_data(table_name: Table, insert_data: dict) -> None:
    with engine.connect() as connection:
        connection.execute(table_name.insert(), insert_data)
        connection.commit()


def main() -> None:
    pass

if __name__ == "__main__":
    main()