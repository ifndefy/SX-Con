import re
import utils.logger.logger as log
def val_price(price: float | int) -> bool:
    """
    Author: Kyle Valdez
    Return: Boolean True or False values given either a float or int value
    Purpose: Validate a price value before inserting into a NoSQL database.

    Returns False if:
    - price is None
    - price contains alphabet characters
    - price contains special characters other than '.'

    Returns True otherwise.
    """
    if price is None:
        log.error("Price cannot be None")
        return False

    if not isinstance(price, (float, int)):
        log.error("Price must be a float or int")
        return False

    check = str(price)
    if isinstance(price, float) and len(check.split('.')[1]) > 2:
        log.error("Price contains too many integers after the decimal point")
        return False

    price_str = str(f"{float(price):.2f}")

    if re.match(r'^\d+.\d{2}$', price_str) is None:
        log.error("Price must contain only two digits after the decimal point")
        return False

    return True