from validate.val_username import val_username

def test_val_username() -> int:
    """
    :purpose: Tests the val_username() validation function
    :returns: 0 on success, -1 on failure
    :author(s): Colin Heinselman
    """

    # If val_username returns 0 (pass) for an invalid username, return -1.
    if val_username("123") == 0:
        assert False, "Expected validation to return -1 for invalid username due to length being too short"
    if val_username("1234567890123456789") == 0:
        assert False, "Expected validation to return -1 for invalid username due to length being too long"

    # If val_username returns -1 (fail) for a valid username, return -1.
    if val_username("1234") == -1:
        assert False, "Expected validation to pass for valid username"
    if val_username("12345") == -1:
        assert False, "Expected validation to pass for valid username"
    if val_username("123456789012345678") == -1:
        assert False, "Expected validation to pass for valid username"

    # Checks that val_username fails usernames with special characters.
    if val_username("username") == -1: # Should pass since it contains no special characters
        assert False, "Expected validation to pass for valid username"
    if val_username("$username") == 0:
        assert False, "Expected validation to return -1 for invalid username due to special characters"
    if val_username("*username") == 0:
        assert False, "Expected validation to return -1 for invalid username due to special characters"
