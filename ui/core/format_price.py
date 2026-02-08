from PyQt6.QtGui import QIntValidator
from PyQt6.QtWidgets import QLineEdit

line_edit = QLineEdit()

def format_price(value):

    if value is None:
        return -1
    
    if type(value) is not str:
        return -1
    
    if value == "":
        return -1
    

    #checks to see if each index is a digit between 0-9, less than will result in -1
    index = 0
    while (index < len(value)):
        ch  = value[index]

        if ch < "0" and ch > "9":
            return -1
        
        index = index + 1


    #value is at least 3 in length, ad zeroes in front to make sure it is 3
    while (len(value) < 3):
        value = "0" + value


    #dollars and cents part, use string slicing to make sure cents .00
    dollars_parted  = value[0: len(value) - 2]
    cents_parted = value[len(value) - 2: len(value)]

    dollars_format = int(dollars_parted)

    formatted_amount = "$" + str(dollars_format) + "." + cents_parted

    return formatted_amount

def restricted_format_price ():
    
    validator = QIntValidator(0, 10000000)
    line_edit.setValidator(validator)

    def user_types (text):

        digits = ""
        i = 0
        while (i < len(text)):
            ch = text[i]

            if ch >= "0" and ch <= "9":
                digits = digits + ch

            i = i + 1

        if digits == "":
            line_edit.setText("")
            return
        
        formatted = format_price(digits)

        if formatted == -1:
            line_edit.setText("")
            return
        
        line_edit.setText(formatted)

        line_edit.tetEdited.connect(user_types)

        return -1
    
    return -1




