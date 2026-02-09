from services.connect_database import db_connection
import utils.logger as log

def autogen_ticket_num():
    """
    Returns the next ticket_num for the Consignments container.
    """
    try:
        container = db_connection.connect("Consignments")

        query = """
            SELECT VALUE MAX(c.ticket_number)
            FROM c
            WHERE c.type = 'consignment'
        """

        items = list(container.query_items(
            query=query,
            enable_cross_partition_query=True
        ))

        if items and items[0] is not None:
            max_ticket = int(items[0]) + 1
        else:
            max_ticket = 1

        return str(max_ticket)

    except Exception as e:
        log.error(f"Error generating ticket number: {e}")
        return "OFFLINE"