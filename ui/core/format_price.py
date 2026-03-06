
# This class clones format_phone
# Modifications are made to fit into the mold of the price field

from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtCore import Qt

"""
    Param: self and parent (widgets)
    Purpose: input text widget, aligns it to the right and has a placeholder of "$0.00". Connects to user edits. Leading Zeroes.
    Author(s): Kyle Valdez
"""



class PriceField(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.setPlaceholderText("$0.00")
        self.textEdited.connect(self._format_price)

    def _format_price(self, text: str) -> None:

        cursor_from_end = len(text) - self.cursorPosition()

        digits = "".join(ch for ch in text if ch.isdigit())

        # If user deleted everything (or only non-digits), show placeholder by clearing text
        if not digits:
            self.blockSignals(True)
            self.setText("")
            self.blockSignals(False)
            return

        # Build dollars/cents
        if len(digits) == 1:
            dollars = "0"
            cents = "0" + digits
        else:
            dollars = digits[:-2]
            cents = digits[-2:]

        # Remove leading zeros in dollars, but keep at least one digit
        dollars = dollars.lstrip("0") or "0"

        formatted = f"${dollars}.{cents}"

        self.blockSignals(True)
        self.setText(formatted)
        # restore cursor
        new_pos = max(0, len(formatted) - cursor_from_end)
        self.setCursorPosition(new_pos)
        self.blockSignals(False)