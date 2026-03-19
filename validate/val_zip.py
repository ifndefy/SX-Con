import utils.logger.logger as log


def val_zip(zip: int) -> bool:
    """
    validates a ZIP code

    returns False if:
        - value is None
        - contains alphabet
        - contains special characters
        - length is not 5

    else returns True
    Author(s): Colin Henderson
    """

    if zip is None or zip == "":
        log.error("Zip cannot be None")
        return False

    if not isinstance(zip, int):
        log.error("Zip code must be a integer")
        return False

    zip_str = str(zip)

    # Must be exactly 5 characters
    if len(zip_str) != 5:
        log.error("Zip code must have a length of 5 integers")
        return False

    return True