from validate.val_check_does_not_exist import val_check_does_not_exists


def val_product_id(prod_id: int) -> bool:
    """
    validates product ID before insertion into database

    returns False if:
        - value is None
        - contains alphabet
        - contains special characters
        - already exists in DB

    else returns True
    Author(s):
    Colin Henderson
    """

    if prod_id is None:
        return False

    prod_id_str = str(prod_id)

    # Must contain only digits
    if not prod_id_str.isdigit():
        return False

    # Must not already exist in DB
    exists_check = val_check_does_not_exists(
        "Entities",
        "product",
        "product_id",
        prod_id
    )

    if not exists_check:
        return False

    return True