from unittest.mock import patch
from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QDialog
from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtWidgets import QComboBox

from src.user import current_user
from ui.core.theme_manager import ThemeManager
from ui.main_window import MainWindow
from ui.prompts.login import LoginScreen
from ui.tabs.admin_settings import AdminSettingsTab
from ui.tabs.create_new import CreateNewTab
from ui.tabs.subtabs.users import UsersTab
from ui.tabs.subtabs.vendors import VendorsTab
from ui.tabs.subtabs.products import ProductsTab

from services.delete_item import delete_item
from services.get_item_by_property import get_item_by_property


def test_e2e_create_user(app):
    ### 1 - opens program (login screen)
    theme_manager = ThemeManager()
    login_screen = LoginScreen(theme_manager)

    # enter valid credentials
    login_screen.username_input.setText("admin")  # real username
    login_screen.password_input.setText("asdf")  # real password
    login_screen.login_btn.click()  # calls attempt_login
    assert current_user != "user", "Expected to be set as current_user after successful login"

    ### 2 - main window opens -> lands on create new
    window = MainWindow()
    assert isinstance(window.tabs.currentWidget(), CreateNewTab), "Expected to land on CreateNewTab"
    assert window.tabs.count() == 5, "Expected to find 5 tabs with admin login"

    ### 3 - Switch to Admin Tab
    window.tabs.setCurrentIndex(4)  # 4 is admin tab
    assert isinstance(window.tabs.currentWidget(), AdminSettingsTab), "Expected to land on AdminSettingsTab"
    assert isinstance(window.tabs.currentWidget().tabs.currentWidget(), UsersTab), "Expected to find Users tab"
    tab = window.tabs.currentWidget().tabs.currentWidget()

    #### 4 - def method to schedule value passing into exec dialog
    stored_username = "fakeusertest"

    def populate_dialog():
        create_user_dialog = tab.findChild(QDialog)
        create_user_dialog.findChild(QLineEdit, "username_input").setText(stored_username)
        create_user_dialog.findChild(QLineEdit, "first_name_input").setText("fake")
        create_user_dialog.findChild(QLineEdit, "last_name_input").setText("user")
        create_user_dialog.findChild(QLineEdit, "password_input").setText("asdf")
        create_user_dialog.findChild(QComboBox, "question1").setCurrentIndex(0)
        create_user_dialog.findChild(QLineEdit, "response1").setText("asdf")
        create_user_dialog.findChild(QComboBox, "question2").setCurrentIndex(1)
        create_user_dialog.findChild(QLineEdit, "response2").setText("asdf")
        create_user_dialog.findChild(QComboBox, "admin_question").setCurrentIndex(1)
        create_user_dialog.accept()

    ### 5 - Click the button
    # this has to go right before the click action to prevent it from being called by another event
    with patch("ui.tabs.subtabs.users.QMessageBox"):
        # QTimer schedule has to go right before the click to prevent another event from triggering it
        QTimer.singleShot(0, populate_dialog)
        tab.create_btn.click()

    assert tab.new_user_data != -1, f"Failed to create user {stored_username}. new_user_data is -1"
    res = get_item_by_property("Entities", "user", "username", stored_username)
    assert not res is None, f"Expected to have created user: {stored_username}"
    assert res.get('username') == stored_username, f"Expected to have created user: {stored_username}"

    delete_item("Entities", "user", res.get('user_id'))

def test_e2e_create_vendor(app):
    ### 1 - opens program (login screen)
    theme_manager = ThemeManager()
    login_screen = LoginScreen(theme_manager)

    # enter valid credentials
    login_screen.username_input.setText("admin")  # real username
    login_screen.password_input.setText("asdf")  # real password
    login_screen.login_btn.click()  # calls attempt_login
    assert current_user != "user", "Expected to be set as current_user after successful login"

    ### 2 - main window opens -> lands on create new
    window = MainWindow()
    assert isinstance(window.tabs.currentWidget(), CreateNewTab), "Expected to land on CreateNewTab"
    assert window.tabs.count() == 5, "Expected to find 5 tabs with admin login"

    ### 3 - Switch to Admin Tab
    window.tabs.setCurrentIndex(4)  # 4 is admin tab
    assert isinstance(window.tabs.currentWidget(), AdminSettingsTab), "Expected to land on AdminSettingsTab"
    assert isinstance(window.tabs.currentWidget().tabs.currentWidget(), UsersTab), "Expected to landn on Users tab"

    ### 4 - Switch to Vendors subtab
    window.tabs.currentWidget().tabs.setCurrentIndex(1)
    assert isinstance(window.tabs.currentWidget().tabs.currentWidget(), VendorsTab), "Expected to have switched to Vendors tab"
    tab = window.tabs.currentWidget().tabs.currentWidget()

    ### 5 - def method to schedule value passing into exec dialog
    stored_vendor_id = 9992

    def populate_dialog():
        create_vendor_dialog = tab.findChild(QDialog)
        create_vendor_dialog.findChild(QLineEdit, "vendor_id_input").setText(str(stored_vendor_id))
        create_vendor_dialog.findChild(QLineEdit, "phone_number_input").setText("123-123-1234")
        create_vendor_dialog.findChild(QLineEdit, "first_name_input").setText("fake")
        create_vendor_dialog.findChild(QLineEdit, "middle_name_input").setText("asdf")
        create_vendor_dialog.findChild(QLineEdit, "last_name_input").setText("vendor")
        create_vendor_dialog.findChild(QLineEdit, "address_input").setText("asdf")
        create_vendor_dialog.findChild(QLineEdit, "city_input").setText("asdf")
        create_vendor_dialog.findChild(QLineEdit, "state_input").setText("AS")
        create_vendor_dialog.findChild(QLineEdit, "zip_code_input").setText("12345")
        create_vendor_dialog.accept()

    ### 6 - Click the button
    with patch("ui.tabs.subtabs.vendors.QMessageBox"):
        # QTimer schedule has to go right before the click to prevent another event from triggering it
        QTimer.singleShot(0, populate_dialog)
        tab.create_btn.click()

    assert tab.new_vendor_data != -1, f"Failed to create vendor with id {stored_vendor_id}. new_vendor_data is -1"
    res = get_item_by_property("Entities", "vendor", "vendor_id", stored_vendor_id)
    assert not res is None, f"Expected to have created vendor: {stored_vendor_id}"
    assert res.get('vendor_id') == stored_vendor_id, f"Expected to have created vendor: {stored_vendor_id}"

    delete_item("Entities", "vendor", res.get('vendor_id'))

def test_e2e_create_product(app):
    ### 1 - opens program (login screen)
    theme_manager = ThemeManager()
    login_screen = LoginScreen(theme_manager)

    # enter valid credentials
    login_screen.username_input.setText("admin")  # real username
    login_screen.password_input.setText("asdf")  # real password
    login_screen.login_btn.click()  # calls attempt_login
    assert current_user != "user", "Expected to be set as current_user after successful login"

    ### 2 - main window opens -> lands on create new
    window = MainWindow()
    assert isinstance(window.tabs.currentWidget(), CreateNewTab), "Expected to land on CreateNewTab"
    assert window.tabs.count() == 5, "Expected to find 5 tabs with admin login"

    ### 3 - Switch to Admin Tab
    window.tabs.setCurrentIndex(4)  # 4 is admin tab
    assert isinstance(window.tabs.currentWidget(), AdminSettingsTab), "Expected to land on AdminSettingsTab"
    assert isinstance(window.tabs.currentWidget().tabs.currentWidget(), UsersTab), "Expected to find Users tab"
    tab = window.tabs.currentWidget().tabs.currentWidget()

    ### 4 - Switch to Vendors subtab
    window.tabs.currentWidget().tabs.setCurrentIndex(2)
    assert isinstance(window.tabs.currentWidget().tabs.currentWidget(), ProductsTab), "Expected to have switched to Products tab"
    tab = window.tabs.currentWidget().tabs.currentWidget()

    ### 5 - def method to schedule value passing into exec dialog
    stored_product_id = 9992

    def populate_dialog():
        create_product_dialog = tab.findChild(QDialog)
        create_product_dialog.findChild(QLineEdit, "product_id_input").setText(str(stored_product_id))
        create_product_dialog.findChild(QLineEdit, "product_name_input").setText("alsdjfk")
        create_product_dialog.findChild(QComboBox, "product_type_input").setCurrentIndex(1)
        create_product_dialog.accept()

    ### 6 - Click the button
    with patch("ui.tabs.subtabs.products.QMessageBox"):
        # QTimer schedule has to go right before the click to prevent another event from triggering it
        QTimer.singleShot(0, populate_dialog)
        tab.create_btn.click()

    assert tab.new_product_data != -1, f"Failed to create product with id {stored_product_id}. new_product_data is -1"
    res = get_item_by_property("Entities", "product", "product_id", int(stored_product_id))
    assert not res is None, f"Expected to have created product: {stored_product_id}"
    assert res.get('product_id') == stored_product_id, f"Expected to have created product: {stored_product_id}"
    delete_item("Entities", "product", res.get('product_id'))
