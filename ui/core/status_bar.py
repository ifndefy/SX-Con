from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget
from services.message_bus import status_bar_instance
import utils.logger as log

class StatusBar(QWidget):
    event_handler = None

    def __init__(self, name, handler_func = None, parent = None):
        super().__init__(parent)
        self.setObjectName(name)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        if handler_func:
            self.add_handler(handler_func)
    
    def add_handler(self, func):
        self.event_handler = func
        log.debug(f"Function {func} linked to status bar")
        status_bar_instance.bus_signal.connect(self.message_handler)
        log.debug(f"Slot created by [ID : {id(self)}] for [ID : {id(status_bar_instance)}]")
        
    def message_handler(self, msg = None):
        if self.event_handler:
            self.event_handler(msg)