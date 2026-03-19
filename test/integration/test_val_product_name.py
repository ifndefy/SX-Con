# test/test_val_product_name.py
from services.get_item_by_property import get_item_by_property
from validate.val_product_name import val_product_name
def test_val_product_name():

    assert val_product_name("uniquename") is True
    assert val_product_name(None) is False
    assert val_product_name("Product123") is False
    assert val_product_name("Product!") is False
    assert val_product_name("Product_Name") is False
    assert val_product_name("Bananas") is False