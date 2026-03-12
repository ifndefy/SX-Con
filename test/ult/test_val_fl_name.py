# test/test_val_fl_name.py
"""
Unit tests for val_fl_name validation function
author(s): Alexander Bubienko
"""

import sys
import os

from validate.val_fl_name import val_fl_name


def test_val_fl_name():
    """
    purpose: Test val_fl_name function with various inputs using assert statements
    author(s): Alexander Bubienko
    """
    
    # TEST GROUP 1: Valid names (should return True)
    
    # Simple first names
    assert val_fl_name("John") == True, "Expected True for simple first name 'John'"
    assert val_fl_name("Mary") == True, "Expected True for simple first name 'Mary'"
    
    # Names with spaces (first and last)
    assert val_fl_name("John Doe") == True, "Expected True for first and last name 'John Doe'"
    assert val_fl_name("Mary Jane Smith") == True, "Expected True for multiple names 'Mary Jane Smith'"
    
    # Names with mixed case
    assert val_fl_name("john") == True, "Expected True for lowercase name 'john'"
    assert val_fl_name("MARY") == True, "Expected True for uppercase name 'MARY'"
    assert val_fl_name("McDonald") == True, "Expected True for mixed case name 'McDonald'"
    
    
    # TEST GROUP 2: Invalid names - contains numbers (should return False)
    
    assert val_fl_name("John123") == False, "Expected False for name with numbers at end 'John123'"
    assert val_fl_name("123John") == False, "Expected False for name with numbers at start '123John'"
    assert val_fl_name("John123Doe") == False, "Expected False for name with numbers in middle 'John123Doe'"
    
    
    # TEST GROUP 3: Invalid names - contains special characters (should return False)
    
    assert val_fl_name("John-Doe") == False, "Expected False for hyphenated name 'John-Doe'"
    assert val_fl_name("O'Connor") == False, "Expected False for name with apostrophe 'O'Connor'"
    assert val_fl_name("John@Doe") == False, "Expected False for name with at symbol 'John@Doe'"
    assert val_fl_name("John_Doe") == False, "Expected False for name with underscore 'John_Doe'"
    assert val_fl_name("John#Doe") == False, "Expected False for name with hash symbol 'John#Doe'"
    assert val_fl_name("John$Doe") == False, "Expected False for name with dollar sign 'John$Doe'"
    assert val_fl_name("John%Doe") == False, "Expected False for name with percent sign 'John%Doe'"
    assert val_fl_name("John*Doe") == False, "Expected False for name with asterisk 'John*Doe'"
    
    
    # TEST GROUP 4: Invalid inputs - empty or whitespace (should return False)
    
    assert val_fl_name("") == False, "Expected False for empty string"
    assert val_fl_name("   ") == False, "Expected False for only spaces"
    assert val_fl_name("\t") == False, "Expected False for tab character"
    assert val_fl_name("\n") == False, "Expected False for newline character"
    assert val_fl_name(" John") == False, "Expected False for name with leading space"
    assert val_fl_name("John ") == False, "Expected False for name with trailing space"
    
    
    # TEST GROUP 5: Invalid inputs - None or wrong types (should return False)
    
    assert val_fl_name(None) == False, "Expected False for None value"
    assert val_fl_name(123) == False, "Expected False for integer input"
    assert val_fl_name(123.45) == False, "Expected False for float input"
    assert val_fl_name([]) == False, "Expected False for empty list"
    assert val_fl_name({}) == False, "Expected False for empty dict"
    assert val_fl_name(True) == False, "Expected False for boolean True"
    assert val_fl_name(False) == False, "Expected False for boolean False"
    
    
    # TEST GROUP 6: Edge cases (should return appropriate values)
    
    assert val_fl_name("A") == True, "Expected True for single letter 'A'"
    assert val_fl_name("A B") == True, "Expected True for single letters with space 'A B'"
    assert val_fl_name("A  B") == True, "Expected True for double space between letters 'A  B'"
    assert val_fl_name("Mary-Jane") == False, "Expected False for hyphenated name 'Mary-Jane'"
    assert val_fl_name("José") == False, "Expected False for accented character 'José'"