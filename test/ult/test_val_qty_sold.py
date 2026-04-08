from validate.val_qty_sold import val_qty_sold

def test_val_qty_sold():
    """
    Purpose: test val_qty_sold function
    Author(s): Tim Liu
    """
    assert val_qty_sold(25, 100), 'unexpected, proper quantity sold failed'
    assert not val_qty_sold(-1, 100), 'unexpected, negative quantity sold was passed through'
    assert not val_qty_sold(101, 100), 'unexpected, quantity sold over quantity amount was passed through'
    assert not val_qty_sold('test', 100), 'unexpected, non-integer quantity sold was passed through'
