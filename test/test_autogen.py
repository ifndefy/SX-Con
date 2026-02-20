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

    try:
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
            return -1

        ticket_num = int(autogen_ticket_num())
        if ticket_num - max_ticket == 1:
            return 0

        return -1

    except Exception:
        return -1

def test_autogen_date():

    """
    purpose: test the accuracy of the generate_host_datetime function
    return: 0 on success, else -1
    author: Tyler Slagboom
    """

    try:
        now = datetime.now()
        format = "%m/%d/%y -- %H:%M:%S"
        now = now.strftime(format)
        auto_time = generate_host_datetime(include_seconds=True)

        print(now)
        print(auto_time)

        if now == auto_time:
            return 0

        return -1

    except Exception:
        return -1

print(test_autogen_date())
print(test_autogen_ticket_num())