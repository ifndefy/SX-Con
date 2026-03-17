
def val_qty_sold(sold: int, qty: int) -> bool:
    """
        purpose: validate that quantity sold is an integer
        author(s): Tim Liu
        parm sold: the sold amount
        param qty: the quantity in stock
        return: True if valid integer, False otherwise
    """
    if sold is not int:
        return False

    if sold > qty:
        return False

    if sold < 0:
        return False

    return True