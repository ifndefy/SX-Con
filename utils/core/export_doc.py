import os
import utils.logger.logger as log
from utils.core.json_helpers import dict_to_json

def export_offline_record(ticket_number, vendor_doc, products_doc, consignment_doc):
    """
    :Purpose: Exports offline records to a local JSON file
    :param ticket_number: The offline ticket number (e.g. 'OFFLINE_1')
    :param vendor_doc: Vendor doc dict
    :param products_doc: Product doc list
    :param consignment_doc: Consignment doc dict
    :Author(s): Joe Lee
    """
    offline_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "OFFLINE_tickets")
    os.makedirs(offline_dir, exist_ok=True)

    docs = {
        'vendor': vendor_doc,
        'product': products_doc,
        'consignment': consignment_doc,
    }

    filepath = os.path.join(offline_dir, f"{ticket_number}.json")

    try:
        with open(filepath, 'w') as f:
            f.write(dict_to_json(docs))
        log.info(f"Offline record exported: {filepath}")
    except OSError as e:
        log.error(f"Failed to export offline record {ticket_number}: {e}")