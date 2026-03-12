# test/test_val_vendor_id.py
"""
Unit tests for val_vendor_id validation function
author(s): Alexander Bubienko
"""
import sys
import os

from validate.val_vendor_id import val_vendor_id


def test_val_vendor_id():
    """
    purpose: Test val_vendor_id function with various inputs using assert statements
    author(s): Alexander Bubienko
    """
    
    # TEST GROUP 1: Valid integer inputs (should return True)
    
    assert val_vendor_id(123) == True, "Expected True for integer 123"
    assert val_vendor_id(0) == True, "Expected True for integer 0"
    assert val_vendor_id(-456) == True, "Expected True for integer -456"
    assert val_vendor_id(999999) == True, "Expected True for large integer"
    
    
    # TEST GROUP 2: Valid string inputs (should return True)
    
    assert val_vendor_id("123") == True, "Expected True for string '123'"
    assert val_vendor_id("0") == True, "Expected True for string '0'"
    assert val_vendor_id("  456  ") == True, "Expected True for string with spaces '  456  '"
    assert val_vendor_id("789") == True, "Expected True for string '789'"
    
    
    # TEST GROUP 3: Invalid inputs - non-integer strings (should return False)
    
    assert val_vendor_id("abc") == False, "Expected False for non-numeric string 'abc'"
    assert val_vendor_id("12.5") == False, "Expected False for decimal string '12.5'"
    assert val_vendor_id("123abc") == False, "Expected False for mixed string '123abc'"
    assert val_vendor_id("") == False, "Expected False for empty string"
    assert val_vendor_id("   ") == False, "Expected False for whitespace-only string"
    
    
    # TEST GROUP 4: Invalid inputs - wrong types (should return False)
    
    assert val_vendor_id(None) == False, "Expected False for None"
    assert val_vendor_id(12.5) == False, "Expected False for float 12.5"
    assert val_vendor_id([]) == False, "Expected False for empty list"
    assert val_vendor_id({}) == False, "Expected False for empty dict"
    
    
    # TEST GROUP 5: Edge cases (should return appropriate values)
    
    assert val_vendor_id("9999999999") == True, "Expected True for very large number string"
