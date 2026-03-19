from utils.logger import logger as log

def val_status(stat: str) -> bool:

    """
    purpose: to validate the value of a string Status
    return: True if valid, False otherwise
    author: Tyler Slagboom
    """

    if type(stat) is None:
        log.error(f'status cannot be None')
        return False

    if not isinstance(stat, str):
        log.error(f'status must be a string')
        return False

    allowed_chars = "abcdefghijklmnopqrstuvwxyz"
    stat_copy = stat.lower()

    if not any(x in allowed_chars for x in stat_copy):
        log.error(f'status must be alpha only')
        return False

    if stat not in "CLOSED" and stat not in "OPEN":
        log.error(f'status must be "OPEN" or "CLOSED"')
        return False

    return True