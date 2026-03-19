import utils.logger.logger as log


def val_qty_rem(rem: int, qty: int) -> bool:
    """
        purpose: validate that the remaining is appropriate to quantity
        author(s): Tim Liu
        parm rem: the remaining amount
        param qty: the quantity in stock
        return: True if valid, False otherwise
    """
    if not isinstance(rem, int):
        log.error("Quantity Remaining must be an integer")
        return False

    if rem > qty:
        log.error(f"Quantity Remaining must be less than Quantity Signed: {qty}")
        return False

    if rem < 0:
        log.error(f"Quantity Remaining must be positive")
        return False

    return True