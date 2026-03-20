from validate.val_rate import val_rate

"""

Author: Kyle Valdez
Purpose: To see if only acceptable inputs are integers, no special characters

"""

def test_val_rate():
    # Valid cases
    assert val_rate(0) is True
    assert val_rate(50) is True
    assert val_rate(100) is True

    # Invalid: greater than 100
    assert val_rate(101) is False
    assert val_rate(150) is False

    # Invalid: contains alphabet
    assert val_rate("10a") is False
    assert val_rate("abc") is False

    # Invalid: contains special characters
    assert val_rate("10%") is False
    assert val_rate("10.5") is False  # period not allowed for rate

    # Invalid: None input
    assert val_rate(None) is False