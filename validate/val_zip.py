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

    if zip is None:
        return False

    zip_str = str(zip)

    # Must be exactly 5 characters
    if len(zip_str) != 5:
        return False

    # Must contain only digits
    if not zip_str.isdigit():
        return False

    return True