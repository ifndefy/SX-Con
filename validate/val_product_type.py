import utils.logger.logger as log

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
        log.error("Product Type must not be None")
        return False

    # Ensure input is treated as a string
    ptype_str = str(ptype)

    # Reject digits
    if any(char.isdigit() for char in ptype_str):
        log.error(f"Product Type must not contain digits")
        return False

    # Reject special characters (only allow alphabetic characters)
    if not all(char.isalpha() or char == ' ' for char in ptype_str):
        log.error(f"Product Type must not contain special characters")
        return False

    return True
