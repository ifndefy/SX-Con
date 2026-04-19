import utils.logger.logger as log

def val_username(username: str) -> bool:
    """
    :purpose: Validates username against length and special character requirements
    :return: True if Valid, False otherwise
    :author(s): Colin Heinselman
    """
    # Set conditions
    max_length = 18
    min_length = 4

    # Allows username to include only upper and lowercase letters, as well as numbers.
    allowed_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

    if len(username) > max_length or len(username) < min_length:
        log.error(f"Error: Username must be within {min_length} and {max_length} characters")
        return False

    if not all(char in allowed_chars for char in username):
        log.error(f"Error: Username contains invalid characters")
        return False

    return True

