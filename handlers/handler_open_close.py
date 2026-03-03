"""
Handler for close button
Wraps update_property to change the property "status" from "OPEN" to "CLOSED"
"""

from services.update_property import update_property

import utils.logger.logger as log


def handler_open_close_btns(ticket_index, action):
    try:
        update_property(
            container_name="Consignments",
            entity_type="consignment",
            entity_id=ticket_index,
            property_name="status",
            property_value=str(action).upper()
        )

    except Exception:
        log.error(f"Could not update status of ticket {ticket_index} to \"CLOSED\"")