def val_qty_sold(rem: int, qty: int) -> bool:
    """
        purpose: validate that the remaining is appropriate to quantity
        author(s): Tim Liu
        parm rem: the remaining amount
        param qty: the quantity in stock
        return: True if valid, False otherwise
    """
    if not isinstance(rem, int):
        return False

    if rem > qty:
        return False

    if rem < 0:
        return False

    return True