from typing import Any

from azure.cosmos.exceptions import CosmosResourceNotFoundError

from services.connect_database import db_connection


def get_item_by_property(container_name: str, entity_type: str, property_name: str, property_value: str) -> Any | None:
    """
    :purpose: Gets an entire document by property value and entity type
    :param: container_name: the Cosmos DB container to query
    :param: entity_type: "user", "vendor", or "product" (required)
    :param: property_name: the property to search by (e.g., "product_name", "phone")
    :param: property_value: the value to find
    :return: entire document as dictionary, or None if not found
    """
    try:
        container = db_connection.connect(container_name)

        # Query Cosmos DB by property
        query = f"SELECT * FROM c WHERE c.type = '{entity_type}' AND c.{property_name} = '{property_value}'"

        items = list(container.query_items(
            query=query,
            enable_cross_partition_query=True
        ))

        if items:
            print(f"Cosmos DB Container {container_name} found by {property_name}: {property_value}")
            return items[0]  # Return first match
        else:
            print(f"Cosmos DB container {container_name} not found by {property_name}: {property_value}")
            return None

    except Exception as e:
        print(f"Error in get_item_by_property: {e}")
        return None