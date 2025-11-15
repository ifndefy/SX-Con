from services.connect_database import db_connection


def insert_item(container_name: str, entity_type: str, item_data: dict):
    """
    :purpose: inserts any record into the database
    :param: container_name: name of the container
    :param: document_data: dictionary of document properties
    :param: entity_type: "user", "vendor", or "product" (required)
    :author(s): Joe Lee
    """
    try:
        container = db_connection.connect(container_name)

        entity_id = item_data.get(f"{entity_type}_id")
        if not entity_id:
            return "-1"

        item_id = f"{entity_type}_{entity_id}"

        document = {
            "id": item_id,
            "partitionKey": item_id,
            "entity_type": entity_type,
            **item_data
        }

        container.create_item(body=document)
        print(f"Successfully inserted {item_id} into {container_name}")
        return 0

    except Exception as e:
        print(f"Error in insert_item: {e}")
        return "-1"