from validate.val_product_id import val_product_id

"""
Module test for val_product_id
Author(s): Colin Henderson
"""

def test_val_product_id():
    assert val_product_id(12345) is True
    assert val_product_id(None) is False
    assert val_product_id("123a") is False
    assert val_product_id("123-4") is False
    assert val_product_id(11) is False