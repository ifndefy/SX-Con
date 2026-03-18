import pytest
from unittest.mock import patch, MagicMock
import logging

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
    ### 5 - enter WRONG password in verification popup
        # intentionally fails, should be handled gracefully
    ### 6 - verify error message shown
    ### 7 - verify app state unchanged
    ### 8 - verify can retry operation
"""


def test_e2e_fail_settings_wrong_password_graceful(app):
    """
    Test that changing username with wrong password fails gracefully
    """
    # 1 - Login
    theme_manager = ThemeManager()
    login_screen = LoginScreen(theme_manager)
    login_screen.username_input.setText("user")
    login_screen.password_input.setText("asdf")
    login_screen.login_btn.click()
    assert current_user.get_username() == "user", "Login failed"

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

    with patch('ui.tabs.settings.LoginScreen') as mock_login_class, \
         patch("ui.tabs.settings.QMessageBox.warning") as mock_warning:
        mock_login_instance = MagicMock()
        mock_login_class.return_value = mock_login_instance
        # simulate wrong credentials by rejecting the dialog
        mock_login_instance.exec.return_value = QDialog.DialogCode.Rejected

        # 4 - Click Change Username button (patched)
        settings_tab.change_username_btn.click()

        # GRACEFUL HANDLING CHECKS:

        # 5a - Check that user was shown an error message
        assert mock_warning.called, "Should show error message to user"

        # 5b - Check the error message content
        if mock_warning.called:
            call_args = mock_warning.call_args[0]
            error_text = str(call_args)
            assert "Invalid credentials" in error_text or "Verification Failed" in error_text, \
                   "Error message should be user-friendly"

        # 5c - Check that app state didn't change (graceful recovery)
        assert settings_tab.current_username_input.text() == original_username, \
               "Username should not change"
        assert settings_tab.current_username_input.isReadOnly() == original_readonly, \
               "Field should remain read-only"
        assert settings_tab.change_username_btn.text() == original_button_text, \
               "Button text should not change"

        # 5d - Check that user can try again (field still accessible)
        assert settings_tab.change_username_btn.isEnabled(), \
               "Button should still be enabled for retry"