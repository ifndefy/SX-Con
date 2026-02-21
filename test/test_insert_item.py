import random

from services.connect_database import db_connection
from services.delete_item import delete_item
from services.insert_item import insert_item

def test_inesrt_item():
    """
    purpose: tests data insert_item method, then deletes the inserted item
    return: 0 on success, else -1
    author: Joe Lee
    """

    seed = random.randint(5000, 10000)

    pass_doc_id = str(f"vendor_{seed}")
    fail_doc_id = str(f"vendor_{seed}") # same, fail for duplication
    fail_doc2_id = seed # fail for data violtaion

    pass_document = {
        'id': pass_doc_id,
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

    fail_document = { # duplicate entry will fail
        'id': fail_doc_id,
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

    fail_document2 = { # should fail for data violation
        'id': fail_doc2_id,
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
        container = db_connection.connect('Entities')

        should_pass = insert_item(container, "vendor", pass_document)
        if should_pass != 0:
            return False

        should_fail = insert_item(container, "vendor", fail_document)
        if should_fail != -1:
            # should fail for duplicate unique key
            return False

        should_fail2 = insert_item(container, "vendor", fail_document2)
        if should_fail2 != -1:
            # should fail for data violation passing int into string field
            return False

        delete_item(container, "vendor", seed)

        return True

    except Exception:
        return -1