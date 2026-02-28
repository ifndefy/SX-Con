
def val_password(password: str) -> int:
    # Set Conditions
    max_length = 25
    min_length = 4

    # No special character requirements, so they are allowed.
    if len(password) > max_length or len(password) < min_length:
        return -1

    return 0
