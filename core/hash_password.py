import bcrypt

def hash_password(password: str) -> str:
    try:
        if not isinstance(password, str) or not password:
            return "-1"

        salt = bcrypt.gensalt(rounds=12)
        hashed = bcrypt.hashpw(password.encode("utf-8"), salt)

        if not bcrypt.checkpw(password.encode("utf-8"), hashed):
            return "-1"

        hashed_str = hashed.decode("utf-8")

        if len(hashed_str) != 60:
            return "-1"

        return hashed_str

    except Exception:
        return "-1"


if __name__ == "__main__":
    # Example usage (for testing only)
    user_input = input("Enter password: ")
    result = hash_password(user_input)
    print(f"Result: {result}")
