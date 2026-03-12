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

    success, new_remaining, error = update_quantities(consignment_id, product_id, new_sold)

    assert success == True
    assert new_remaining is not None
    assert error == ""

# integration: should pass, invalid consignment returns false
def test_integration_invalid_consignment():
    success, new_remaining, error = update_quantities("901283", "Oakland Raiders", 1)
    assert success == False
    assert new_remaining is None