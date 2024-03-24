'''
This module contains service methods
'''

from collections import OrderedDict
import requests
import config


def get_product_info(vend_code:int) -> OrderedDict:
    ''' This method requests information about the product '''
    url = config.URL_INFO.format(vend_code=vend_code)
    resp = requests.get(url=url, timeout=10).json()
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
    ''' This method checks if the entered article is available in the WB '''
    try:
        info = get_product_info(vend_code=vend_code)
    except (IndexError, requests.exceptions.Timeout):
        info = False
    return info


def get_info_from_message(message: str, key_words: list) -> dict:
    ''' This method extracts its properties from a typical product information message '''
    result_dict = {}
    list_line = message.split("\n")
    for key_word in key_words:
        for line in list_line:
            if key_word in line:
                start_index = len(key_word) + 3
                find_value = line[start_index:]
                result_dict[key_word] = find_value.strip()
    return result_dict


if __name__ == "__main__":
    pass
