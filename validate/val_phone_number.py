import re

def val_phone_number(phone_num: str) -> bool:
    if not isinstance(phone_num, str): 
        return False

    regex = r"^(?:\d{3}-){2}\d{4}$"
    
    return bool(re.search(regex, phone_num))