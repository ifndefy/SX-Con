import re

from validate.val_check_does_not_exist import val_check_does_not_exists


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
        return False

    # Check only letters and spaces
    if not re.fullmatch(r"[A-Za-z ]+", prod_name):
        return False

    # Check uniqueness in DB
    exists_check = val_check_does_not_exists(
        "Entities",
        "product",
        "product_name",
        prod_name
    )

    if exists_check == -1:
        return False

    return True