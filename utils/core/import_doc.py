import os
from pathlib import Path

from services.insert_item import insert_item
from services.get_item_by_property import get_item_by_property
from services.get_max_value import get_max_value
from validate.val_check_does_not_exist import val_check_does_not_exists
from utils.core.json_helpers import json_to_dict
import utils.logger.logger as log

def import_offline_records():
    """
    purpose: imports offline records and inserts them into the database
    note: validation should not be done here, they should have been validated prior to exporting
    author(s): Joe Lee
    """
    offline_dir = Path(__file__).parent.parent / 'OFFLINE_tickets'
    if not offline_dir.exists():
        log.info("No OFFLINE_tickets directory found, skipping import")
        return

    for file in offline_dir.iterdir():
        if not file.is_file() or not file.suffix == '.json':
            continue

        with open(file, 'r') as f:
            docs = json_to_dict(f.read())

        if not docs:
            log.error(f"Failed to parse offline record {file.name}")
            continue

        vendor = docs.get('vendor')
        products = docs.get('product')
        consignment = docs.get('consignment')

        if not vendor or not products or not consignment:
            log.error(f"Invalid syntax in {file.name}, skipping")
            continue

        vendor['type'] = 'vendor'
        consignment['type'] = 'consignment'
        for product in products:
            product['type'] = 'product'
        success = True

        if val_check_does_not_exists("Entities", "vendor", "vendor_id", vendor['vendor_id']):
            if insert_item("Entities", "vendor", vendor) == -1:
                log.error(f"Failed to insert vendor {vendor['vendor_id']} from {file.name}")
                success = False
        else:
            log.info(f"Vendor {vendor['vendor_id']} already exists, skipping")

        for product in products:
            product['product_name'] = product['product_name'].lower()

            if not val_check_does_not_exists("Entities", "product", "product_id", product['product_id']):
                log.info(f"Product {product['product_id']} already exists, skipping")
                continue

            existing = get_item_by_property("Entities", "product", "product_name", product['product_name'])
            if existing:
                log.info(f"Product name '{product['product_name']}' exists under product_id {existing['product_id']}, remapping")
                product['product_id'] = existing['product_id']
                continue

            if insert_item("Entities", "product", product) == -1:
                log.error(f"Failed to insert product {product['product_id']} from {file.name}")
                success = False

        ticket_number = int(get_max_value("Consignments", "ticket_number")) + 1
        consignment['ticket_number'] = ticket_number
        consignment['consignment_id'] = ticket_number

        if insert_item("Consignments", "consignment", consignment) == -1:
            log.error(f"Failed to insert consignment {ticket_number} from {file.name}")
            success = False

        if success:
            os.remove(file)
            log.info(f"Offline record {file.name} imported as ticket {ticket_number} and deleted successfully")
        else:
            log.error(f"Offline record {file.name} had errors, not deleted")