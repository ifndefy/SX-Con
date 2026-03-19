from validate.val_ticket_number import val_ticket_number

def test_val_ticket_number():

    """
    purpose: unit tests for the val_ticket_number function
    author: Tyler Slagboom
    """

    assert val_ticket_number(0) == True #legal low value
    assert val_ticket_number(2 ** 31) == True  # legal high value; shouldn't reach this number

    assert val_ticket_number(1) == False #illegal low value; ticket 1 exists
    assert val_ticket_number(-1) == False #illegal negative value
    assert val_ticket_number(-2**31) == False #illegal high negative value

    assert val_ticket_number("1") == False #illegal string input
    assert val_ticket_number("a") == False #illegal string input
    assert val_ticket_number("1a") == False #illegal string input
    assert val_ticket_number("!") == False #illegal string input
    assert val_ticket_number(None) == False #illegal None input
    assert val_ticket_number("") == False #illegal empty input