from validate.val_product_id import val_product_id

"""
Module test for val_product_id
Author(s): Colin Henderson
"""

def test_val_product_id():
    assert val_product_id(12345) is True, "Expected 12345 to be a valid input"
    assert val_product_id(None) is False, "Expected None input to fail"
    assert val_product_id("123a") is False, "Expected '123a' to fail for non-integer data type"