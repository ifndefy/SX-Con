import utils.logger.logger as log

def val_product_id(prod_id: int) -> bool:
    """
    validates product ID before insertion into database

    returns False if:
        - value is None
        - contains alphabet
        - contains special characters
        - already exists in DB

    else returns True
    Author(s): Colin Henderson
    """

    if prod_id is None:
        log.error("Product ID cannot be None")
        return False

    prod_id_str = str(prod_id)

    # Must contain only digits
    if not prod_id_str.isdigit():
        log.error("Product ID must be an integer")
        return False

    return True