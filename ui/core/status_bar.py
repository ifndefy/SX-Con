from PyQt6.QtCore import Qt
from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QWidget
from utils.message_bus import status_bar_instance

class StatusBar(QWidget):
    '''
    :purpose: Creates a atatus bar that waits on any incoming messages from the bus and updates it's appearence to reflect thats
    
    :return: None
    :author: Maksym Komarov, Joe lee
    '''
    event_handler = None

    def __init__(self, name, handler_func = None, parent = None):
        super().__init__(parent)
        self.setObjectName(name)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        if handler_func:
            self.add_handler(handler_func)

    def add_handler(self, func):
        self.event_handler = func
        status_bar_instance.bus_signal.connect(self.message_handler)
        status_bar_instance.error_signal.connect(self.flash_red)

    def flash_red(self):
        """
        :Purpose: Flashes the status bar red when an error is received
        :Author(s): Joe Lee
        """
        self.setStyleSheet("background-color: #691601;")
        QTimer.singleShot(2000, self._clear_style)

    def _clear_style(self):
        """
        :Purpose: Resets the style of the status bar
        :Author(s): Joe Lee
        """
        self.setStyleSheet("")

    def message_handler(self, msg = None):
        if self.event_handler:
            self.event_handler(msg)