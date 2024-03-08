import os
import json
import asyncio
import requests
from dotenv import load_dotenv
from collections import OrderedDict


load_dotenv()

# TODO: make asyncio
def get_product_info(vend_code:int) -> OrderedDict:
    url = os.getenv("URL_GOODS_INFO").format(vend_code=vend_code)
    resp = requests.get(url=url).json()
    currency = resp["params"]["curr"]
    if resp["data"]["products"][0]["salePriceU"]:
        price = str(round(resp["data"]["products"][0]["salePriceU"] / 100, 2)) + " " + currency
    else:
        price = resp["data"]["products"][0]["priceU"] / 100 + " " + currency
    info = OrderedDict()
    info = {
        "product_name": resp["data"]["products"][0]["name"],
        "vend_code": vend_code,
        "price": price,
        "rating": resp["data"]["products"][0]["reviewRating"],
        "products_count": resp["data"]["products"][0]["wh"]
    }
    return info

# функция если артикул неверный, отсутсвтует в WB

def main() -> None:
    print(get_product_info(ven_code=120772856))

if __name__ == "__main__":
    main()