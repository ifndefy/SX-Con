"""
Middle Name validation module
author(s): Alexander Bubienko
"""

import utils.logger.logger as log


def val_m_name(name: str) -> bool:
    """
    purpose: Validate that a middle name contains only letters (a-zA-Z) and spaces
    author(s): Alexander Bubienko
    return: True if valid middle name or empty/None, False otherwise
    
    Rules:
        - Can be None or empty string (allowed to omit middle name)
        - If provided, must be a string
        - Cannot have leading or trailing spaces
        - Can only contain letters a-z and A-Z, and spaces BETWEEN words
        - Cannot contain numbers, special characters, or accented characters
        - Cannot be only whitespace
    """
    # Allow None or empty string (middle name can be omitted)
    if name is None or name == "":
        return True
    
    # If it's not a string, reject it
    if not isinstance(name, str):
        log.error(f"Invalid middle name: Must be a string {name}")
        return False
    
    # Check if only whitespace (like "   ")
    if name.strip() == "":
        log.error(f"Invalid middle name: Contains only white space(s)")
        return False
    
    # Check for leading or trailing spaces
    if name != name.strip():
        log.error(f"Invalid middle name: must not be extended by white space(s)")
        return False
    
    # Check each character - only allow a-z, A-Z, and spaces
    for char in name:
        # Allow spaces
        if char.isspace():
            continue
        
        # Check if it's a letter in a-z or A-Z range
        if not ('a' <= char <= 'z' or 'A' <= char <= 'Z'):
            log.error(f"Invalid middle name: {name}, must only contain letters")
            return False
    
    return True