from services.connect_database import db_connection
from services.get_max_value import get_max_value

def test_get_max_value():

    """
    purpose: test the accuracy of the get_max_value function
    return: 0 on success, else -1
    author: Tyler Slagboom
    """

    container = db_connection.connect('Consignments')
    property = 'ticket_number'

    query = f"SELECT VALUE MAX(c.{property}) FROM c"

    items = list(container.query_items(
        query=query,
        enable_cross_partition_query=True
    ))

    if items and items[0] is not None:
        max_value = items[0]
    else:
        assert False, "Did not find a max value"

    if not max_value == get_max_value(container, property):
        assert False, f"get_max_value returns {items[0]} when max is {max_value}"