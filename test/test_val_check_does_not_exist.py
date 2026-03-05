# test_val_check_exists.py

import uuid

from validate.val_check_does_not_exist import val_check_does_not_exists


def run_tests() -> int:
    """
    Returns:
        0  -> All tests passed
        -1 -> At least one test failed
    Author(s): Colin Henderson
    """

    existing_name = "Bananas"

    fail_result = val_check_does_not_exists(
        "Entities",
        "product",
        "product_name",
        existing_name
    )

    if fail_result != -1:
        return -1

    unique_value = f"UNIQUE_{uuid.uuid4()}"

    pass_result = val_check_does_not_exists(
        "Entities",
        "product",
        "product_name",
        unique_value
    )

    if pass_result != 0:
        return -1

    return 0