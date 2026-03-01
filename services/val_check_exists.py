# services/validation_service.py

from services.get_item_by_property import get_item_by_property

def val_check_exists(value: str):
    """
    accepts a single string value for product name and checks if the product exists
    Author(s): Colin Henderson
    """
    result = get_item_by_property(
        "Entities",
        "product",
        "product_name",
        value
    )
    return 0 if result is None else -1