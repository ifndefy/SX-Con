import utils.logger.logger as log

def val_password(password: str) -> int:
    """
    :purpose:Validates password against max_length and min_length requirements.
    :param password: The String password to validate.
    :return: 0 if valid, -1 if invalid.
    :author(s): Colin Heinselman
    """

    # Set Conditions
    max_length = 25
    min_length = 4

    # No special character requirements, so they are allowed.
    if len(password) > max_length or len(password) < min_length:
        log.error(f"Password must be between {max_length} and {min_length}")
        return False

    return True