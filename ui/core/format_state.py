import re
from PyQt6.QtWidgets import QLineEdit


class FormatState(QLineEdit):

    def __init__(self, parent = None):
        """"
            Param: self and parent (widgets)
            Purpose: input text widgets, it forces only alphabetical characters, and forces them capitalize
            Author(s): Tim Liu
        """
        super().__init__(parent)
        self.setPlaceholderText("ST")
        self.textEdited.connect(self.__placeholder_manager)

    def __placeholder_manager(self, string):
        """
            Param: self and string (current text of user)
            Purpose: input text widgets, it forces only alphabetical characters, and forces them capitalize
            Author(s): Tim Liu
        """
        self.setInputMask(">AA")
        new_cursor_pos = re.search(r" |$", self.displayText()).start()
        self.setCursorPosition(new_cursor_pos)