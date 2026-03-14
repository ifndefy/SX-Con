def val_rate(rate: int) -> bool:
    """
    Author: Kyle Valdez
    Return: Boolean True or False value given 1 int value
    Purpose: Validating a rate value before inserting into a NoSQL database.

    Returns False if:
    - rate is None
    - rate contains alphabet characters
    - rate contains special characters
    - rate is greater than 100

    Returns True otherwise.
    """

    if rate is None:
        return False

    # Convert to string for character validation
    rate_str = str(rate)

    # Reject alphabetic characters
    if any(char.isalpha() for char in rate_str):
        return False

    # Reject special characters (anything not numeric)
    if not rate_str.isdigit():
        return False

    # Convert to integer for numeric validation
    rate_int = int(rate_str)

    if rate_int > 100:
        return False

    return True
