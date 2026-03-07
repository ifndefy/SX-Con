from typing import Any
from azure.cosmos.exceptions import CosmosResourceNotFoundError

from services.connect_database import db_connection
from src import SPOT
import utils.logger.logger as log

def get_item(container_name: str, entity_type: str, id: str, silent: bool = False) -> Any | None:
    """
    :purpose: Gets an entire document by ID and entity type
    :param: container_name: the Cosmos DB container to query
    :param: id_value: the numeric ID value to find
    :param: entity_type: "user", "vendor", or "product" (required)
    :return: entire document as dictionary, or "-1" if not found
    :author(s): Alexander Bubienko, Joe Lee
    """
    if SPOT.OFFLINE:
        log.warning("OFFLINE - Invalid Action - Requires network access")
        return 0

    try:
        container = db_connection.connect(container_name)

        item_id = f"{entity_type}_{id}"
        partition_key = item_id

        try:
            document = container.read_item(item=item_id, partition_key=partition_key)
            if not silent:
                log.info(f"Cosmos DB Container {container_name} found ID: {item_id} ID: {partition_key}")
            return document
        except CosmosResourceNotFoundError:
            if not silent:
                log.info(f"Cosmos DB container {container_name} not found ID: {item_id} ID: {partition_key}")
            return None
        except Exception as e:
            log.error(f"Error reading document: {e}")
            return None
    except Exception as e:
        log.error(f"Error in get_item: {e}")
        return None