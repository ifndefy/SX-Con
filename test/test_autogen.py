from datetime import datetime

from services.connect_database import db_connection
from ui.core.autogen_ticket_num import autogen_ticket_num
from ui.core.autogen_date import generate_host_datetime

def test_autogen_ticket_num():
    """
    purpose: test the accuracy of the autogen_ticket_num function
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
        max_ticket = int(items[0])
    else:
        assert False, "Max Ticket number not found"

    ticket_num = int(autogen_ticket_num())
    if not ticket_num - max_ticket == 1:
        assert False, "New ticket number is not an increment of max ticket number"

def test_autogen_date():

    """
    purpose: test the accuracy of the generate_host_datetime function
    return: 0 on success, else -1
    author: Tyler Slagboom
    """
    now = datetime.now()
    format = "%m/%d/%y -- %H:%M:%S"
    now = now.strftime(format)
    auto_time = generate_host_datetime(include_seconds=True)

    if not now == auto_time:
        assert False, "Generated time is not the same as current system time"