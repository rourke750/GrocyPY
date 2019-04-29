import copy
import argparse
import csv
import logging
import time
from . import config_handler as config
from . import utils
from . import db_handler as db
from .scrapers import kroger_scraper as scraper
from . import grocy_handler as grocy


def barcode_mapping(data):
    mapping = {}
    for d in data:
        items = d["data"]["data"][0]["items"]
        for item in items:
            mapping[item["itemIdentifier"]] = item
    return mapping

# log to the directory of execution
logging.basicConfig(filename='grocypy.log', level=logging.DEBUG)
# No we want to run the scraper
data = scraper.get_valid_data()
mapping = barcode_mapping(data)
grocy.handle_item_updates(copy.deepcopy(mapping))
grocy.handle_item_purchases(mapping)
# Now we want to add the receipts to the db
for d in data:
    receipt = d["receipt"]
    db.generate_receipt(receipt["userId"], receipt["divisionNumber"], receipt["storeNumber"], receipt["transactionDate"], receipt["terminalNumber"], receipt["transactionId"])