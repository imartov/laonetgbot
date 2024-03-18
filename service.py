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

def check_vend_code(vend_code: int) -> any:
    try:
        info = get_product_info(vend_code=vend_code)
    except IndexError:
        info = False
    return info

# функция если артикул неверный, отсутсвтует в WB

def get_info_from_message(message: str, key_words: list) -> dict:
    result_dict = {}
    list_line = message.split("\n")
    for key_word in key_words:
        for line in list_line:
            if key_word in line:
                start_index = len(key_word) + 3
                find_value = line[start_index:]
                result_dict[key_word] = find_value.strip()
    print(result_dict)
    return result_dict


def main() -> None:
    # with open("test.txt", "r", encoding="utf-8") as file:
    #     message = file.read()
    # key_words = ["Артикул", "Название"]
    # get_info_from_message(message=message, key_words=key_words)

    info = get_product_info(vend_code=123)

if __name__ == "__main__":
    main()