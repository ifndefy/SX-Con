
def val_qty_sold(sold: int, qty: int) -> bool:
    """
        purpose: validate that quantity sold is appropriate for qty
        author(s): Tim Liu
        parm sold: the sold amount
        param qty: the quantity in stock
        return: True if valid, False otherwise
    """
    if not isinstance(sold, int):
        return False

    if sold > qty:
        return False

    if sold < 0:
        return False

    return True