import uuid

from services.connect_database import db_connection
from services.delete_item import delete_item
from services.insert_item import insert_item
from services.delete_property import delete_property
from services.get_item import get_item

def test_delete_item():
    """
    Module test for delete_item.py
    Spec:
    - insert an item into the database
    - delete the same item
    - return 0 on pass, -1 on fail
    Author(s): Colin Henderson
    """
    container_name = getattr(db_connection, "container_name", "Entities")
    entity_type = "vendor"
    entity_id = str(uuid.uuid4())

    item_data = {f"{entity_type}_id": entity_id, "name": "test_delete_item"}

    insert_rc = insert_item(container_name, entity_type, item_data)
    if insert_rc != 0:
        assert False, "Failed to insert item into database"

    delete_rc = delete_item(container_name, entity_type, entity_id)
    if delete_rc != 0:
        assert False, "Failed to delete item from database"

    item = get_item(container_name, entity_type, entity_id)
    if item is not None:
        assert False, "Item still exists in database"

def test_delete_property():
    """
    Module test for delete_property.py
    Spec:
    - Insert an item, then delete (set to null) a property of that same item.
    - Verify the property is null.
    - Return 0 on success, -1 on failure.
    Author(s): Colin Henderson, Joe Lee
    """
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
    if insert_rc != 0:
        assert False, "Failed to insert item into database"

    delprop_rc = delete_property(container_name, entity_type, entity_id, attribute_to_delete)
    if delprop_rc != 0:
        assert False, "Failed to delete property from database"

    item = get_item(container_name, entity_type, entity_id)
    if item.get(attribute_to_delete) is not None:
        assert False, "Item property still exists in database"

    del_rc = delete_item(container_name, entity_type, entity_id)
    if del_rc != 0:
        assert False, "Failed to delete item from database"