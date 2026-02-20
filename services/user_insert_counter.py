from services.connect_database import db_connection
from services.get_item import get_item
from services.update_property import update_property
from services.insert_item import insert_item
import utils.logger.logger as log

def get_next_user_id():
    """
    :purpose: Returns the next user_id that can be inserted into the db
    :author(s): Colin Heinselman
    """
    container_name = "Entities"
    counter_id = "user_counter"
    partition_key = "counter"

    counter = get_item("Entities", "user", "counter")

    user_count = counter["current_user_count"] + 1
    return user_count

def increment_user_counter():
    """
    :purpose: Increments the user counter by 1 in the db, represented by the user with user_id: user_counter
    :author(s): Colin Heinselman
    """
    user_count = get_next_user_id()
    update_property("Entities", "user", "counter", "current_user_count", user_count)

def insert_new_user(user_data: dict):
    """
    :purpose: Inserts a new user into the db with automated user_id creation
    :param: user_data: Dictionary containing user data with the following fields:
            username, first_name, last_name, password, q1_q, q1_a, q2_q, q2_a, admin
    :author(s): Colin Heinselman
    """

    if len(list(user_data.keys())) < 9:
        log.error("User creation failed. Missing one of the following fields: username, first_name, last_name, password, q1_q, q1_a, q2_q, q2_a, admin")
        return -1

    user_data["type"] = "user"
    user_data["user_id"] = get_next_user_id()

    insert_item("Entities", "user", user_data)
    increment_user_counter()
    return 0


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

    insert_new_user(user_dict)



