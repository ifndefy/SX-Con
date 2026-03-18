import utils.logger.logger as log
from services.get_item_by_property import get_item_by_property
from src import SPOT

def val_ticket_number(ticket_num: int) -> bool:

    """
    purpose: validate that ticket numbers are valid
    return True if int and unique, else False
    author: Tyler Slagboom
    """

    if type(ticket_num) is None:
        log.error(f'ticket number cannot be None')
        return False

    if not isinstance(ticket_num, int):
        log.error(f'ticket number must be an integer')
        return False

    if ticket_num < 0:
        log.error(f'ticket number must be greater than 0')
        return False

    if not SPOT.OFFLINE:

        try:
            item = get_item_by_property("Consignments", "consignment", "consignment_id", ticket_num)

            if item is None:
                pass
            else:
                log.error(f'ticket number cannot be a duplicate')
                return False
        except Exception as e:
            log.error(f"Error querying the database: {e}")

    return True