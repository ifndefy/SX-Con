from PyQt6.QtWidgets import QApplication

from src.user import current_user
from ui.core.theme_manager import ThemeManager
from ui.main_window import MainWindow
from ui.prompts.login import LoginScreen

from ui.tabs.create_new import CreateNewTab
from ui.tabs.settings import SettingsTab
from ui.prompts.security_dialog import SecurityQuestionsDialog


"""
Sequence:
    ### 1 - Opens program (login screen)
    ### 2 - Main window opens -> lands on create new
    ### 3 - Navigate to Settings tab
    ### 4 - Click "Change Q/A" button
    ### 5 - Log in with valid user credentials
    ### 6 - Enter invalid Security Questions
        # (Choosing the same security question twice is not allowed)
    ### 7 - Verify error message shown 
    ### 8 - Verify app state unchanged
    ### 9 - Verify user can retry operation
"""

from unittest.mock import patch


def test_e2e_fail_change_security_q_a(app):
    ### 1 - Opens program (login screen)
    theme_manager = ThemeManager()
    login_screen = LoginScreen(theme_manager)

    login_screen.username_input.setText("user")
    login_screen.password_input.setText("asdf")
    login_screen.login_btn.click()

    assert current_user != "user", "Expected to be set as current_user after successful login"

    ### 2 - Main window opens -> lands on create new
    window = MainWindow()
    assert isinstance(window.tabs.currentWidget(), CreateNewTab), "Expected to land on CreateNewTab"

    ### 3 - Navigate to Settings Tab
    settings_tab = window.settings_tab
    assert isinstance(settings_tab, SettingsTab), "Expected to open SettingsTab"

    original_username = settings_tab.current_username_input.text()
    original_button_text = settings_tab.change_qa_btn.text()
    original_readonly = settings_tab.current_username_input.isReadOnly()
    original_tab_name = settings_tab.tab_name


    with patch.object(settings_tab, "verify_credentials_for_cred_change"), \
        patch("ui.tabs.settings.QMessageBox.critical") as mock_warning, \
        patch('ui.tabs.settings.QMessageBox.warning') as mock_login_warning, \
        patch("ui.tabs.settings.SecurityQuestionsDialog.exec"):


            ### 4 - Click "Change Q/A" button
            settings_tab.change_qa_btn.click()
            QApplication.processEvents()

            login_dialog = None
            security_dialog = None
            for w in QApplication.topLevelWidgets():
                if isinstance(w, LoginScreen):
                    login_dialog = w
                if isinstance(w, SecurityQuestionsDialog):
                    security_dialog = w

            assert isinstance(login_dialog, LoginScreen), "Expected login dialog to appear"


            ### 5 - Log in with valid user credentials
            login_dialog.username_input.setText("user")
            login_dialog.password_input.setText("asdf")
            login_dialog.login_btn.click()
            QApplication.processEvents()

            assert not mock_login_warning.called, "Expected no warning for valid user credentials"
            assert security_dialog is not None, "Expected security dialog to appear"


            ### 6 - Enter invalid Security Questions
            security_dialog.question1_combo.setCurrentIndex(1)
            security_dialog.answer1_input.setText("Answer 1")

            security_dialog.question2_combo.setCurrentIndex(1)
            security_dialog.answer2_input.setText("Answer 2")

            security_dialog.update_btn.click()
            QApplication.processEvents()


            ### 7 - Verify error message shown
            assert mock_warning.called, "Expected warning message to display for duplicate security questions"


            ### 8 - Verify app state unchanged
            assert settings_tab.current_username_input.text() == original_username, "Expected username to remain unchanged"
            assert settings_tab.current_username_input.isReadOnly() == original_readonly, "Expected username to remain read only"
            assert settings_tab.change_qa_btn.text() == original_button_text, "Expected 'Change Q/A' button text to remain unchanged"
            assert settings_tab.tab_name == original_tab_name, "Expected settings tab name to remain unchanged"
            assert settings_tab.change_qa_btn.isEnabled(), "Expected 'Change Q/A' button to remain enabled"
            assert isinstance(window.tabs.currentWidget(), CreateNewTab), "Expected to remain on the Create New tab"


            ### 9 - Verify user can retry operation
            security_dialog.cancel_btn.click()
            QApplication.processEvents()

            settings_tab.change_qa_btn.click()
            QApplication.processEvents()

            login_dialog_found = any(
                isinstance(w, LoginScreen)
                for w in QApplication.topLevelWidgets()
            )
            assert login_dialog_found, "Expected for user to be able to retry the change security q/a flow"
