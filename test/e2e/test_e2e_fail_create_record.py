from unittest.mock import patch

from src.user import current_user
from ui.core.theme_manager import ThemeManager
from ui.main_window import MainWindow
from ui.prompts.login import LoginScreen

"""
Sequence:
    1 - opens program (login screen)
    2 - main window opens -> lands on create new
    3 - populate required vendor and product fields
    4 - patch record creation to fail
    5 - click create record
    6 - verify failure handled gracefully
    7 - verify form state unchanged
"""


def test_e2e_create_record_fail_graceful(app):
    # 1 - Login
    theme_manager = ThemeManager()
    login_screen = LoginScreen(theme_manager)
    login_screen.username_input.setText("user")
    login_screen.password_input.setText("asdf")
    login_screen.login_btn.click()
    assert current_user.get_username() == "user", "Login failed"

    # 2 - Open main window and get Create New tab
    window = MainWindow()
    create_tab = window.create_new_tab

    # 3 - Fill required vendor fields
    create_tab.vendor_id_input.setText("1234")
    create_tab.phone_input.setText("1234567890")
    create_tab.first_name_input.setText("Test")
    create_tab.middle_name_input.setText("A")
    create_tab.last_name_input.setText("User")
    create_tab.address_input.setText("123 Test St")
    create_tab.city_input.setText("Sacramento")
    create_tab.state_input.setText("CA")
    create_tab.zip_input.setText("12345")

    # 4 - Fill first product line with valid data
    product = create_tab.product_sections[0]
    product["product_id"].setText("54321")
    product["product_type"].setCurrentText("General")
    product["product_name"].setText("Widget")
    product["price"].setText("10")
    product["quantity"].setText("2")

    # Let rate/total/revenue update through normal UI flow
    create_tab.calc_btn.click()

    # 5 - Capture state before failure
    original_vendor_id = create_tab.vendor_id_input.text()
    original_product_id = product["product_id"].text()
    original_product_name = product["product_name"].text()
    original_product_count = len(create_tab.product_sections)
    original_button_enabled = create_tab.create_btn.isEnabled()

    # 6 - Force backend failure at the chosen endpoint
    with patch.object(create_tab, "_post_to_database", return_value=-1):
        create_tab.create_btn.click()

        # 7 - Graceful failure checks:
        # form should NOT clear on failed create
        assert create_tab.vendor_id_input.text() == original_vendor_id
        assert create_tab.product_sections[0]["product_id"].text() == original_product_id
        assert create_tab.product_sections[0]["product_name"].text() == original_product_name
        assert len(create_tab.product_sections) == original_product_count

        # user should still be able to retry
        assert create_tab.create_btn.isEnabled() == original_button_enabled
        assert create_tab.create_btn.isEnabled()