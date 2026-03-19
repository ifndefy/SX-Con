from validate.val_status import val_status

def test_val_status():

    """
    purpose: test the val_status function
    author: Tyler Slagboom
    """

    assert val_status("OPEN") == True #legal value
    assert val_status("CLOSED") == True #legal value

    assert val_status("open") == False #illegal value; lower case
    assert val_status("closed") == False #illegal value; lower case

    assert val_status("OPEN!") == False #illegal value; contains special character
    assert val_status("CLOSED!") == False #illegal value; contains special character
    assert val_status("OPEN1") == False #illegal value; contains integer
    assert val_status("CLOSED1") == False #illegal value; contains integer

    assert val_status(None) == False #illegal value; is None
    assert val_status(1) == False #illegal value; is int
    assert val_status("") == False #illegal value; is empty
    assert val_status("abcde") == False #illegal value; is not in "CLOSED" or "OPEN

    assert val_status("aCLOSED") == False #illegal value; contains extra character
    assert val_status("aOPEN") == False #illegal value; contains extra character
    assert val_status("CLOSEDz") == False #illegal value; contains extra character
    assert val_status("OPENz") == False #illegal value; contains extra character
    assert val_status("CLOaSED") == False #illegal value; contains extra character
    assert val_status("OPaEN") == False #illegal value; contains extra character
    assert val_status("aCLOSEDz") == False #illegal value; contains extra characters
    assert val_status("aOPENz") == False #illegal value; contains extra characters