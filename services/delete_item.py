"""
How to use:
    delete_item("Entities", "vendor", "1")
"""

from connect_database import db_connection
from src import SPOT

def delete_item(container_name: str, type: str, id: str) -> int:
    """
    :purpose: This function deletes a record from a Cosmos DB container
    :params: container_name: name of the container
    :params: the item id to delete (user_id, vendor_id, product_id, etc.)
    :params: partition_key_value: the value of the partition key
    :return: 0 on success -1 on failure
    :author(s): Tim Liu, Joe Lee
    """
    if SPOT.OFFLINE:
        print("OFFLINE - Invalid Action - Requires network access")
        return 0

    try:
        print("deleting a record")
        container = db_connection.connect(container_name)

        arg = f"{type}_{id}"

        container.delete_item(arg, arg)
        return 0
    except Exception as e:
        print("ERROR: failed to delete " + str(e))
        return -1