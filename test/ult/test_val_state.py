from validate.val_state import val_state

def test_val_state():
    """
        :purpose: Unit test for val_state() function
        :author(s): Colin Heinselman
    """

    # Invalid Inputs: "Empty" values
    assert val_state(None) == False, "Expected False for state input with value of None"
    assert val_state("") == False, "Expected False for state input with value of empty string ('')"
    assert val_state("     ") == False, "Expected False for state input with only spaces"


    # Invalid Inputs: Invalid Types (i.e. input is not a string)
    assert val_state({}) == False, "Expected False for state input with value of empty dict ({})"
    assert val_state([]) == False, "Expected False for state input with value of empty list ([])"
    assert val_state(["123"]) == False, "Expected False for state input that is a list"
    assert val_state(1234) == False, "Expected False for state input that is an integer"
    assert val_state(123.4) == False, "Expected False for state input that is a float"
    assert val_state(True) == False, "Expected False for state input that is a boolean"
    assert val_state(False) == False, "Expected False for state input that is a boolean"


    # Invalid Inputs: State contains numbers or special characters
    assert val_state("123California") == False, "Expected False for state input that contains numbers"
    assert val_state("$California") == False, "Expected False for state input that contains special characters"
    assert val_state("California:") == False, "Expected False for state input that contains special characters"


    # Invalid Inputs: State input is too short (<= 2 characters)
    assert val_state("Ca") == False, "Expected False for state input with a length of <= 2"
    assert val_state("C") == False, "Expected False for state input with a length of <= 2"


    # Valid Inputs: State input containing no numbers or special characters, with length > 2.
    assert val_state("California") == True, "Expected True for valid state input containing no special characters or numbers, and length >2"
    assert val_state("Arizona") == True, "Expected True for valid state input"
    assert val_state("New York") == True, "Expected True for valid state input with two words"
    assert val_state("massachusetts") == True, "Expected True for valid state name in all lower case"
    assert val_state ("MASSACHUSETTS") == True, "Expected True for valid state name in all upper case"