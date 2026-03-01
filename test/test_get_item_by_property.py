from services.get_item_by_property import get_item_by_property


def test_get_item_by_property() -> int:
    """
    Module test for get_item.
    Purpose: "Test if get_item_by_property.py retrieves data from the db. Return 0 if success and -1 if not"
    Author(s): Kyle Valdez
    """

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

    if not result:
        assert False, f"Could not get item by property {property_name} {property_value} from db"