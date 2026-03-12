import bcrypt

import utils.logger.logger as log

def authenticate_password(password: str, stored_hash: str) -> str:
    try:
        if not isinstance(password, str) or not isinstance(stored_hash, str):
            log.error(f"Password and stored hash must be of type str")
            return "-1"

        password_bytes = password.encode("utf-8")
        hash_bytes = stored_hash.encode("utf-8")

        if bcrypt.checkpw(password_bytes, hash_bytes):
            return "1"
        log.error(f"Password and stored hash do not match")
        return "-1"

    except Exception as e:
        log.error(f"Failed to authenticate {e}")
        return "-1"