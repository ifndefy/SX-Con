def val_username(username: str) -> int:
    # Set conditions
    max_length = 18
    min_length = 4

    # Allows username to include only upper and lowercase letters, as well as numbers.
    allowed_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

    if len(username) > max_length or len(username) < min_length:
        return -1

    if not all(char in allowed_chars for char in username):
        return -1

    return 0

