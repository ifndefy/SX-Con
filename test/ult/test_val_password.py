from validate.val_password import val_password

def test_val_password() -> int:
    """
    :purpose: Tests the val_password function against the current max and min length requirements
    :return: 0 if valid, -1 if invalid.
    :author(s): Colin Heinselman
    """

    # Checks invalid passwords (outside [min, max] length)
    if val_password("123") == True:
        assert False, "Expected validation to fail for length of password input being too short"
    if val_password("12345678901234567890123456") == True:
        assert False, "Expected validation to fail for length of password input being too long"

    # Checks valid passwords (inside [min, max] length)
    if val_password("1234") == False:
        assert False, "Expected validation to pass for valid input"
    if val_password("1234567890123456789012345") == False:
        assert False, "Expected validation to pass for invalid input"
