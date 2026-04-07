from validate.val_state import val_state

def test_val_state():
    """
        :purpose: Unit test for val_state() function
        :return: None
        :author(s): Colin Heinselman
    """

    # Invalid Inputs: "Empty" values
    assert val_state(None) == False, "Expected False for state input with value of None"
    assert val_state("") == False, "Expected False for state input with value of empty string ('')"
    assert val_state("  ") == False, "Expected False for state input with only spaces"


    # Invalid Inputs: Invalid Types (i.e. input is not a string)
    assert val_state({}) == False, "Expected False for state input with value of empty dict ({})"
    assert val_state([]) == False, "Expected False for state input with value of empty list ([])"
    assert val_state(["CA"]) == False, "Expected False for state input that is a list"
    assert val_state(12) == False, "Expected False for state input that is an integer"
    assert val_state(1.2) == False, "Expected False for state input that is a float"
    assert val_state(True) == False, "Expected False for state input that is a boolean"
    assert val_state(False) == False, "Expected False for state input that is a boolean"


    # Invalid Inputs: State contains numbers or special characters
    assert val_state("C1") == False, "Expected False for state input that contains numbers"
    assert val_state("C@") == False, "Expected False for state input that contains special characters"
    assert val_state("(a") == False, "Expected False for state input that contains special characters"


    # Invalid Inputs: State contains lowercase letters
    assert val_state("Ca") == False, "Expected False for state input with lowercase characters"
    assert val_state("cA") == False, "Expected False for state input with lowercase characters"


    # Invalid Inputs: State input is too short or too long (length != 2)
    assert val_state("C") == False, "Expected False for state input with a length of 1"
    assert val_state("A") == False, "Expected False for state input with a length of 1"
    assert val_state("CAL") == False, "Expected False for state input with a length of greater than 2"
    assert val_state("CALIFORNIA") == False, "Expected False for state input with a length of greater than 2"


    # Valid Inputs: State input containing no numbers or special characters, with length == 2.
    assert val_state("CA") == True, "Expected True for valid state input containing no special characters or numbers, and length == 2"
    assert val_state("AZ") == True, "Expected True for valid state input"