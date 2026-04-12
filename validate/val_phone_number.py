import re
import utils.logger.logger as log


def val_phone_number(phone_num: str) -> bool:
    '''
    :purpose: Validate that the phone number is in the format : ###-###-#### using regex
    
    :return: True on success, False on Fail
    :author: Maksym Komarov
    '''
    if not isinstance(phone_num, str):
        log.error("Phone number must be a string")
        return False

    regex = r"^(?:\d{3}-){2}\d{4}$"
    
    if bool(re.search(regex, phone_num)):
        return True
    else:
        log.error("Invalid phone number")
        return False