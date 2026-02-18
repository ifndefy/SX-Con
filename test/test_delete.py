# ./test/test_delete.py

import uuid

from services.connect_database import db_connection
from services.delete_item import delete_item
from services.insert_item import insert_item
from services.delete_property import delete_property

def test_delete_item():
    """
    Module test for delete_item.py

    Spec:
      - insert an item into the database
      - delete the same item
      - return 0 on pass, -1 on fail
    Author(s): Colin Henderson
    """
    try:
        container = getattr(db_connection, "container_name")
        entity_type = "vendor"

        entity_id = str(uuid.uuid4())

        item_data = {
            f"{entity_type}_id": entity_id,
            "name": "test_delete_item",
        }

        insert_result = insert_item(container, entity_type, item_data)
        if insert_result != 0:
            return -1

        delete_result = delete_item(container, entity_type, entity_id)
        if delete_result != 0:
            return -1

        return 0

    except Exception:
        return -1

def test_delete_property():
    """
    Insert an item, then delete (set to null) a property of that same item.
    Verify the property is null. Return 0 on success, -1 on failure.
    Author(s): Colin Henderson
    """
    try:
        container = getattr(db_connection, "container_name")
        entity_type = "vendor"
        attribute_to_delete = "email"

        entity_id = str(uuid.uuid4())

        item_data = {
            f"{entity_type}_id": entity_id,
            "name": "test_delete_property",
            attribute_to_delete: "test@example.com",
        }

        insert_result = insert_item(container, entity_type, item_data)
        if insert_result != 0:
            return -1

        delete_prop_result = delete_property(container, entity_type, entity_id, attribute_to_delete)
        if delete_prop_result != 0:
            return -1

        item_id = f"{entity_type}_{entity_id}"
        partition_key = item_id
        try:
            container = db_connection.connect(container)
            item = container.read_item(item_id, partition_key)
        except Exception:
            return -1

        if attribute_to_delete not in item:
            return 0

        if item.get(attribute_to_delete) is None:
            return 0

        return -1

    except Exception:
        return -1