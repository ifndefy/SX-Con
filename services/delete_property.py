"""
How to use:
    delete_property("Entities", "vendor", "1", "email")
"""

from connect_database import DatabaseConnection


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
    try:
        print(f"deleting attribute '{attribute_name}' from record")
        db_service = DatabaseConnection()
        container = db_service.connect(container_name)

        item_id = f"{type}_{id}"
        partition_key = item_id

        item = container.read_item(item_id, partition_key)
        item[attribute_name] = None

        container.replace_item(item_id, item)

        return 0
    except Exception as e:
        print("ERROR: failed to delete_property " + str(e))
        return -1