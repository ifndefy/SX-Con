import re

from utils import logger
from PyQt6.QtWidgets import QLineEdit

class PhoneNumField(QLineEdit):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.masked = False
        self.setPlaceholderText("Phone Number")
        self.textEdited.connect(self.__placeholder_manager)

    def __placeholder_manager(self, string):
        parsed_string = re.sub(r"\D", "", string)

        if parsed_string != "" and self.masked == False:    
            self.setInputMask("(999)999-9999")
            self.cursorForward(False, len(parsed_string))
            self.masked = True
        elif parsed_string == "":
            self.setInputMask("")
            self.clear()
            self.masked = False