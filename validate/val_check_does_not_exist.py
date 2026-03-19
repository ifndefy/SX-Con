from typing import Union
from services.get_item_by_property import get_item_by_property

import utils.logger.logger as log


def val_check_does_not_exists(
    container: str,
    etype: str,
    property_name: str,
    value: Union[str, int]
) -> bool:
    """
    Validates that a property value doesn't already exist

    Returns:
        True -> value does not exist
        False -> value already exists
    Author(s): Colin Henderson
    """

    result = get_item_by_property(
        container,
        etype,
        property_name,
        value
    )

    if result is None:
        log.info(f"Did not find existing items for {result}")
        return True
    else:
        log.info(f"Found existing items for {result} in {container}")
        return False