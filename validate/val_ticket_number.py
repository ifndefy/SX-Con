import utils.logger.logger as log
from validate.val_check_does_not_exist import val_check_does_not_exists

def val_ticket_number(ticket_num: int) -> bool:

    """
    purpose: validate that ticket numbers are valid
    return True if int and unique, else False
    author: Tyler Slagboom
    """

    if ticket_num is None:
        log.error(f'ticket number cannot be None')
        return False

    if not isinstance(ticket_num, int):
        log.error(f'ticket number must be an integer')
        return False

    if ticket_num < 0:
        log.error(f'ticket number must be greater than 0')
        return False

    check_exists = val_check_does_not_exists(
        'Consignments',
        'consignment',
        'consignment_id',
        ticket_num)

    if not check_exists:
        log.error(f'ticket number {ticket_num} already exists')
        return False

    return True