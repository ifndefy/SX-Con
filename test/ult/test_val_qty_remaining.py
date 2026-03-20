from validate.val_qty_remaining import val_qty_rem

def test_val_qty_remaining():
    """
        purpose: test the val_qty_remaining method
        author(s): Tim Liu
    """

    assert val_qty_rem(25,100), 'unexpected, remaining value being lower then quantity did not get accepted'
    assert not val_qty_rem(-10, 100), 'unexpected, negative remaining value got accepted'
    assert not val_qty_rem(101, 100), 'unexpected, remaining value over quantity got accepted'
    assert not val_qty_rem('test', 100), 'unexpected, non-integer remaining value got accepted'