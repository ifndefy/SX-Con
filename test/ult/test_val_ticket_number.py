from validate.val_ticket_number import val_ticket_number

def test_val_ticket_number():
    """
    purpose: unit tests for the val_ticket_number function
    author: Tyler Slagboom
    """

    assert val_ticket_number(123874), "Expected 123874 to be valid"
    assert not val_ticket_number(1), "Expected to fail for as ticket number 1 should already exists"
    assert not val_ticket_number(-2), "Expected to fail for illegal high negative value"
    assert not val_ticket_number("1"), "Expected to fail for illegal string input"
    assert not val_ticket_number(None), "Expected to fail for illegal None input"
