import utils.logger.logger as log

def val_city(city: str) -> bool:
    """
    :purpose: Validates city name
    :param city: city name
    :return: True if city is valid, False otherwise
    :author(s): Colin Heinselman
    """
    allowed_chars = " abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

    if city is None:
        log.error("Error: city cannot be None")
        return False
    if city == "":
        log.error("Error: city cannot be an empty string")
        return False
    if type(city) != str:
        log.error("Error: city must be a string")
        return False

    if not all(char in allowed_chars for char in city):
        log.error("Error: city contains invalid characters")
        return False

    return True