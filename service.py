import db
from sqlalchemy import select
from app import send_info
import asyncio


# async def service_send_info() -> None:
#     with db.engine.connect() as connection:
#         stmt = select(db.subscribe_products)
#         all_subscribe_rows = list(connection.execute(stmt))
#     for subscribe_row in all_subscribe_rows:
#         chat_id = subscribe_row[1]
#         vend_code = subscribe_row[2]
#         print(chat_id, vend_code)
#         await send_info(chat_id=chat_id, vend_code=vend_code)

def service_send_info() -> None:
    with db.engine.connect() as connection:
        stmt = select(db.subscribe_products)
        all_subscribe_rows = list(connection.execute(stmt))
    for subscribe_row in all_subscribe_rows:
        chat_id = subscribe_row[1]
        vend_code = subscribe_row[2]
        print(chat_id, vend_code)
        asyncio.run(send_info(chat_id=chat_id, vend_code=vend_code))


def main() -> None:
    # asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    # asyncio.get_event_loop().run_until_complete(service_send_info())
    service_send_info()

if __name__ == "__main__":
    main()