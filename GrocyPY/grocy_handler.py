"""This class is used in order to communicate with grocy and to add missing entities and stock up fridge
"""

from . import config_handler as config
from . import utils

import requests
import json

headers = {
    'GROCY-API-KEY': "",
    'cache-control': "no-cache",
    'Postman-Token': "dd86ba36-1baf-487d-b8f7-8d3d2a794c34"
    }
    
url = config.get_value("grocy_api_url")

def handle_item_updates(mapping):
    # Going to iterate through all our new items and see if they exist
    # Mapping is a barcode: item
    with requests.Session() as s:
        objectUrl = url + "/objects/products"
        response = s.request("GET", objectUrl, headers=headers)
        products = json.loads(response.text)
        for product in products:
            for barcode in product["barcode"].split(","):
                mapping.pop(barcode, None)
        # Now only stuff left in mapping is what we need to add
        for key in mapping:
            data = mapping[key]
            payload = {
                "name": data["detail"]["description"],
                "description": data["detail"]["description"],
                "qu_id_purchase": 1,
                "qu_id_stock": 1,
                "qu_factor_purchase_to_stock": 1,
                "barcode": data["itemIdentifier"],
                "allow_partial_units_in_stock": "false"
            }
            
            response = s.request("POST", objectUrl, data=payload, headers=headers)
            utils.log(("Code for posting to api item update %d" % response.status_code))
            
def handle_item_purchases(mapping):
    with requests.Session() as s:
        for key in mapping:
            data = mapping[key]
            productUrl = "%s/stock/products/by-barcode/%s" % (url, key)
            response = s.request("GET", productUrl, headers=headers)
            id = json.loads(response.text)['product']['id']
            utils.log(("handle item purchases product id is %s" % id))
            # now we can update the amount
            stockUrl = productUrl = "%s/stock/products/%s/add" % (url, id)
            payload = {
                "amount": data["quantity"],
                "transaction_type": "purchase",
                "best_before_date": "2999-12-31",
                "price": data["pricePaid"]
            }
            response = s.request("POST", stockUrl, headers=headers, data=payload)
            utils.log(("handle item purchases success %d" % response.status_code))
            
    
headers["GROCY-API-KEY"] = config.get_value("grocy_api_key")