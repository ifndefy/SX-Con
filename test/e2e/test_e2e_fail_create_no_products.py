from unittest.mock import patch, Mock

from src.user import current_user
from ui.core.theme_manager import ThemeManager
from ui.main_window import MainWindow
from ui.prompts.login import LoginScreen
from ui.tabs import SearchTicketsTab
from ui.tabs.create_new import CreateNewTab

from services.delete_item import delete_item

"""
Check that the ticket creation handles incomplete forms gracefully, and that nothing is added to the DB when a form does not contain any valid products
Sequence:
    ### 1 - opens program (login screen)
    ### 2 - main window opens -> lands on create new
    ### 3 - set/emit values to autofill vendor fields
    ### 4 - Leave products empty
    ### 4 - emulate calculate press 
    ### 6 - check calculate fields -> expect fail
    ### 6 - click on create record -> expect fail no products
    ### 7 - Go to Vendor Tickets Tab
    ### 8 - search for ticket number -> should return nothing for that ticket number
"""

def test_e2e_fail_create_no_products(app):
    ### 1 - opens program (login screen)
    theme_manager = ThemeManager()
    login_screen = LoginScreen(theme_manager)

    login_screen.username_input.setText("user") # real username
    login_screen.password_input.setText("asdf") # real password
    login_screen.login_btn.click() # calls attempt_login
    assert current_user != "user", "Expected to be set as current_user after successful login"

    ### 2 - main window opens -> lands on create new
    window = MainWindow()
    assert isinstance(window.tabs.currentWidget(), CreateNewTab), "Expected to land on CreateNewTab"

    ### 3 - set/emit values into vendor and product fields
    # shortcut the name
    current_tab = window.create_new_tab

    ## Get the ticket number for later check
    ticket_number = current_tab.ticket_input.text().strip()

    ## Try to create an entirely empty ticket -> should fail
    current_tab.create_btn.click()
    assert window.status_label.text() == "Invalid Vendor ID", "Expected the program to report that No vendor data has been filled"

    # enter 1 into vendor_id field and then press enter to autopopulate
    current_tab.vendor_id_input.setText("1")
    current_tab.vendor_id_input.returnPressed.emit()

    #for state checking, check what's been passed to the status bar
    ### 4 - Emulate calculate press
    current_tab.calc_btn.click()
    assert window.status_label.text() == "No products to calculate", "Expected program to refuse to calculate when no products are present"

    ### 6 - click on create record -> expect failure with different message
    current_tab.create_btn.click()
    assert window.status_label.text() == "All product sections are empty", "Expected the program to report that no products exist in ticket"
    
    ### 7 - Go to Search Tab
    window.tabs.setCurrentIndex(2)
    assert isinstance(window.tabs.currentWidget(), SearchTicketsTab), "Expected to move into SearchTicketsTab"

    ### 8 - search for ticket_number ticket
    current_tab = window.search_tickets_tab
    current_tab.ticket_number_input.setText(f"{ticket_number}")
    current_tab.ticket_number_input.textChanged.emit(f"{ticket_number}") # this tab is on text changed
    current_tab.search_btn.click()

    # Ensure that the ticket does not exist in database
    try:
        assert window.status_label.text() == "No tickets found", "Expected no tickets to be reported here"
    except AssertionError as e:
        #On the off-chance we do have something pushed to the database
        result = delete_item("Consignments", "consignment", ticket_number)

        #if we also fail to delete, then panic
        assert result == 0, "Error in delete_item found, test clean-up for test_e2e_fail_create_no_products has failed"
        
        #re-raise our error to fail the test
        raise e
