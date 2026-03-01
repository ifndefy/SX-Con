from validate.val_password import val_password

def test_val_password() -> int:
    """
    :purpose: Tests the val_password function against the current max and min length requirements
    :return: 0 if valid, -1 if invalid.
    :author(s): Colin Heinselman
    """

    # Checks invalid passwords (outside [min, max] length)
    if val_password("123") == 0:
        return -1
    if val_password("12345678901234567890123456") == -0:
        return -1

    # Checks valid passwords (inside [min, max] length)
    if val_password("1234") == -1:
        return -1
    if val_password("1234567890123456789012345") == -1:
        return -1

    return 0
