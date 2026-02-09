from PyQt6.QtCore import QObject
from PyQt6.QtCore import pyqtSignal

class MessageBus(QObject):
    bus_signal = pyqtSignal(str)

    def __init__(self, logger = None):
        super().__init__()
        self.logger = logger

    def send_message(self, msg):
        self.bus_signal.emit(msg)
        if self.logger:
            self.logger.debug(f"Message sent on bus [ID : {id(self)}]: {msg}")
    
    def set_logger(self, logger):
        self.logger = logger

#Create global status_bar instance on first import, producers can use the message function to pass a signal down the bus
#Consumers can connect to the bus to perform work on the data in the bus. In this case the Status bar is connected in the main window, 
#allowing child processes to communicate with the parent anywhere in the hierarchy 
status_bar_instance = MessageBus()
