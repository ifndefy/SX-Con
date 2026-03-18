"""
tests if instances of format_phone are correctly masking inputs
"""
from ui.core.format_phone import PhoneNumField

def test_format_phone(app):
    test_phone_field = PhoneNumField()

    test_phone_field.setText("1")
    test_phone_field.textEdited.emit("1")
    assert test_phone_field.text() == "1--", "Assert: phone number failed to be masked"

    test_phone_field.setText("12")
    test_phone_field.textEdited.emit("12")
    assert test_phone_field.text() == "12--", "Assert: phone number failed to be masked"

    test_phone_field.setText("123")
    test_phone_field.textEdited.emit("123")
    assert test_phone_field.text() == "123--", "Assert: phone number failed to be masked"

    test_phone_field.setText("1234")
    test_phone_field.textEdited.emit("1234")
    assert test_phone_field.text() == "123-4-", "Assert: phone number failed to be masked"

    test_phone_field.setText("12345")
    test_phone_field.textEdited.emit("12345")
    assert test_phone_field.text() == "123-45-", "Assert: phone number failed to be masked"

    test_phone_field.setText("123456")
    test_phone_field.textEdited.emit("123456")
    assert test_phone_field.text() == "123-456-", "Assert: phone number failed to be masked"

    test_phone_field.setText("1234567")
    test_phone_field.textEdited.emit("1234567")
    assert test_phone_field.text() == "123-456-7", "Assert: phone number failed to be masked"

    test_phone_field.setText("12345678")
    test_phone_field.textEdited.emit("12345678")
    assert test_phone_field.text() == "123-456-78", "Assert: phone number failed to be masked"

    test_phone_field.setText("123456789")
    test_phone_field.textEdited.emit("123456789")
    assert test_phone_field.text() == "123-456-789", "Assert: phone number failed to be masked"

    test_phone_field.setText("1234567890")
    test_phone_field.textEdited.emit("1234567890")
    assert test_phone_field.text() == "123-456-7890", "Assert: phone number failed to be masked"