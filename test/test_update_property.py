import random
import time
from services.delete_item import delete_item
from services.get_item import get_item
from services.get_property import get_property
from services.insert_item import insert_item
from services.update_property import update_property


def test_update_property():
    """
    Purpose: tests update property's functionality
    Method: inserts new item, compares property with static, then updates property, then compares property again, then deletes property
    Authors: Joe lee
    """

    seed = str(random.randint(5000, 10000))
    new_val = str(random.randint(1, 100))

    user_id = str(f"user_{seed}")
    vendor_id = str(f"vendor_{seed}")

    user_doc = {
        "user_id": seed,
        "username": "Smiley's Second Cousin",
        "first_name": "Twice Removed",
        "last_name": "No Cap",
        "password": "Definitely not a fake password",
        "q1_q": "foo",
        "q1_a": "bar",
        "q2_q": "typo",
        "q2_a": "chocolate",
    }

    vendor_doc = {
        'id': vendor_id,
        'partitionKey': f"vendor_{seed}",
        'vendor_id': int(seed),
        'phone': "098-765-4321",
        'first_name': "Smiley",
        'middle_name': "Mick",
        'last_name': "Smileyface",
        'address': "3rd McDonald's Avenue",
        'city': "Stockton",
        'state': "CA",
        'zip': 95820
    }


    try:
        # insert items
        insert_item("Entities", "user", user_doc)
        insert_item("Entities", "vendor", vendor_doc)

        # get properties to save for comparison
        user_comp = get_property("Entities", "last_name", "user", user_id)
        vendor_comp = get_property("Entities", "city", "vendor", str(seed))

        # initial comparison so there are no false positives
        if new_val == user_comp:
            return -1
        if new_val == vendor_comp:
            return -1

        # update prop
        update_property("Entities", "user", str(seed), "last_name", str(new_val))
        update_property("Entities", "vendor", str(seed), "city", str(new_val))

        # get properties after update for comparison
        user_comp = get_property("Entities", "last_name", "user", str(seed))
        vendor_comp = get_property("Entities", "city", "vendor", str(seed))

        # Compare after updating
        if new_val != user_comp:
            return -1
        if new_val != vendor_comp:
            return -1

        del1 = delete_item("Entities", "user", seed)
        if del1 == -1:
            return -1
        del2 = delete_item("Entities", "vendor", seed)
        if del2 == -1:
            return -1

        return 0

    except Exception:
        return -1

print(test_update_property())