def val_product_type(ptype: str) -> bool:
    """
    Author: Kyle Valdez
    Return: Boolean True or False values given 1 string
    Purpose: Validate a product type before inserting into a NoSQL database.

    Returns False if:
    - ptype is None
    - ptype contains integers
    - ptype contains special characters

    Returns True otherwise.
    """

    if ptype is None:
        return False

    # Ensure input is treated as a string
    ptype_str = str(ptype)

    # Reject digits
    if any(char.isdigit() for char in ptype_str):
        return False

    # Reject special characters (only allow alphabetic characters)
    if not all(char.isalpha() or char == ' ' for char in ptype_str):
        return False

    return True
