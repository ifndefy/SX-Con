import logging as log
import sys
from pathlib import Path
from datetime import datetime

try:
    from utils.message_bus import status_bar_instance
except Exception:
    status_bar_instance = None

#DEBUG -> INFO -> WARNING -> ERROR -> CRITICAL (All levels to the right are also passed)
__LOG_LEVEL = log.INFO

class ForwardHandler(log.Handler):
    def emit(self, record):
        if status_bar_instance is None:
            return
        msg = record.getMessage()
        status_bar_instance.bus_signal.emit(msg)
        if record.levelno >= log.ERROR:
            status_bar_instance.error_signal.emit(msg)

__timestamp = datetime.now().strftime("%Y-%m-%d")
__resolved_path = Path(sys.executable).parent if getattr(sys, 'frozen', False) else Path(__file__).parent
__log_location = __resolved_path / "logs" / f"{__timestamp}.log"
__log_location.parent.mkdir(parents=True, exist_ok=True)

__app_logger = log.getLogger('base_logger')
__log_handler = log.FileHandler(__log_location, mode="a", encoding="utf-8")
__forward_handler = ForwardHandler()

__log_format = log.Formatter("%(asctime)s | %(module)s -> %(funcName)s [%(levelname)s] : %(message)s")
__log_handler.setFormatter(__log_format)
__forward_handler.setFormatter(__log_format)
__app_logger.addHandler(__log_handler)
__app_logger.addHandler(__forward_handler)

__app_logger.setLevel(__LOG_LEVEL)
status_bar_instance.set_logger(__app_logger)

def debug(msg: str):
    __app_logger.debug(msg, stacklevel=2)

def error(msg: str):
    __app_logger.error(msg, stacklevel=2)

def info(msg: str):
    __app_logger.info(msg, stacklevel=2)

def warning(msg: str):
    __app_logger.warning(msg, stacklevel=2)

def critical(msg: str):
    __app_logger.critical(msg, stacklevel=2)