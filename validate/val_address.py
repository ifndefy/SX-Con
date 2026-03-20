import utils.logger.logger as log

def val_address(address: str) -> bool:
    """
    :purpose: Validation method for address input
    :param address: Address to validate
    :return: True if address is valid, False otherwise
    :author(s): Colin Heinselman
    """
    if address is None:
        log.error("Address is None")
        return False

    allowed_chars = " abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

    if not all(char in allowed_chars for char in address):
        log.error(f"Error: Address contains invalid characters")
        return False

    return True
