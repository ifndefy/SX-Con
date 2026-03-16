import utils.logger.logger as log

def val_state(state: str) -> bool:
    """
    :purpose: Validates state name input
    :param state: state name to validate
    :return: True if state is valid, False otherwise
    :author(s): Colin Heinselman
    """

    allowed_chars = " abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

    if state is None:
        log.error("Error: State cannot be None")
        return False
    if state == "":
        log.error("Error: State cannot be empty")
        return False
    if not isinstance(state, str):
        log.error("Error: State must be a string")
        return False

    if len(state) <= 2:
        log.error("Error: State must be greater than 2 characters")
        return False
    if state.strip() == "":
        log.error("Error: State cannot be empty or only spaces")
        return False

    if not all(char in allowed_chars for char in state):
        log.error("Error: State contains invalid characters")
        return False

    return True