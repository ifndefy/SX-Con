from unittest.mock import patch
from src.user import current_user
from ui.core.theme_manager import ThemeManager
from ui.main_window import MainWindow
from ui.prompts.login import LoginScreen
from ui.tabs import VendorTicketsTab
from ui.tabs.create_new import CreateNewTab


"""
Sequence:
    1 - opens program (login screen)
    2 - main window opens -> lands on create new
    3 - populate valid vendor and product fields
    4 - click create record -> successful
    5 - verify form clears after successful create
    6 - go to Vendor Tickets tab
    7 - search for vendor tickets
    8 - verify created ticket appears
"""


def test_e2e_fetch_ticket(app):
    # 1 - opens program (login screen)
    theme_manager = ThemeManager()
    login_screen = LoginScreen(theme_manager)

    login_screen.username_input.setText("user")
    login_screen.password_input.setText("asdf")
    login_screen.login_btn.click()

    assert current_user.get_username() == "user", "Login failed"

    # 2 - main window opens -> lands on create new
    window = MainWindow()
    assert isinstance(window.tabs.currentWidget(), CreateNewTab), "Expected to land on CreateNewTab"

    current_tab = window.create_new_tab

    # 3 - populate valid vendor and product fields
    ticket_number = current_tab.ticket_input.text().strip()

    current_tab.vendor_id_input.setText("1")
    current_tab.vendor_id_input.returnPressed.emit()

    current_tab.product_sections[0]["product_id"].setText("1")
    current_tab.product_sections[0]["product_id"].returnPressed.emit()
    current_tab.product_sections[0]["notes"].setText("e2e fetch ticket test")
    current_tab.product_sections[0]["price"].textEdited.emit("100")
    current_tab.product_sections[0]["quantity"].setText("2")

    # 4 - click create record -> successful
    with patch.object(current_tab, 'on_print_clicked'):
        current_tab.create_btn.click()

    # 5 - verify form clears after successful create
    assert current_tab.vendor_id_input.text() == "", "Expected form to be cleared after successful record creation"

    # 6 - go to Vendor Tickets tab
    window.tabs.setCurrentIndex(1)
    assert isinstance(window.tabs.currentWidget(), VendorTicketsTab), "Expected to move into VendorTicketsTab"

    current_tab = window.vendor_tickets_tab

    # 7 - search for vendor tickets
    current_tab.vendor_id_input.textChanged.emit("1")
    current_tab.search_btn.click()

    # 8 - verify created ticket appears
    assert current_tab.tickets_section[0]["ticket_num"].text() == ticket_number, \
        "Expected to find the created ticket in VendorTicketsTab"