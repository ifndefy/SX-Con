from validate.val_username import val_username

def test_val_username() -> int:
    """
    :purpose: Tests the val_username() validation function
    :returns: 0 on success, -1 on failure
    :author(s): Colin Heinselman
    """

    # If val_username returns 0 (pass) for an invalid password, return -1.
    if val_username("123") == 0:
        return -1
    if val_username("1234567890123456789") == 0:
        return -1

    # If val_username returns -1 (fail) for a valid password, return -1.
    if val_username("1234") == -1:
        return -1
    if val_username("12345") == -1:
        return -1
    if val_username("123456789012345678") == -1:
        return -1

    # Checks that val_username fails usernames with special characters.
    if val_username("username") == -1: # Should pass since it contains no special characters
        return -1
    if val_username("$username") == 0:
        return -1
    if val_username("*username") == 0:
        return -1

    # If no tests fail, then return 0
    return 0
