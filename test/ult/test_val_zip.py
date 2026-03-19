# test/test_val_zip.py

"""
Module test for val_zip
Author(s): Colin Henderson
"""

from validate.val_zip import val_zip


def test_val_zip():
    assert val_zip(12345), "Expected 12345 to be valid"
    assert not val_zip("12345"), "Expected '12345' to be false for string data type"
    assert not val_zip(None), "Expected 'None' to be invalid"
    assert not val_zip(1234), "Expected 1234 to be invalid for length 4"
    assert not val_zip(123456), "Expected 123456 to be invalid for length 6"