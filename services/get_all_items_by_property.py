from typing import Any
from src import SPOT
from services.connect_database import db_connection
import utils.logger.logger as log


def get_all_items_by_property(container_name: str, entity_type: str, property_name: str, property_value: Any) -> Any | None:
    """
    :purpose: gets all items by property
    :param container_name: name of the container
    :param entity_type: type of the entity
    :param property_name: name of the property
    :param property_value: value of the property
    :return: single item dict, list of dicts, or None
    :author(s): Joe Lee
    """
    if SPOT.OFFLINE:
        log.warning("OFFLINE - Invalid Action - Requires network access")
        return 0

    try:
        container = db_connection.connect(container_name)

        if isinstance(property_value, (int, float)):
            query = f"SELECT * FROM c WHERE c.entity_type = '{entity_type}' AND c.{property_name} = {property_value}"
        else:
            query = f"SELECT * FROM c WHERE c.entity_type = '{entity_type}' AND c.{property_name} = '{property_value}'"

        items = list(container.query_items(
            query=query,
            enable_cross_partition_query=True
        ))
        log.info(f"Query returned {len(items)} item(s) for {property_name}: {property_value}")

        if items:
            log.info(f"Found {len(items)} item(s) by {property_name}: {property_value}")
            return items[0] if len(items) == 1 else items
        else:
            log.info(f"Did not find any items using {property_name}: {property_value}")
            return None
    except Exception as e:
        log.error(f"Error: Failed to get item(s) by property: {property_value} : {e}")
        return None