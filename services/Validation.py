# services/validation_service.py

from services.get_item_by_property import get_item_by_property

def val_check_exists(value: str):
    result = get_item_by_property(
        "Entities",
        "product",
        "product_name",
        value
    )
    return 0 if result is None else -1