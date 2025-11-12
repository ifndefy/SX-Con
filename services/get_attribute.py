from database_service import DatabaseService

def get_attribute_value(container_name: str, attribute: str, id_value: str, entity_type: str) -> str:
    """
    :purpose: Gets a specific attribute value from a document by ID
    :param: container_name: the Cosmos DB container to query
    :param: attribute: the property name to retrieve
    :param: id_value: the numeric ID value to find
    :param: entity_type: "user", "vendor", or "product" (required)
    :return: value of the attribute
    :use case: get_attribute_value("Entities", "username", "1", "user")
    :author(s): Alexander Bubienko, Joe Lee
    """
    try:
        db = DatabaseService()
        container = db.connect(container_name)

        item_id = f"{entity_type}_{id_value}"
        partition_key = item_id

        try:
            document = container.read_item(item=item_id, partition_key=partition_key)
            return str(document.get(attribute, "-1"))
        except Exception as e:
            print(f"Error reading document: {e}")
            return "-1"

    except Exception as e:
        print(f"Error in get_attribute_value: {e}")
        return "-1"