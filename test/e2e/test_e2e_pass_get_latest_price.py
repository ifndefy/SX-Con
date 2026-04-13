from unittest.mock import patch
from src.user import current_user

from ui.main_window import MainWindow
from ui.prompts.login import LoginScreen
from ui.tabs.create_new import CreateNewTab
from ui.tabs.admin_settings import AdminSettingsTab
from ui.tabs.subtabs.products import ProductsTab as ProductsSubTab
from ui.core.theme_manager import ThemeManager

from services.delete_item import delete_item

import re
import random
import utils.logger.logger as log

"""
Sequence:
    ### 1 - opens program (login screen)
    ### 2 - main window opens -> lands on create new
    ### 3 - set/emit values into vendor and product fields, use a specific dummy PID
    ### 4 - click on create ticket
    ### 5 - Go to admin settings tab -> products
    ### 6 - Verify that product type is properly fetched on search 
    ### 7 - Verify that the latest price matches the most recent value added by the test
    ### 8 - Delete the consignment ticket that we created in testing
    ### 9 - Delete the product created at the dummy PID
"""

def test_e2e_pass_get_latest_price(app, monkeypatch, tmp_path):
    ### 1 - opens program (login screen)
    theme_manager = ThemeManager()
    login_screen = LoginScreen(theme_manager)

    # enter valid credentials
    login_screen.username_input.setText("admin") # real username
    login_screen.password_input.setText("asdf") # real password
    login_screen.login_btn.click() # calls attempt_login
    assert current_user != "user", "Expected to be set as current_user after successful login"

    ### 2 - main window opens -> lands on create new
    window = MainWindow()
    assert isinstance(window.tabs.currentWidget(), CreateNewTab), "Expected to land on CreateNewTab"

    ### 3 - set/emit values into vendor and product fields
    # shortcut the name
    current_tab = window.create_new_tab

    ## Init ticket list for later cleanup
    ticket_number = []
    latest_price = None

    ## generate some tickets
    ticket_number.append(current_tab.ticket_input.text().strip())

    # enter 1 into vendor_id field and then press enter to autopopulate
    current_tab.vendor_id_input.setText("1")
    current_tab.vendor_id_input.returnPressed.emit()

    prod_1_price = f"{10 * (random.randint(1, 10)):.2f}"
    prod_1_qty = str(1)

    current_tab.product_sections[0]['product_id'].setText('999')
    current_tab.product_sections[0]['product_id'].returnPressed.emit()
    current_tab.product_sections[0]['product_name'].setText('latest price test')
    current_tab.product_sections[0]['product_type'].setCurrentIndex(0)
    current_tab.product_sections[0]['price'].textEdited.emit(prod_1_price)
    current_tab.product_sections[0]['quantity'].setText(prod_1_qty)

    #Update latest price added
    latest_price = prod_1_price

    ###click on create record -> successful
    current_tab.create_btn.click()
    assert current_tab.vendor_id_input.text() == "", "Expected form to be cleared after successful record creation"

    assert latest_price != None, "Expected Latest ticket price to be captured"

    ### Move to Admin Settings
    window.tabs.setCurrentWidget(window.admin_settings_tab)
    current_tab = window.admin_settings_tab

    assert isinstance(window.tabs.currentWidget(), AdminSettingsTab), "Expected to land on AdminSettingsTab"

    ### Move into Products subtab
    current_tab.tabs.setCurrentWidget(current_tab.products_tab)
    current_subtab = current_tab.products_tab
    assert isinstance(current_tab.tabs.currentWidget() , ProductsSubTab), "Expected to land on AdminSettings -> Products"

    current_subtab.product_id_input.setText("999")
    ###Click the button to force build and search
    current_subtab.search_btn.click()

    assert current_subtab.products_layout.count() != 0, "Products section should not be empty"

    ###Retrieve the value from the qt layout manually because the self.products_section does not get updated properly
    tickets = []
    for i in range(current_subtab.products_layout.count()):
        item = current_subtab.products_layout.itemAt(i)
        widget = item.widget()
        if widget is not None:
            tickets.append(widget)

    assert len(tickets) == 1, "Products section should not return more than one product per ID"

    ticket_row_1 = tickets[0].layout().itemAt(0).layout()
    ticket_row_2 = tickets[0].layout().itemAt(1).layout()
    
    ticket_ID = ticket_row_1.itemAt(1).widget().text()
    ticket_latest_price = ticket_row_2.itemAt(7).widget().text()  

    ###Convert the string value to a usable float for comarison
    ticket_latest_price = float(re.sub(r'[^\d.]', '', ticket_latest_price))
    # log.info(ticket_latest_price)

    assert ticket_ID == "999", "Products subtab did not retrieve the correct value for the search"
    assert ticket_latest_price == float(latest_price), "Latest price field does not match latest entry"

    ###Cleanup Test Objects
    for i in ticket_number:
        assert delete_item("Consignments", "consignment", i) == 0, f"Failed to delete ticket num: {i}"

    assert delete_item("Entities", "product", 999) == 0, "Failed to clean-up test product with ID: 999"