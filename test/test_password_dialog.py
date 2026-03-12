from unittest.mock import patch
from ui.prompts.password_dialog import PasswordChangeDialog

# should pass, dialog opens
def test_dialog_opens(app):
    dialog = PasswordChangeDialog(theme_manager=None)
    assert dialog is not None

# should pass, window title is correct
def test_dialog_title(app):
    dialog = PasswordChangeDialog(theme_manager=None)
    assert dialog.windowTitle() == "Change Password"

# should pass, there are inputs
def test_dialog_has_password_inputs(app):
    dialog = PasswordChangeDialog(theme_manager=None)
    assert dialog.new_password_input is not None
    assert dialog.confirm_password_input is not None

# should pass, password fields should start empty
def test_dialog_inputs_start_empty(app):
    dialog = PasswordChangeDialog(theme_manager=None)
    assert dialog.new_password_input.text() == ""
    assert dialog.confirm_password_input.text() == ""

# should pass, new_password should start as None before submission
def test_dialog_new_password_starts_none(app):
    dialog = PasswordChangeDialog(theme_manager=None)
    assert dialog.new_password is None

# should pass, matching passwords should be accepted
def test_dialog_accepts_change(app):
    dialog = PasswordChangeDialog(theme_manager=None)
    dialog.new_password_input.setText("password")
    dialog.confirm_password_input.setText("password")
    dialog.on_update_clicked()
    assert dialog.new_password == "password"

# should pass, password change should get rejected for pw not matching
def test_dialog_pw_change_fails_for_not_matching(app):
    with patch("ui.prompts.password_dialog.QMessageBox.warning"):
        dialog = PasswordChangeDialog(theme_manager=None)
        dialog.new_password_input.setText("password")
        dialog.confirm_password_input.setText("not password")
        dialog.on_update_clicked()
        assert dialog.new_password is None

# should pass, empty password should be rejected
def test_dialog_pw_change_fails_for_empty_strings(app):
    with patch("ui.prompts.password_dialog.QMessageBox.warning"):
        dialog = PasswordChangeDialog(theme_manager=None)
        dialog.new_password_input.setText("")
        dialog.confirm_password_input.setText("")
        dialog.on_update_clicked()
        assert dialog.new_password is None