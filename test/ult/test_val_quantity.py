from validate.val_quantity import val_quantity

def test_val_quantity():
    assert val_quantity(10), "Expected 10 to be valid quantity"
    assert not val_quantity("10"), "Expected '10' to fail for invalid data type"
    assert not val_quantity(-1), "Expected -1 to fail for negative quantity"
