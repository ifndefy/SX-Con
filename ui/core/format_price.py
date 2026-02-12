from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtCore import Qt

# This class clones format_phone
# Modifications are made to fit into the mold of the price field

class PriceField(QLineEdit):

    def __init__(self, parent = None):
        """
            Param: self and parent (widgets)
            Purpose: input text widget, aligns it to the right and has a placeholder of "$0.00". Connects to user edits
            Author(s): Kyle Valdez
        """
        super().__init__(parent)
        self.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.setPlaceholderText("$0.00")
        self.textEdited.connect(self.__placeholder_manager)

    def __placeholder_manager(self, string):
        """
            Param: self and string (current text of user)
            Purpose: Make sure only integer digits are taken, formats the text as currency with looking for the last two numbers as cents.
                    QLineEdit is edited in real time.
            Author(s): Kyle Valdez
        """
        raw_text = "".join(filter(str.isdigit, string))

        if len(raw_text) <= 2:
            formatted = f"${raw_text.zfill(1)}"
        else:
            formatted = f"${raw_text[:-2]}.{raw_text[-2:]}"

        self.setText(formatted)