from validate.val_city import val_city

def test_val_city():
    """
    :purpose: Tests the validation city function
    :return: None
    :author(s): Colin Heinselman

    """

    # Invalid Inputs : "Empty" values
    if val_city(None) == True:
        assert False, "Expected False for city with a value of None"
    if val_city("") == True:
        assert False, "Expected False for city that is an empty string"

    # Invalid Inputs: Invalid Types (i.e. input is not a string)
    if val_city({}) == True:
        assert False, "Expected False for city that is an empty dictionary"
    if val_city({"a": 1}) == True:
        assert False, "Expected False for city that is a dictionary"
    if val_city([]) == True:
        assert False, "Expected False for city that is an empty list"
    if val_city(["123"]):
        assert False, "Expected False for city that is a list"
    if val_city(1234) == True:
        assert False, "Expected False for integer input"
    if val_city(True) == True:
        assert False, "Expected False for boolean input"


    # Invalid Inputs: City contains numbers or special characters
    if val_city("123Sacramento") == True:
        assert False, "Expected False for city that contains numbers"
    if val_city("$Sacramento") == True:
        assert False, "Expected False for city that contains special characters"
    if val_city("Sacramento:") == True:
        assert False, "Expected False for city that contains special characters"


    # Valid Inputs: City names with no numbers or special characters
    if val_city("Sacramento") == False:
        assert False, "Expected True for city name 'Sacramento' containing no numbers or special characters"
    if val_city("Rancho Cordova") == False:
        assert False, "Expected True for two-word city name 'Rancho Cordova' containing no numbers or special characters"