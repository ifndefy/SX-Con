import re

from validate.val_check_does_not_exist import val_check_does_not_exists
import utils.logger.logger as log

def val_product_name(prod_name: str) -> bool:
    """
    validates product name before insertion into database

    returns False if:
        - value is None
        - contains integers
        - contains special characters
        - already exists in DB

    else returns True
    Author(s): Colin Henderson
    """

    # Check None
    if prod_name is None:
        log.error(f"Product Name cannot be None")
        return False

    # Check only letters and spaces
    if not re.fullmatch(r"[A-Za-z ]+", prod_name):
        log.error("Product name must only contain alphabetical characters")
        return False

    return True