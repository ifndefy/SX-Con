"""
Unit tests for val_m_name validation function
author(s): Alexander Bubienko
"""

import sys
import os

from validate.val_m_name import val_m_name

def test_val_m_name():
    """
    purpose: Test val_m_name function with various inputs using assert statements
    author(s): Alexander Bubienko
    """
    
    # TEST GROUP 1: Valid inputs - None or empty (should return True)
    
    assert val_m_name(None) == True, "Expected True for None value"
    assert val_m_name("") == True, "Expected True for empty string"
    
    
    # TEST GROUP 2: Valid middle names (should return True)
    
    # Simple middle names
    assert val_m_name("James") == True, "Expected True for simple middle name 'James'"
    assert val_m_name("Marie") == True, "Expected True for simple middle name 'Marie'"
    
    # Middle names with spaces (multiple middle names)
    assert val_m_name("James Paul") == True, "Expected True for multiple middle names with space 'James Paul'"
    assert val_m_name("Anne Marie") == True, "Expected True for multiple middle names 'Anne Marie'"
    
    # Mixed case
    assert val_m_name("james") == True, "Expected True for lowercase middle name 'james'"
    assert val_m_name("JAMES") == True, "Expected True for uppercase middle name 'JAMES'"
    assert val_m_name("McKay") == True, "Expected True for mixed case with capital in middle 'McKay'"
    
    # Single letter
    assert val_m_name("A") == True, "Expected True for single letter 'A'"
    assert val_m_name("J P") == True, "Expected True for single letters with space 'J P'"
    
    
    # TEST GROUP 3: Invalid names - contains numbers (should return False)
    
    assert val_m_name("James123") == False, "Expected False for name with numbers at end 'James123'"
    assert val_m_name("123James") == False, "Expected False for name with numbers at start '123James'"
    assert val_m_name("James123Paul") == False, "Expected False for name with numbers in middle 'James123Paul'"
    
    
    # TEST GROUP 4: Invalid names - contains special characters (should return False)
    
    assert val_m_name("James-Paul") == False, "Expected False for hyphenated name 'James-Paul'"
    assert val_m_name("O'Malley") == False, "Expected False for name with apostrophe 'O'Malley'"
    assert val_m_name("James@Paul") == False, "Expected False for name with at symbol 'James@Paul'"
    assert val_m_name("James_Paul") == False, "Expected False for name with underscore 'James_Paul'"
    assert val_m_name("James#Paul") == False, "Expected False for name with hash symbol 'James#Paul'"
    assert val_m_name("James$Paul") == False, "Expected False for name with dollar sign 'James$Paul'"
    assert val_m_name("James%Paul") == False, "Expected False for name with percent sign 'James%Paul'"
    assert val_m_name("James*Paul") == False, "Expected False for name with asterisk 'James*Paul'"
    
    
    # TEST GROUP 5: Invalid inputs - whitespace issues (should return False)
    
    assert val_m_name("   ") == False, "Expected False for only spaces"
    assert val_m_name("\t") == False, "Expected False for tab character"
    assert val_m_name("\n") == False, "Expected False for newline character"
    assert val_m_name(" James") == False, "Expected False for name with leading space"
    assert val_m_name("James ") == False, "Expected False for name with trailing space"
    assert val_m_name(" James ") == False, "Expected False for name with leading and trailing spaces"
    
    
    # TEST GROUP 6: Invalid inputs - accented characters (should return False)
    
    assert val_m_name("José") == False, "Expected False for accented e 'José'"
    assert val_m_name("François") == False, "Expected False for accented c 'François'"
    assert val_m_name("Müller") == False, "Expected False for umlaut 'Müller'"
    assert val_m_name("José María") == False, "Expected False for multiple accented characters 'José María'"
    
    
    # TEST GROUP 7: Invalid inputs - wrong types (should return False)
    
    assert val_m_name(123) == False, "Expected False for integer input"
    assert val_m_name(123.45) == False, "Expected False for float input"
    assert val_m_name([]) == False, "Expected False for empty list"
    assert val_m_name({}) == False, "Expected False for empty dict"
    assert val_m_name(True) == False, "Expected False for boolean True"
    assert val_m_name(False) == False, "Expected False for boolean False"
