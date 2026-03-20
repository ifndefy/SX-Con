from validate.val_price import val_price

"""
 Author: Kyle Valdez
 Purpose: Different test cases to see if correct syntax is true and false otherwise
"""


def test_val_price():
    # Valid cases
    assert val_price(10), "Expected 10 to be converted to 10.00 then validated"
    assert val_price(10.50), "Expected 10.50 to be valid"
    assert not val_price("10.99"), "Expected '10.99' to be invalid for string data type"
    assert val_price(10.99), "Expected 10.99 to be valid"
    assert not val_price(10.999), "Expected 10.999 to be invalid for too many digits after the decimal"
    assert not val_price("0.01"), "Expected '0.01' to be invalid for string data type"

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