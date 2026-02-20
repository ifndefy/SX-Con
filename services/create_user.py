import re

from services.insert_item import insert_item
from services.get_max_value import get_max_value

def create_user(user_data: dict):
    """
    :purpose: Inserts a new user into the db with automated user_id creation
    :param: user_data: Dictionary containing user data with the following fields:
            username, first_name, last_name, password, q1_q, q1_a, q2_q, q2_a, admin
    :author(s): Colin Heinselman
    """

    status = validate_user_data(user_data)
    if status != 0:
        return status

    user_data["user_id"] = get_max_value("Entities", "user_id") + 1
    insert_item("Entities", "user", user_data)

    return 0


banned_substrings = [
        "administrator", "root", "system", "guest",
        "support", "help", "owner", "moderator",
        "login", "logout", "create", "delete", "config",
        "settings", "account", "profile", "username",
    ]


def contains_banned_substring(username: str) -> bool:
    """
    :purpose: Takes a username as input and determine if it includes any banned substrings
    :param username: The username to check
    :return: True if the username contains any banned substrings. False otherwise
    :author(s): Colin Heinselman
    """
    lower_username = username.lower()  # make check case-insensitive
    for banned in banned_substrings:
        if banned in lower_username:
            return True
    return False


def is_in_valid_regex(username):
    allowed_pattern = re.compile(r"^[a-zA-Z0-9_.]{3,20}$")
    forbidden_chars_pattern = re.compile(r"[\'\";#/*`<>$&|?:=%\\~\s]")

    if not allowed_pattern.fullmatch(username):
        return False
    elif re.search(forbidden_chars_pattern, username):
        return False

    return True


def is_valid_username(username: str) -> bool:

    if not is_in_valid_regex(username):
        return False
    if contains_banned_substring(username):
        return False

    return True


def user_dict_contains_required_fields(user_data):
    required_fields = ["username", "first_name", "last_name", "password", "q1_q", "q1_a", "q2_q", "q2_a", "admin"]

    if len(list(user_data.keys())) < 9 or not all(key in user_data for key in required_fields):
        print("User creation failed. Missing one of the following fields:")
        print("username, first_name, last_name, password, q1_q, q1_a, q2_q, q2_a, admin")
        return False

    return True

def validate_user_data(user_data):
    if not user_dict_contains_required_fields(user_data):
        print("User dictionary is missing required fields")
        print("User dictionary is missing required fields")
        return -1
    if not is_valid_username(user_data["username"]):
        print("Username is invalid")
        return -2
    return 0


