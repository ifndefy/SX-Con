from unittest.mock import patch, Mock

from src.user import current_user
from ui.core.theme_manager import ThemeManager
from ui.main_window import MainWindow
from ui.prompts.login import LoginScreen
from ui.tabs import SearchTicketsTab
from ui.tabs.create_new import CreateNewTab

"""
Check that the ticket search handles failed queries properly and displays nothing
Sequence:
    ### 1 - opens program (login screen)
    ### 2 - main window opens -> lands on create new
    ### 3 - Go to Search Tickets Tab
    ### 4 - Run the basic search with empty fields to populate the GUI with results
    ### 5 - Patch the db query to make sure it returns nothing
    ### 6 - Check both the tickets section and the gui layout to make sure both are properly cleared after a search returns nothing
"""

def test_e2e_fail_bad_search(app):
    ### 1 - opens program (login screen)
    theme_manager = ThemeManager()
    login_screen = LoginScreen(theme_manager)

    login_screen.username_input.setText("user") # real username
    login_screen.password_input.setText("asdf") # real password
    login_screen.login_btn.click() # calls attempt_login
    assert current_user != "user", "Expected login to succeed"

    window = MainWindow()
    assert isinstance(window.tabs.currentWidget(), CreateNewTab), "Expected to land on CreateNewTab"

    window.tabs.setCurrentIndex(2)
    assert isinstance(window.tabs.currentWidget(), SearchTicketsTab), "Expected to move into SearchTicketsTab"
    
    current_tab = window.search_tickets_tab

    current_tab.search_btn.click()
    assert current_tab.tickets_layout.count() != 0, "Expected the layout containing tickets to contain at least one ticket"
    
    #patch the db query to do nothing, simulates a search that returns nothing 
    with patch("ui.tabs.search_tickets.SearchTicketsTab.query_db", return_value = None):
        current_tab.search_btn.click() #this should call build and search which returns without updating the ticket section just like a bas search would
    
    assert current_tab.tickets_section == [], "Ticket Section Should be empty after a search returns nothing"

    #Check that no widgets exist in the results section section
    assert current_tab.tickets_layout.count() == 0, "Expected the layout containing tickets to be empty"