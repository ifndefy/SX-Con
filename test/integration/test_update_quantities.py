import pytest
from unittest.mock import MagicMock
from unittest.mock import patch
from src.core.update_quantities import _find_product_id
from src.core.update_quantities import _validate_sold
from src.core.update_quantities import update_quantities

# integration: should pass, sold and remaining update correctly
def test_integration_update_quantities():
    consignment_id = str(1)
    product_id = str(1)
    new_sold = 1

    success, new_remaining, error = update_quantities(consignment_id, product_id, new_sold, 0)

    assert success == True
    assert new_remaining is not None
    assert error == ""

# integration: should pass, invalid consignment returns false
def test_integration_invalid_consignment():
    success, new_remaining, error = update_quantities("901283", "Oakland Raiders", 1, 0)
    assert success == False
    assert new_remaining is None

# should pass, finds correct index
def test_find_product_id_found():
    products = [
        {"product_id": 1, "product_name": "apple"},
        {"product_id": 2, "product_name": "banana"}
    ]
    assert _find_product_id(products, "2") == 1

# should pass, returns None if not found
def test_find_product_id_not_found():
    products = [{"product_id": 1, "product_name": "apple"}]
    assert _find_product_id(products, str(999)) is None

# should pass, valid sold quantity
def test_validate_sold_valid():
    assert _validate_sold(5, 10) == True

# should pass, sold equals quantity exactly
def test_validate_sold_equal():
    assert _validate_sold(10, 10) == True

# should pass, sold cannot be negative
def test_validate_sold_negative():
    assert _validate_sold(-1, 10) == False

# should pass, sold cannot exceed quantity
def test_validate_sold_exceeds_signed():
    assert _validate_sold(11, 10) == False