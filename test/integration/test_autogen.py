from datetime import datetime

from ui.core.autogen_date import generate_host_datetime

def test_autogen_date():

    """
    purpose: test the accuracy of the generate_host_datetime function
    return: 0 on success, else -1
    author: Tyler Slagboom
    """
    now = datetime.now()
    format = "%m/%d/%y -- %I:%M:%S %p"
    now = now.strftime(format)
    auto_time = generate_host_datetime(include_seconds=True)

    if not now == auto_time:
        assert False, "Generated time is not the same as current system time"