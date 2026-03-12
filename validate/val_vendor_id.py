"""
Vendor ID validation module
author(s): Alexander Bubienko
"""

def val_vendor_id(v_id) -> bool:
    """
    purpose: Validate that a vendor ID is an integer
    author(s): Alexander Bubienko
    return: True if valid integer, False otherwise

    """
    try:
        # Check if it's already an integer
        if isinstance(v_id, int):
            return True
        
        # Check if it's a string that represents an integer
        if isinstance(v_id, str) and v_id.strip().isdigit():
            return True
        
        # If it's neither an int nor a digit string, it's invalid
        return False
        
    except Exception:
        # Any unexpected error means validation fails
        return False