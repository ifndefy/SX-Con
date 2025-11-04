import bcrypt
def authenticate_password(password: str, stored_hash: str) -> str:
    try:
        if not isinstance(password, str) or not isinstance(stored_hash, str):
            return "-1"

        password_bytes = password.encode("utf-8")
        hash_bytes = stored_hash.encode("utf-8")

        if bcrypt.checkpw(password_bytes, hash_bytes):
            return "1"
        return "-1"

    except Exception:
        return "-1"