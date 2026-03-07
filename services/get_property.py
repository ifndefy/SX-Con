from services.connect_database import db_connection
from src import SPOT
import utils.logger.logger as log

def get_property(container_name: str, attribute: str, entity_type: str, id_value: str, silent: bool = False) -> str:
    """
    :purpose: Gets a specific attribute value from a document by ID
    :param: container_name: the Cosmos DB container to query
    :param: attribute: the property name to retrieve
    :param: id_value: the numeric ID value to find
    :param: entity_type: "user", "vendor", or "product" (required)
    :return: value of the attribute
    :use case: get_property("Entities", "username", "1", "user")
    :author(s): Alexander Bubienko, Joe Lee
    """
    if SPOT.OFFLINE:
        log.warning("OFFLINE - Invalid Action - Requires network access")
        return 0

    try:
        container = db_connection.connect(container_name)

        item_id = f"{entity_type}_{id_value}"
        partition_key = item_id

        try:
            document = container.read_item(item=item_id, partition_key=partition_key)
            return str(document.get(attribute, "-1"))
        except Exception as e:
            log.error(f"Error reading document: {e}")
            return "-1"

    except Exception as e:
        log.error(f"Error in get_property: {e}")
        return "-1"