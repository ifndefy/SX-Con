from services.get_property import get_property
from src import SPOT


def test_get_property() -> int:
    """
   Module test for get_property
   Purpose: To see if get_property is working and retrieving an attribute value from both containers
   Authors: Kyle Valdez
    """

    SPOT.OFFLINE = False

    test_matrix = {
        "Entities": ["user", "product", "vendor"],
        "Consignments": ["consignment"]
    }

    attribute = "id"
    entity_id = "1"

    for container_name, entity_types in test_matrix.items():
        for entity_type in entity_types:

            result = get_property(
                container_name=container_name,
                attribute=attribute,
                entity_type=entity_type,
                id_value=entity_id
            )

            expected_value = f"{entity_type}_{entity_id}"

            if result != expected_value:
                assert False, f"{result} != {expected_value}"