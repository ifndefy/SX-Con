from services.connect_database import db_connection


def get_max_value(container_name, property_name):
    """
    :purpose: gets the max value of a property
    :param container_name: name of the container
    :param property_name: name of the property
    :return: max value of a property
    :author(s): Joe Lee
    """
    try:
        # Use the global connection directly
        container = db_connection.connect(container_name)
    except Exception as e:
        print(f"Error connecting to container {container_name}: {e}")
        return -1

    try:
        query = f"SELECT VALUE MAX(c.{property_name}) FROM c"

        items = list(container.query_items(
            query=query,
            enable_cross_partition_query=True
        ))

        if items and items[0] is not None:
            return items[0]
        else:
            return 0
    except Exception as e:
        print(f"Error querying max value: {e}")
        return -1