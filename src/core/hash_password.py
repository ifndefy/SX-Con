import bcrypt

import utils.logger.logger as log


def hash_password(password: str) -> str:
    try:
        if not isinstance(password, str) or not password:
            log.error("Password cannot be empty")
            return "-1"

        salt = bcrypt.gensalt(rounds=12)
        hashed = bcrypt.hashpw(password.encode("utf-8"), salt)

        if not bcrypt.checkpw(password.encode("utf-8"), hashed):
            log.error("Password does not match")
            return "-1"

        hashed_str = hashed.decode("utf-8")

        if len(hashed_str) != 60:
            log.error("Hashed password has an invalid length")
            return "-1"

        return hashed_str

    except Exception as e:
        log.error(f"Failed to hash password: {e}")
        return "-1"