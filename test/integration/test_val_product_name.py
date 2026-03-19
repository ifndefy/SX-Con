# test/test_val_product_name.py
from services.get_item_by_property import get_item_by_property
from validate.val_product_name import val_product_name
def test_val_product_name():

    assert val_product_name("uniquename") is True, "Expected 'uniquename' to be valid"
    assert val_product_name(None) is False, "Expected None input to be invalid"
    assert val_product_name("Product123") is False, "Expected 'Product123' to be invalid for integers"
    assert val_product_name("Product!") is False, "Expected 'Product!' to be invalid for special character"