from services.get_item import get_item  # Adjust if module path differs


def test_get_item() -> int:
    """
    Module test for get_item.
    Purpose: "Test if get_item.py retrieves data from the db. Return 0 if success and -1 if not"
    Author(s): Kyle Valdez
    """

    # ---- Configure valid test values ----
    container_name = "Container name (Entities)"
    entity_type = "Entity Type (product, user, vendor)"
    entity_id = "Entity id (int)"
    # --------------------------------------

    try:
        result = get_item(container_name, entity_type, entity_id)

        if result is not None:
            return 0
        else:
            return -1

    except Exception:
        return -1
