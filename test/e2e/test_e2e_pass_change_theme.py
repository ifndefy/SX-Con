from unittest.mock import patch

from PyQt6.QtWidgets import QApplication

from src.user import current_user

from ui.core.theme_manager import ThemeManager
from ui.prompts.login import LoginScreen
from ui.main_window import MainWindow
from ui.tabs.create_new import CreateNewTab
from ui.tabs.settings import SettingsTab

"""
sequence:
    ### 1 - Open Program
    ### 2 - Log In as User
    ### 3 - Land on Create New
    ### 4 - Navigate to the Settings Tab
    ### 5 - Change current theme
    ### 6 - Save the theme to preferences
    ### 7 - Change to another theme
    ### 8 - Load the saved theme
    ### 9 - Change back to the default theme
"""

def test_e2e_pass_change_theme(app):

    #1 open program

    theme_manager = ThemeManager()
    login_screen = LoginScreen(theme_manager)

    assert isinstance(login_screen, LoginScreen), "Make sure we open the login screen"
    assert login_screen.login_btn.isEnabled(), "Make sure the login button is enabled"
    assert login_screen.forgot_pw_btn.isEnabled(), "Make sure the forgot password button is enabled"

    #2 attempt to log in as a user

    login_screen.username_input.setText("user")
    login_screen.password_input.setText("asdf")

    login_screen.login_btn.click()

    assert current_user.get_username() == "user", "should be logged in as admin"

    #3 land on the main window

    window = MainWindow()
    assert isinstance(window.tabs.currentWidget(), CreateNewTab), "Make sure we land on the CreateNew tab"

    #4 nagivate to settings

    current_tab = window.settings_tab
    assert isinstance(current_tab, SettingsTab), "Make sure we land on the Settings tab"

    #5 change theme to something else

    assert current_tab.theme_dropdown_menu.isEnabled(), "Make sure we can change the theme"
    current_tab.theme_dropdown_menu.setCurrentIndex(1)

    assert current_tab.theme_dropdown_menu.currentText() == "CSUS", "We should have selected CSUS theme"

    #6 save the current theme to preferences
    with patch('ui.tabs.settings.QMessageBox.information'):
        current_tab.save_btn.click()

    #7 change the theme back to super

    assert current_tab.theme_dropdown_menu.isEnabled(), "Make sure we can keep changing"
    current_tab.theme_dropdown_menu.setCurrentIndex(0)
    
    assert current_tab.theme_dropdown_menu.currentText() == "Super", "We should have selected Super theme"

    #8 load theme from preferences
    with patch('ui.tabs.settings.QMessageBox.information'):
        current_tab.load_btn.click()

    assert current_tab.theme_dropdown_menu.currentText() == "CSUS", "Loading should have changed the theme to CSUS"

    #9 change preferences back to default

    current_tab.theme_dropdown_menu.setCurrentIndex(0)
    with patch('ui.tabs.settings.QMessageBox.information'):
        current_tab.save_btn.click()