import re
from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtCore import Qt

class PhoneNumField(QLineEdit):

    def __init__(self, parent = None):    
        """
            Creates a modified QLineEdit field to handle phone number formatting. Inherits base QLineEdit __init__() function, 
            adds default placeholder text to describe field and links function to handle input mask state. 
            Function is called on textEdited signal, only user input to change text will trigger masking check (setText() and other functions will not)
        """
        super().__init__(parent)
        self.masked = False
        self.setPlaceholderText("Phone Number")
        self.textEdited.connect(self.__placeholder_manager)
        

    def __placeholder_manager(self, string):
        """
            Private Function for handling input mask state, placeholder text is displayed if input is empty otherwise phone number format is enforced.\n
            
            [Args]: \n
                string: the current text content of the field, passed by textEdited signal handler
            
            No return values
        """

        #check for valid input, mask out non number inputs
        parsed_string = re.sub(r"\D", "", string)

        #Do we have some valid input for the field
        if parsed_string != "" and self.masked == False:    
            #Enforce mask
            self.setInputMask("999-999-9999")
            #Push cursor to offset mask characters
            new_cursor_pos =  re.search(r" |$", self.displayText()).start()
            self.setCursorPosition(new_cursor_pos)
            self.masked = True
        elif parsed_string == "":
            #No valid input left, remove mask and clear field (Acts as a psuedo input mask that rejects all non numbers for the field when mask is inactive)
            self.setInputMask("")
            self.setText("")
            self.masked = False

    def keyPressEvent(self, event):
        """
        :Purpose: Enables return key press events for the button
        :Author(s): Joe Lee
        """
        if event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            super().keyPressEvent(event)
        else:
            super().keyPressEvent(event)

    def clear_phone(self):
        """
        :Purpose: Clears the phone number field of its value and mask
        :Author(s): Joe Lee
        """
        self.setInputMask("")
        self.setText("")
        self.setObjectName("DEFAULT")
        self.style().unpolish(self)
        self.style().polish(self)
        self.setReadOnly(False)
        self.masked = False