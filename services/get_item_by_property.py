from typing import Any

from services.connect_database import db_connection
import utils.logger.logger as log

def get_item_by_property(container_name: str, entity_type: str, property_name: str, property_value: str) -> Any | None:
    """
    :purpose: gets an item by property
    :param container_name: name of the container
    :param entity_type: type of the entity
    :param property_name: name of the propertyW
    :param property_value: value of the property
    :return: None
    :author(s): Joe Lee
    """
    try:
        container = db_connection.connect(container_name)

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