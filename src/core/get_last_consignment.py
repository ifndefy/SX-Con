from datetime import datetime
from services.connect_database import db_connection
from src import SPOT
import utils.logger.logger as log


def get_last_consignment(entity_type: str, entity_id: str) -> datetime | None:
    """
    Returns the datetime of the most recent consignment
    associated with the given entity.
    Author(s): Colin Henderson
    """

    if SPOT.OFFLINE:
        log.warning("OFFLINE - Invalid Action - Requires network access")
        return None

    try:
        container = db_connection.connect("Consignments")

        entity_id = int(entity_id)

        if entity_type == "vendor":
            query = f"""
                SELECT VALUE MAX(c.datetime)
                FROM c
                WHERE c.type = 'consignment'
                AND c.vendor_id = {entity_id}
            """

        elif entity_type == "product":
            query = f"""
                SELECT VALUE MAX(c.datetime)
                FROM c
                WHERE c.type = 'consignment'
                AND ARRAY_CONTAINS(c.product_ids, {entity_id})
            """

        elif entity_type == "user":
            query = f"""
                SELECT VALUE MAX(c.datetime)
                FROM c
                WHERE c.type = 'consignment'
                AND c.user_id = {entity_id}
            """

        else:
            log.error(f"Unsupported entity_type: {entity_type}")
            return None

        items = list(container.query_items(
            query=query,
            enable_cross_partition_query=True
        ))

        if items and items[0] is not None:
            return items[0]
        log.error(f"Could not retrieve datetime for {entity_type} {entity_id}")
        return None



    except Exception as e:
        log.error(f"Error in get_last_consignment: {e}")
        return None