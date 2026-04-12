from unittest.mock import patch, MagicMock

from src.user import current_user
from ui.core.theme_manager import ThemeManager
from ui.main_window import MainWindow
from ui.prompts.login import LoginScreen


"""
Sequence:
    ### 1 - opens program (login screen)
    ### 2 - main window opens -> lands on create new
    ### 3 - navigate to Settings tab
    ### 4 - click Change Username button
    ### 5 - enter CORRECT password in verification popup
    ### 6 - clear username field (make it empty)
    ### 7 - click Update button
        # intentionally fails, should be handled gracefully
    ### 8 - verify error message shown
    ### 9 - verify app state unchanged
    ### 10 - verify can retry operation
"""


def test_e2e_fail_change_username_empty(app):
    """
    Test that changing username to empty string fails gracefully
    """
    # 1 - Login
    theme_manager = ThemeManager()
    login_screen = LoginScreen(theme_manager)
    login_screen.username_input.setText("user")
    login_screen.password_input.setText("asdf")
    login_screen.login_btn.click()
    assert current_user.get_username() == "user", "Expected to be able to login"

    # 2 - Open main window and go to Settings tab
    window = MainWindow()
    window.tabs.setCurrentIndex(4)  # Assuming Settings is tab 4
    settings_tab = window.settings_tab

    # Store original state
    original_username = settings_tab.current_username_input.text()
    original_button_text = settings_tab.change_username_btn.text()
    original_readonly = settings_tab.current_username_input.isReadOnly()

    # 3 - Prepare to intercept login dialog before clicking the button
    #    so that no real window opens during the test.
    from PyQt6.QtWidgets import QDialog

    # First, mock successful verification to get into edit mode
    with patch('ui.tabs.settings.LoginScreen') as mock_login_class:
        mock_login_instance = MagicMock()
        mock_login_class.return_value = mock_login_instance
        # simulate correct credentials by accepting the dialog
        mock_login_instance.exec.return_value = QDialog.DialogCode.Accepted

        # 4 - Click Change Username button (patched)
        settings_tab.change_username_btn.click()

    # Verify we're in edit mode
    assert settings_tab.current_username_input.isReadOnly() == False, "Username field should be editable"
    assert settings_tab.change_username_btn.text() == "Update", "Button should say Update"

    # 5 - Clear the username field (make it empty)
    settings_tab.current_username_input.setText("")

    # 6 - Click Update button and capture the warning
    with patch("ui.tabs.settings.QMessageBox.warning") as mock_warning:
        settings_tab.change_username_btn.click()

        # GRACEFUL HANDLING CHECKS:

        # 7 - Check that user was shown an error message
        assert mock_warning.called, "Should show error message to user"

        # 8 - Check the error message content
        if mock_warning.called:
            call_args = mock_warning.call_args[0]
            error_text = str(call_args)
            assert "empty" in error_text.lower() or "cannot be empty" in error_text.lower(), \
                   "Error message should mention empty username"

        # 9 - Check that app state didn't change (graceful recovery)
        assert settings_tab.current_username_input.text() == "", "Username field should still be empty"
        assert settings_tab.current_username_input.isReadOnly() == False, "Field should still be editable"
        assert settings_tab.change_username_btn.text() == "Update", "Button text should not change"

        # 10 - Check that user can try again (field still accessible)
        assert settings_tab.change_username_btn.isEnabled(), \
               "Button should still be enabled for retry"
    
    # 11 - Clean up - cancel edit mode
    settings_tab.cancel_username_update()