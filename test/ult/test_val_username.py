from validate.val_username import val_username

def test_val_username() -> bool:
    """
    :purpose: Tests the val_username() validation function
    :returns: 0 on success, -1 on failure
    :author(s): Colin Heinselman
    """

    # If val_username returns 0 (pass) for an invalid username, return -1.
    if val_username("123") == True:
        assert False, "Expected validation to return -1 for invalid username due to length being too short"
    if val_username("1234567890123456789") == True:
        assert False, "Expected validation to return -1 for invalid username due to length being too long"

    # If val_username returns -1 (fail) for a valid username, return -1.
    if val_username("1234") == False:
        assert False, "Expected validation to pass for valid username"
    if val_username("12345") == False:
        assert False, "Expected validation to pass for valid username"
    if val_username("123456789012345678") == False:
        assert False, "Expected validation to pass for valid username"

    # Checks that val_username fails usernames with special characters.
    if val_username("username") == False: # Should pass since it contains no special characters
        assert False, "Expected validation to pass for valid username"
    if val_username("$username") == True:
        assert False, "Expected validation to return -1 for invalid username due to special characters"
    if val_username("*username") == True:
        assert False, "Expected validation to return -1 for invalid username due to special characters"
