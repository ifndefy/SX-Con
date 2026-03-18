from validate.val_price import val_price

"""
 Author: Kyle Valdez
 Purpose: Different test cases to see if correct syntax is true and false otherwise
"""

def test_val_price():
    # Valid cases
    assert val_price(10) is True
    assert val_price(10.50) is True
    assert val_price("10.99") is True
    assert val_price("0.01") is True

    # Invalid: multiple periods
    assert val_price("10..5") is False

    # Invalid: special characters
    assert val_price("10$") is False
    assert val_price("10,00") is False
    assert val_price("10-00") is False

    # Invalid: alphabetic characters
    assert val_price("10a") is False
    assert val_price("abc") is False

    # Invalid: None input
    assert val_price(None) is False