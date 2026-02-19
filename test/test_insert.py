from services.connect_database import db_connection
from services.update_property import update_property
from services.get_item import get_item
from services.delete_item import delete_item
from src import  SPOT
import utils.logger.logger as log


def test_update_property(container_name: str):
    """
    :purpose: test update property from services file
    :param: container_name: name of the container
    :author(s): Tim Liu
    """
    if SPOT.OFFLINE:
        print("OFFLINE -Invalid Action - Requires network access to test update_property")
        return 0

    try:
        container = db_connection.connect(container_name)

        document = {
            "id": "test",
            "partitionKey": "test_test",
            "entity_type": "test",
            "test_update": "no",
        }

        container.create_item(body=document)

        update_property(container_name, "test", "test_test", "test_update", "yes")

        grab_item = get_item(container_name, "test", "test")
        log.debug(f"item: {grab_item['test_update']}")
        if grab_item['test_update'] == "yes":
            log.debug(f"update_property test succeeded")
            return 0
        else:
            log.debug(f"update_property test failed")
            return -1
    except Exception as e:
        log.error(f"Error in test_update_property: {e}")
        return -1
    finally:
        delete_item(container_name, "test", "test")