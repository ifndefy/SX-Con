import re as regex

def val_datetime(stat: str) -> bool:
    """
    purpose: validate that date time string contains the correct format
    author(s): Tim Liu
    parm stat: the string of the date time
    return: True if valid name, False otherwise
    """
    temp = regex.split(r'\s*--\s*', stat)
    if temp is None or (len(temp) != 2): return False
    if regex.match(r'^\d\d/\d\d/\d\d$', temp[0]) is None: return False
    if regex.match(r'^\d\d:\d\d$', temp[1]) is None: return False
    return True
