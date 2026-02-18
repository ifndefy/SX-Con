import re

from services.insert_item import insert_item
from services import get_max_value

banned_substrings = [
        "administrator", "root", "system", "guest",
        "support", "help", "owner", "moderator",
        "login", "logout", "create", "delete", "config",
        "settings", "account", "profile", "username",
        #"test",
        #"admin"
        # TODO: Uncomment out common testing substrings
    ]

def create_user(user_data: dict):
    """
    :purpose: Inserts a new user into the db with automated user_id creation
    :param: user_data: Dictionary containing user data with the following fields:
            username, first_name, last_name, password, q1_q, q1_a, q2_q, q2_a, admin
    :author(s): Colin Heinselman
    :return: -1 if user_data missing fields. 0 otherwise
    """


    required_fields = ["username", "first_name", "last_name", "password", "q1_q", "q1_a", "q2_q", "q2_a", "admin"]

    if len(list(user_data.keys())) < 9 or not all(key in user_data for key in required_fields):
        print("User creation failed. Missing one of the following fields:")
        print("username, first_name, last_name, password, q1_q, q1_a, q2_q, q2_a, admin")
        return -1

    user_data["type"] = "user"
    user_data["user_id"] = get_max_value.get_max_value("Entities", "user_id") + 1

    insert_item("Entities", "user", user_data)
    return 0

def is_username_valid(username: str) -> bool:
    """
    :purpose: Takes a username and checks if it is a valid username. Restricts certain keywords and special characters.
    :param username: The username
    :return: False if username is invalid. True otherwise
    :author(s): Colin Heinselman
    """

    allowed_pattern = re.compile(r"^[a-zA-Z0-9_.]{3,20}$")
    forbidden_chars_pattern = re.compile(r"[\'\";#/*`<>$&|?:=%\\~\s]")

    if contains_banned_substring(username):
        return False
    elif len(username) < 4:
        return False
    elif not allowed_pattern.fullmatch(username):
        return False
    elif forbidden_chars_pattern.fullmatch(username):
        return False

    return True


def contains_banned_substring(username: str) -> bool:
    lower_username = username.lower()  # make check case-insensitive
    for banned in banned_substrings:
        if banned in lower_username:
            return True
    return False





if __name__ == "__main__":
    #increment_user_counter()
    #print("Next user number = " + str(get_next_user_id()))

    user_dict = {
        "username": "test user",
        "first_name": "user123",
        "last_name": "test",
        "password": "239852734958",
        "q1_q": "question1",
        "q1_a": "answer",
        "q2_q": "question2",
        "q2_a": "answer",
        "admin": False,
    }

    max_user_id = get_max_value.get_max_value("Entities", "user_id")
    print(max_user_id)

    # Creates a valid user
    create_user(user_dict)

    user_dict2 = {
        "username": "test user2",
        "first_name": "user2",
        "last_name": "test2",
        "q1_q": "question1",
        "q1_a": "answer",
        "q2_q": "question2",
        "q2_a": "answer",
        "admin": False
    }
    # Should return an error
    create_user(user_dict2)


    print(is_username_valid("test_admin123"))








