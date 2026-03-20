from validate.val_rate import val_rate

"""

Author: Kyle Valdez
Purpose: To see if only acceptable inputs are integers, no special characters

"""

def test_val_rate():
    # Valid cases
    assert val_rate(0) is True, "Expected 0 to be a valid input"
    assert val_rate(50) is True, f"Expected 50 to be a valid input"
    assert val_rate(100) is True, f"Expected 100 to be a valid input"

    # Invalid: greater than 100
    assert val_rate(101) is False, f"Expected 101 to be an in valid input for exceeding 100"
    assert val_rate(150) is False, f"Expected 150 to be a valid input for exceeding 100"

    # Invalid: contains alphabet
    assert val_rate("10a") is False, f"Expected '10a' to be invalid input for string data type"
    assert val_rate("abc") is False, f"Expected 'abc' to be invalid input for string data type"

    # Invalid: contains special characters
    assert val_rate("10%") is False, f"Expected '10%' to be invalid input for string data type and special character"
    assert val_rate("10.5") is False, f"Expected '10.5' to be invalid input for string data type and special characters"

    # Invalid: None input
    assert val_rate(None) is False