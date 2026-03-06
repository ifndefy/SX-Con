from typing import Union
from services.get_item_by_property import get_item_by_property


def val_check_does_not_exists(
    container: str,
    etype: str,
    property_name: str,
    value: Union[str, int]
) -> int:
    """
    Validates that a property value doesn't already exist

    Returns:
        0  -> value does not exist
        -1 -> value already exists
    Author(s): Colin Henderson
    """

    result = get_item_by_property(
        container,
        etype,
        property_name,
        value
    )

    if result is None:
        return 0
    else:
        return -1