import re as regex
import utils.logger.logger as log

def val_datetime(stat: str) -> bool:
    """
    purpose: validate that date time string contains the correct format
    author(s): Tim Liu
    parm stat: the string of the date time
    return: True if valid name, False otherwise
    """
    temp = regex.split(r'\s*--\s*', stat)
    if temp is None or (len(temp) != 2):
        log.error(f"Invalid date time: {stat}")
        return False
    if regex.match(r'^\d\d/\d\d/\d\d$', temp[0]) is None:
        log.error(f"Invalid date time: {stat}")
        return False
    if regex.match(r'^\d\d:\d\d(:\d\d)? (AM|PM)$', temp[1]) is None:
        log.error(f"Invalid date time: {stat}")
        return False
    return True
