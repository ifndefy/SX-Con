"""
Handler for open button
Wraps update_property to change the property "status" from "CLOSED" to "OPEN"
"""

from services.update_property import update_property

import utils.logger.logger as log


def handler_open_btn(ticket_index):
    try:
        update_property(
            container_name="Consignments",
            entity_type="consignment",
            entity_id=ticket_index,
            property_name="status",
            property_value="OPEN"
        )

    except Exception:
        log.error(f"Could not update status of ticket {ticket_index} to \"OPEN\"")