import utils.logger.logger as log


def val_qty_sold(sold: int, qty: int) -> bool:
    """
        purpose: validate that quantity sold is appropriate for qty
        author(s): Tim Liu
        parm sold: the sold amount
        param qty: the quantity in stock
        return: True if valid, False otherwise
    """
    if not isinstance(sold, int):
        log.error(f"Quantity sold must be an integer")
        return False

    if sold > qty:
        log.error(f"Quantity sold must be less than Quantity Signed {qty}")
        return False

    if sold < 0:
        log.error(f"Quantity sold must be positive")
        return False

    return True