from validate.val_status import val_status

def test_val_status():

    """
    purpose: test the val_status function
    author: Tyler Slagboom
    """

    assert val_status("OPEN") == True, "Expected 'OPEN' to be a valid value"
    assert val_status("CLOSED") == True, "Expected 'CLOESD' to be a valid value"

    assert val_status("open") == False, "Expected 'open' to be an invalid value: lowercase"
    assert val_status("closed") == False, "Expected 'closed' to be an invalid value: lowercase"

    assert val_status("OPEN!") == False, "Expected 'OPEN!' to be an invalid value for special character and not in ('OPEN', 'CLOSED')"
    assert val_status("CLOSED!") == False, "Expected 'CLOSED!' to be an invalid value for special character and not in ('OPEN', 'CLOSED')"
    assert val_status("OPEN1") == False, "Expected 'OPEN!' to be an invalid value for integer character and not in ('OPEN', 'CLOSED')"
    assert val_status("CLOSED1") == False, "Expected 'CLOSED!' to be an invalid value for integer character and not in ('OPEN', 'CLOSED')"

    assert val_status(None) == False, "Expected None input to fail"
    assert val_status(1) == False, "Expected 1 to be an invalid value for integer character and not in ('OPEN', 'CLOSED')"
    assert val_status("") == False, "Expected '' to be an invalid value for empty string and not in ('OPEN', 'CLOSED')"
    assert val_status("abcde") == False, "Expected 'abcde' to be invalid value for not in ('OPEN', 'CLOSED')"

    assert val_status("aCLOSED") == False, "Expected 'aCLOSED' to be an invalid value for special character and not in ('OPEN', 'CLOSED')"
    assert val_status("aOPEN") == False, "Expected 'aOPEN' to be an invalid value for special character and not in ('OPEN', 'CLOSED')"
    assert val_status("CLOSEDz") == False, "Expected 'aOPEN' to be an invalid value for special character and not in ('OPEN', 'CLOSED')"
    assert val_status("OPENz") == False, "Expected 'OPENz' to be an invalid value for special character and not in ('OPEN', 'CLOSED')"
    assert val_status("CLOaSED") == False, "Expected 'CLOaSED' to be an invalid value for special character and not in ('OPEN', 'CLOSED')"
    assert val_status("OPaEN") == False, "Expected 'OPaEN' to be an invalid value for special character and not in ('OPEN', 'CLOSED')"
    assert val_status("aCLOSEDz") == False, "Expected 'aCLOSEDz' to be an invalid value for special character and not in ('OPEN', 'CLOSED')"
    assert val_status("aOPENz") == False, "Expected 'aOPENz' to be an invalid value for special character and not in ('OPEN', 'CLOSED')"