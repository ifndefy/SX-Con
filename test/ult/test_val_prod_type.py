from validate.val_product_type import val_product_type

"""
    
Author: Kyle Valdez
Purpose: Checking if production type and syntax are in the database.
    
"""

def test_val_product_type():
    # Valid cases
    assert val_product_type("electronics") is True, "Expected 'electronics' to be a valid input"
    assert val_product_type("Furniture") is True, "Expected 'Furniture' to be a valid input"
    assert val_product_type("Toys") is True, "Expected 'Toys' to be a valid input"

    # Invalid: contains integers
    assert val_product_type("toy123") is False, "Expected 'toy123' to be an invalid input for integers"
    assert val_product_type("123") is False, "Expected '123' to be an invalid input for integers"

    # Invalid: contains special characters
    assert val_product_type("toy-car") is False, "Expected 'toy-car' to be an invalid input for special characters"
    assert val_product_type("toy_car") is False, "Expected 'toy_car' to be an invalid input for special characters"
    assert val_product_type("toy!") is False, "Expected 'toy!' to be an invalid input for special characters"

    # Invalid: None input
    assert val_product_type(None) is False, "Expected None input to be invalid"