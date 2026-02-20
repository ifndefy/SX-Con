from typing import Any

from services.connect_database import db_connection
from src import SPOT
import utils.logger.logger as log

def get_item_by_property(container_name: str, entity_type: str, property_name: str, property_value: Any) -> Any | None:
    """
    :purpose: gets an item by property
    :param container_name: name of the container
    :param entity_type: type of the entity
    :param property_name: name of the property
    :param property_value: value of the property
    :return: None
    :author(s): Joe Lee
    """
    if SPOT.OFFLINE:
        log.warning("OFFLINE - Invalid Action - Requires network access")
        return 0

    try:
        container = db_connection.connect(container_name)

        if isinstance(property_value, (int, float)):
            query = f"SELECT * FROM c WHERE c.type = '{entity_type}' AND c.{property_name} = {property_value}"
        else:
            query = f"SELECT * FROM c WHERE c.type = '{entity_type}' AND c.{property_name} = '{property_value}'"

        items = list(container.query_items(
            query=query,
            enable_cross_partition_query=True
        ))

        if items:
            log.info(f"Cosmos DB Container {container_name} found by {property_name}: {property_value}")
            return items[0]
        else:
            log.info(f"Cosmos DB container {container_name} not found by {property_name}: {property_value}")
            return None
    except Exception as e:
        log.error(f"Error in get_item_by_property: {e}")
        return None