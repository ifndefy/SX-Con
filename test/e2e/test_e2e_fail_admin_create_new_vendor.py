from unittest.mock import patch, MagicMock
from PyQt6.QtWidgets import QLineEdit, QDialog, QVBoxLayout
from ui.core.theme_manager import ThemeManager
from ui.main_window import MainWindow
from ui.prompts.login import LoginScreen
from src.user import current_user
from ui.tabs.create_new import CreateNewTab
from ui.tabs.admin_settings import AdminSettingsTab
from ui.tabs.subtabs.vendors import VendorsTab

from ui.core import format_state
"""
Sequence:
    ### 1 - open program (login screen)
    ### 2 - main window opens -> lands on create new
    ### 3 - click on admin settings
    ### 4 - click on admin vendor settings
    ### 5 - create dialog
    ### 6 - click on create new vendor
    ### 7 - run the dialog through the create new vendor -> fail
"""

def test_e2e_fail_admin_create_new_vendor(app):
    with patch('ui.tabs.subtabs.vendors.VendorsTab.create_new_vendor_prompt') as mock_create_new_vendor:
        # 1 - open program (login screen)
        theme_manager = ThemeManager()
        login_screen = LoginScreen(theme_manager)

        login_screen.username_input.setText("admin")
        login_screen.password_input.setText("asdf")
        login_screen.login_btn.click()
        assert current_user != "user", "Expected to be set as current_user after successful login"

        # 2 - main window opens -> lands on create new
        window = MainWindow()
        assert isinstance(window.tabs.currentWidget(), CreateNewTab), "Expected to land on CreateNewTab"

        # 3 - click on admin settings
        window.tabs.setCurrentWidget(window.admin_settings_tab)
        admin = window.admin_settings_tab
        assert isinstance(window.tabs.currentWidget(), AdminSettingsTab), "Expected to land on AdminSettingsTab"

        # 4 - click on admin vendor settings
        admin.tabs.setCurrentWidget(admin.vendors_tab)
        vendor = admin.vendors_tab
        assert isinstance(admin.tabs.currentWidget(), VendorsTab), "Expected to land on AdminSettingsTab"

        # 5 - create dialog
        dialog = QDialog()
        layout = QVBoxLayout(dialog)

        first_name_input = QLineEdit()
        first_name_input.setObjectName("first_name_input")
        layout.addWidget(first_name_input)
        first_name_input.setText('')

        middle_name_input = QLineEdit()
        middle_name_input.setObjectName("middle_name_input")
        layout.addWidget(middle_name_input)
        middle_name_input.setText('')

        last_name_input = QLineEdit()
        last_name_input.setObjectName("last_name_input")
        layout.addWidget(last_name_input)
        last_name_input.setText('')

        address_input = QLineEdit()
        address_input.setObjectName("address_input")
        layout.addWidget(address_input)
        address_input.setText('')

        city_input = QLineEdit()
        city_input.setObjectName("city_input")
        layout.addWidget(city_input)
        city_input.setText('')

        state_input = format_state.FormatState()
        layout.addWidget(state_input)
        state_input.setText('')

        zip_code_input = QLineEdit()
        zip_code_input.setObjectName("zip_code_input")
        layout.addWidget(zip_code_input)
        zip_code_input.setText('')

        # 6 - click on create new vendor (should only run once)
        vendor.create_btn.click()
        mock_create_new_vendor.assert_called_once()

        # 7 - run the dialog through the create new vendor -> fail
        assert not (vendor.on_create_clicked(dialog))()



