# test_val_check_exists.py

import uuid

from validate.val_check_does_not_exist import val_check_does_not_exists


def test_val_check_does_not_exist() -> int:
    """
    Returns:
        0  -> All tests passed
        -1 -> At least one test failed
    Author(s): Colin Henderson
    """

    existing_name = "Produce"

    fail_result = val_check_does_not_exists(
        "Entities",
        "product",
        "product_name",
        existing_name
    )

    if fail_result != -1:
        assert False, f"Expected failure for {existing_name} as it already exists in DB"

    unique_value = f"UNIQUE_{uuid.uuid4()}"

    pass_result = val_check_does_not_exists(
        "Entities",
        "product",
        "product_name",
        unique_value
    )

    if pass_result != 0:
        assert False, f"Expected pass for {unique_value} as it is unlikely to exists in DB"
