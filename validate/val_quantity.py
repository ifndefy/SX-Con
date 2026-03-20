import utils.logger.logger as log


def val_quantity(qty: int) -> bool:
    if qty is None:
        log.error(f"Invalid quantity: None")
        return False

    if not isinstance(qty, int):
        log.error(f"Invalid quantity: Data type {type(qty)}is not int")
        return False

    if qty <= 0:
        log.error(f"Invalid quantity: Data value {qty} is negative")
        return False

    return True