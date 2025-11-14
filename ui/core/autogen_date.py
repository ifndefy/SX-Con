from datetime import datetime
from typing import Union

def generate_host_datetime(include_seconds: bool = False) -> Union[str, int]:
    """
    Returns host-local time as 'MM:DD:YY--HH:MM' (or HH:MM:SS if include_seconds).
    On any error, returns -1.
    :author(s): Kyle Valdez
    """

    try:
        now = datetime.now()  # host's local time
        fmt = "%m/%d/%y -- %H:%M:%S" if include_seconds else "%m/%d/%y -- %H:%M"
        return now.strftime(fmt)
    except Exception:
        return -1