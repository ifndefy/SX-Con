from validate.val_product_type import val_product_type

"""
    
Author: Kyle Valdez
Purpose: Checking if production type and syntax are in the database.
    
"""

def test_val_product_type():
    # Valid cases
    assert val_product_type("electronics") is True
    assert val_product_type("Furniture") is True
    assert val_product_type("Toys") is True

    # Invalid: contains integers
    assert val_product_type("toy123") is False
    assert val_product_type("123") is False

    # Invalid: contains special characters
    assert val_product_type("toy-car") is False
    assert val_product_type("toy_car") is False
    assert val_product_type("toy!") is False

    # Invalid: None input
    assert val_product_type(None) is False