"""
First/Last Name validation module
author(s): Alexander Bubienko
"""

import utils.logger.logger as log

def val_fl_name(name: str) -> bool:
    """
    purpose: Validate that a name contains only letters and spaces
    author(s): Alexander Bubienko
    return: True if valid name, False otherwise
    
    Rules:
        - Must be a string
        - Cannot be None
        - Cannot be empty
        - Cannot be only whitespace
        - Can only contain letters (a-zA-Z) and spaces
        - Cannot contain numbers or special characters
    """
    # Check if None
    if name is None:
        log.error(f"Name field is empty")
        return False
    
    # Check if it's a string
    if not isinstance(name, str):
        log.error(f"Name field must be a string")
        return False
    
    # Check if empty or only whitespace
    if not name or name.strip() == "":
        log.error(f"Name field is empty")
        return False
    
    # Check for leading or trailing spaces
    if name != name.strip():
        log.error(f"Name field must not be extended by whitespace(s)")
        return False
    
    # Check each character - only allow letters and spaces
    for char in name:
        # Check if it's a space
        if char.isspace():
            continue
        
        # Check if it's a letter in a-z or A-Z range
        if not ('a' <= char <= 'z' or 'A' <= char <= 'Z'):
            log.error(f"Name field must only contain letters and spaces")
            return False
    
    # If we get here, all checks passed
    return True