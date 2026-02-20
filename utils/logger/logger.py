import configparser as cparser
import logging as log
import logging.config as config
from pathlib import Path
try:
    from services.message_bus import status_bar_instance
except Exception:
    status_bar_instance = None

#Forwarding handler for passing any logging messages to the bus alongside the file handler, inherits base log handler
class ForwardHandler(log.Handler):
    def emit(self, record):
        if status_bar_instance is None:
            return
        try:
            status_bar_instance.bus_signal.emit(record.getMessage())
        except Exception:
            pass

#Logger setup to be done on import
#Create object to read in config file
config = cparser.ConfigParser()

CONFIG_PATH = Path(__file__).with_name("config.ini")
config.read(CONFIG_PATH)

#Get logger config values from file
__path = config.get('Logger Settings', 'log_path')
__name = config.get('Logger Settings', 'log_name')
__format = config.get('Logger Settings', 'log_format', raw = True)
__level_str = config.get('Logger Settings', 'log_level')

#convert level string to level attribute if exists
__level_attr = getattr(log, __level_str, log.CRITICAL)

#Setup values for log handler and format
__log_location = Path(__path) / __name
__log_location.parent.mkdir(parents=True, exist_ok=True)
__log_format = log.Formatter(__format) 

#Grab logger object from interpreter and create/open log file 
#(all modules share same logger obejct, can be changed in the future)
__app_logger = log.getLogger('base_logger')
__log_handler = log.FileHandler(__log_location, mode="a", encoding="utf-8")
__forward_handler = ForwardHandler()

#Set handler format and attach to logger object
__log_handler.setFormatter(__log_format)
__forward_handler.setFormatter(__log_format)
__app_logger.addHandler(__log_handler)
__app_logger.addHandler(__forward_handler)

__app_logger.setLevel(__level_attr)
status_bar_instance.set_logger(__app_logger)

#Actual logging functions
def debug(msg: str):
    __app_logger.debug(msg, stacklevel = 2)
    return

def error(msg: str):
    __app_logger.error(msg, stacklevel = 2)
    return

def info(msg: str):
    __app_logger.info(msg, stacklevel = 2)
    return

def warning(msg: str):
    __app_logger.warning(msg, stacklevel = 2)
    return

def critical(msg: str):
    __app_logger.critical(msg, stacklevel = 2)
    return