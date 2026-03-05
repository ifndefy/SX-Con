"""
tests if instances of format_state is correctly capitalizing the input and limiting to 2
"""
from ui.core.format_state import FormatState

def test_format_state(app):
    test_state_field = FormatState()

    test_state_field.setText("a")
    test_state_field.textEdited.emit("a")
    assert test_state_field.text() == "A", "Assert: Failed to capitalize"

    test_state_field.setText("")
    test_state_field.textEdited.emit("")
    assert test_state_field.text() == "", "Assert: Failed to clear field"

    test_state_field.setText("ab")
    test_state_field.textEdited.emit("ab")
    assert test_state_field.text() == "AB", "Assert: Failed to capitalize"

    test_state_field.setText("a")
    test_state_field.textEdited.emit("a")
    assert test_state_field.text() == "A", "Assert: Failed to capitalize"

    test_state_field.setText("abc")
    test_state_field.textEdited.emit("abc")
    assert test_state_field.text() == "AB", "Assert: Failed to capitalize"

    test_state_field.setText("1")
    test_state_field.textEdited.emit("1")
    assert test_state_field.text() == "", "Assert: Failed to prevent integer input"

    test_state_field.setText("*")
    test_state_field.textEdited.emit("*")
    assert test_state_field.text() == "", "Assert: Failed to prevent special character input"
