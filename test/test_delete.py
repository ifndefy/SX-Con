# ./test/test_delete.py
print("test_delete.py imported")

import uuid
import logging

from services.connect_database import db_connection
from services.delete_item import delete_item
from services.insert_item import insert_item
from services.delete_property import delete_property
import utils.logger.logger as log
log.info("test_delete.py imported")
import os
print("CWD:", os.getcwd())

def _flush_base_logger():
    for h in logging.getLogger("base_logger").handlers:
        try:
            h.flush()
        except Exception:
            pass

def test_delete_item():
    """
    Module test for delete_item.py
    Spec:
    - insert an item into the database
    - delete the same item
    - return 0 on pass, -1 on fail
    Author(s): Colin Henderson
    """
    print("test_delete_item executed")
    try:
        log.info("Starting test_delete_item")
        _flush_base_logger()

        container_name = getattr(db_connection, "container_name", "Entities")
        entity_type = "vendor"
        entity_id = str(uuid.uuid4())

        item_data = {f"{entity_type}_id": entity_id, "name": "test_delete_item"}

        insert_rc = insert_item(container_name, entity_type, item_data)
        log.info(f"insert_item returned: {insert_rc!r}")
        _flush_base_logger()
        if insert_rc != 0:
            return -1

        delete_rc = delete_item(container_name, entity_type, entity_id)
        log.info(f"delete_item returned: {delete_rc!r}")
        _flush_base_logger()
        if delete_rc != 0:
            return -1

        return 0

    except Exception as e:
        log.error(f"test_delete_item exception: {e!r}")
        _flush_base_logger()
        return -1


def test_delete_property():
    """
    Module test for delete_property.py
    Spec:
    - Insert an item, then delete (set to null) a property of that same item.
    - Verify the property is null.
    - Return 0 on success, -1 on failure.
    Author(s): Colin Henderson
    """
    print("test_delete_property executed")
    try:
        container_name = getattr(db_connection, "container_name", "Entities")
        entity_type = "vendor"
        attribute_to_delete = "email"
        entity_id = str(uuid.uuid4())

        item_data = {
            f"{entity_type}_id": entity_id,
            "name": "test_delete_property",
            attribute_to_delete: "test@example.com",
        }

        insert_rc = insert_item(container_name, entity_type, item_data)
        log.info(f"insert_item returned: {insert_rc!r}")
        _flush_base_logger()
        if insert_rc != 0:
            return -1

        delprop_rc = delete_property(container_name, entity_type, entity_id, attribute_to_delete)
        log.info(f"delete_property returned: {delprop_rc!r}")
        _flush_base_logger()
        if delprop_rc != 0:
            return -1

        item_id = f"{entity_type}_{entity_id}"
        partition_key = item_id

        container_client = db_connection.connect(container_name)
        item = container_client.read_item(item_id, partition_key)

        # delete_property sets it to None
        return 0 if item.get(attribute_to_delete) is None else -1

    except Exception as e:
        log.error(f"test_delete_property exception: {e!r}")
        _flush_base_logger()
        return -1