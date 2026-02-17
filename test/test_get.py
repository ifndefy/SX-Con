
from services.connect_database import db_connection
from services.get_max_value import get_max_value

def test_get_max_value():

    """
    purpose: test the accuracy of the get_max_value function
    return: 0 on success, else -1
    author: Tyler Slagboom
    """

    try:
        container = db_connection.container_name
        property = container.property_name

        query = f"SELECT VALUE MAX(c.{property}) FROM c"

        items = list(container.query_items(
            query=query,
            enable_cross_partition_query=True
        ))

        if items and items[0] is not None:
            max_value = items[0]
            print(max_value)
        else:
            max_value = -1

        if max_value == get_max_value(container, property):
            return 0

        return -1

    except Exception:
        return -1