
from datetime import datetime
from ui.core.autogen_date import generate_host_datetime

def test_autogen_date():

    """
    purpose: test the accuracy of the generate_host_datetime function
    return: 0 on success, else -1
    author: Tyler Slagboom
    """

    try:
        now = datetime.now()
        format = "%m/%d/%y -- %H:%M:%S"
        now = now.strftime(format)
        auto_time = generate_host_datetime(include_seconds=True)

        print(now)
        print(auto_time)

        if now == auto_time:
            return 0

        return -1

    except Exception:
        return -1