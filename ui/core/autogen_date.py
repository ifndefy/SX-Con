from datetime import datetime
from typing import Union

import utils.logger.logger as log

def generate_host_datetime(include_seconds: bool = False) -> Union[str, int]:
    """
    :Purpose: Generate a host-local time
    :Returns: host-local time as 'MM:DD:YY--HH:MM' | On any error, returns -1
    :Author(s): Kyle Valdez
    """

    try:
        now = datetime.now()  # host's local time
        fmt = "%m/%d/%y -- %I:%M:%S %p" if include_seconds else "%m/%d/%y -- %I:%M %p"
        return now.strftime(fmt)
    except Exception as e:
        log.error(f"Failed to generate host-local time: {e}")
        return -1