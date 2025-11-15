from database_service import DatabaseService


def delete_record(container_name: str, id: str, partition_key_value: str) -> int:
    """
    :purpose: This function deletes a record from a Cosmos DB container
    :params: container_name: name of the container
    :params: the item id to delete (user_id, vendor_id, product_id, etc.)
    :params: partition_key_value: the value of the partition key
    :return: 0 on success -1 on failure
    :author(s): Tim Liu, Joe Lee
    """
    try:
        print("deleting a record")
        db_service = DatabaseService()
        container = db_service.connect(container_name)
        container.delete_item(container_name, item=id, partition_key=partition_key_value)
        return 0
    except Exception as e:
        print("ERROR: failed to delete " + str(e))
        return -1


def delete_record(container_name: str, id: str, partition_key_value: str) -> int:
    """
    :purpose: This function deletes a record from a Cosmos DB container
    :params: container_name: name of the container (consignments or entities)
    :params: id: the item id to delete
    :params: partition_key_value: the value of the partition key
    :method: reduce argument input by concatenating container_name with id and partition_key_value for true values
    :return: 0 on success -1 on failure
    """
    try:
        print("deleting a record")
        id_fixed = f"{container_name.lower()}_{id}"
        print(id_fixed)
        pkv_fixed = f"{container_name.lower()}_{partition_key_value}"
        print(pkv_fixed)
        db_service = DatabaseService()
        connection = db_service.connect(container_name=container_name)
        connection.container.delete_item(item=id_fixed, partition_key=pkv_fixed)
        return 0
    except Exception as e:
        print("ERROR: failed to delete " + str(e))
        return -1

# Run the test
delete_record("Consignments", "3", "3")