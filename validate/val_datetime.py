import re as regex

def val_datetime(stat: str) -> bool:
    """
    purpose: validate that date time string contains the correct format
    author(s): Tim Liu
    parm stat: the string of the date time
    return: False if valid name, True otherwise
    """
    if len(stat) == 0:
        return False

    temp = stat.split('--')
    if(len(temp) != 2): return True
    if regex.match(r'^\d\d\\\d\d\\\d\d$', temp[0]) is None: return True
    if regex.match(r'^\d\d:\d\d$', temp[1]) is None: return True
    return False
