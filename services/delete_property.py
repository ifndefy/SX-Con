from services.connect_database import db_connection
from src import SPOT
import utils.logger.logger as log

def delete_property(container_name: str, type: str, id: str, attribute_name: str) -> int:
    """
    :purpose: This function deletes a specific attribute from a record in Cosmos DB by setting it to null
    :params: container_name: name of the container
    :params: type: the item type (vendor, user, product, etc.)
    :params: id: the item id to modify
    :params: attribute_name: the name of the attribute to delete/set to null
    :return: 0 on success -1 on failure
    :author(s): Tim Liu, Joe Lee
    """
    if SPOT.OFFLINE:
        log.warning("OFFLINE - Invalid Action - Requires network access")
        return 0

    try:
        log.info(f"deleting attribute '{attribute_name}' from record {type}_{id} from {container_name}")
        container = db_connection.connect(container_name)

        item_id = f"{type}_{id}"
        partition_key = item_id

        item = container.read_item(item_id, partition_key)
        item[attribute_name] = None

        container.replace_item(item_id, item)
        log.info(f"Successfully deleted attribute '{attribute_name}' from record {type}_{id} in {container_name}")
        return 0
    except Exception as e:
        log.error(f"ERROR: failed to delete property {attribute_name} from {type}_{id} in {container_name}: {e}")
        return -1