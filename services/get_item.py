from typing import Union
from services.connect_database import db_connection

def get_record(container_name: str, entity_type: str, id: str) -> Union[dict, str]:
    """
    :purpose: Gets an entire document by ID and entity type
    :param: container_name: the Cosmos DB container to query
    :param: id_value: the numeric ID value to find
    :param: entity_type: "user", "vendor", or "product" (required)
    :return: entire document as dictionary, or "-1" if not found
    :author(s): Alexander Bubienko, Joe Lee
    """
    try:
        container = db_connection.connect(container_name)

        item_id = f"{entity_type}_{id}"
        partition_key = item_id

        try:
            document = container.read_item(item=item_id, partition_key=partition_key)
            return document
        except Exception as e:
            print(f"Error reading document: {e}")
            return "-1"

    except Exception as e:
        print(f"Error in get_item: {e}")
        return "-1"