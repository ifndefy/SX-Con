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
        return False

    price_str = str(price)

    # Reject alphabetic characters
    if any(char.isalpha() for char in price_str):
        return False

    # Allow digits and at most one period
    if price_str.count('.') > 1:
        return False

    for char in price_str:
        if not (char.isdigit() or char == '.'):
            return False

    return True
