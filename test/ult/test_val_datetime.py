from validate.val_datetime import val_datetime

def test_val_datetime():
    """
        purpose: test the validation datetime function
        author(s): Tim Liu
    """
    if val_datetime(''):
        assert False, 'Unexpected empty string passed in method'

    if val_datetime(' -- '):
        assert False, 'Unexpected empty 2 string passed in method'

    if val_datetime('wrong -- wrong'):
        assert False, 'Unexpected 2 wrong string passed in method'

    if val_datetime('12/12/12 -- wrong'):
        assert False, 'Unexpected time wrong string passed in method'

    if val_datetime('wrong -- 12:12'):
        assert False, 'Unexpected date wrong string passed in method'

    if not val_datetime('12/12/12 -- 12:12'):
        assert False, 'Unexpected correct date and time failed in method'