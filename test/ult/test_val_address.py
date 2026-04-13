from validate.val_address import val_address

def test_val_address():
    """
        :purpose: Unit tests for the val_address() function, tested against None and special character requirements
        :return: None
        :author(s): Colin Heinselman
        """
    if val_address(None) == True:
        assert False, "Expected validation to fail for address being None"
    if val_address("%123 Drive") == True:
        assert False, "Expected validation to fail for address containing special characters"
    if val_address("123 Drive/") == True:
        assert False, "Expected validation to fail for address containing special characters"


    if val_address("") == False:
        assert False, "Expected validation to pass for valid input"
    if val_address("123 California Street") == False:
        assert False, "Expected validation to pass for valid input"