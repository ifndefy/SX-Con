from validate.val_datetime import val_datetime

def test_val_datetime():
    """
        purpose: test the validation datetime function
        author(s): Tim Liu
    """
    if val_datetime(''):
        assert False

    if val_datetime(' -- '):
        assert False

    if val_datetime('wrong -- wrong'):
        assert False

    if val_datetime('12/12/12 -- wrong'):
        assert False

    if val_datetime('wrong -- 12:12'):
        assert False

    if not val_datetime('12/12/12 -- 12:12'):
        assert False