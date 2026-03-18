# test/test_val_zip.py

"""
    Module test for val_zip
    Author(s): Colin Henderson
"""

from validate.val_zip import val_zip


def test_val_zip():
    assert val_zip(12345) is True
    assert val_zip("12345") is True
    assert val_zip(None) is False
    assert val_zip(1234) is False
    assert val_zip(123456) is False
    assert val_zip("12a45") is False
    assert val_zip("12-45") is False
    assert val_zip("12 45") is False