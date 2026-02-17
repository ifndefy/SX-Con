# ./test/test_delete.py

import uuid

from services.connect_database import db_connection
from services.delete_item import delete_item
from services.insert_item import insert_item


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
        container = db_connection.container_name
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