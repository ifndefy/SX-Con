from services.get_item import get_item  # Adjust if module path differs


def test_get_item() -> int:
    """
    Module test for get_item.
    Purpose: "Test if get_item.py retrieves data from the db. Return 0 if success and -1 if not"
    Author(s): Kyle Valdez
    """

    # ---- Configure valid test values ----
    test_matrix = {
        "Entities": ["user", "product", "vendor"],
        "Consignments": ["consignment"]
    }

    entity_id = "1"
    # --------------------------------------

    try:
        for container, entity_types in test_matrix.items():
            for etype in entity_types:

                result = get_item(container, etype, entity_id)

                if result is None:
                    print(
                        f"FAIL -> container={container}, "
                        f"type={etype}, id={entity_id}"
                    )
                    return -1

        return 0

    except Exception as e:
        return -1

