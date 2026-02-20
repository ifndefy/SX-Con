from services.insert_item import insert_item
from services.get_max_value import get_max_value

def create_user(user_data: dict):
    """
    :purpose: Inserts a new user into the db with automated user_id creation
    :param: user_data: Dictionary containing user data with the following fields:
            username, first_name, last_name, password, q1_q, q1_a, q2_q, q2_a, admin
    :author(s): Colin Heinselman
    """

    user_data["user_id"] = get_max_value("Entities", "user_id") + 1
    insert_item("Entities", "user", user_data)

    return 0
