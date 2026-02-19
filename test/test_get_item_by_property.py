from services.get_item_by_property import get_item_by_property


def test_get_item_by_property() -> int:
    """
    Simple integration-style test.
    Returns:
        0  -> success (item retrieved)
        -1 -> failure (no item or exception)
    """

    try:
        # ---- Adjust these values to match real test data in your DB ----
        container_name = "Consignments"
        entity_type = "consignment"
        property_name = "id"
        property_value = "consignment_1"
        # ---------------------------------------------------------------

        result = get_item_by_property(
            container_name=container_name,
            entity_type=entity_type,
            property_name=property_name,
            property_value=property_value
        )

        if result:
            return 0
        else:
            return -1

    except Exception:
        return -1


