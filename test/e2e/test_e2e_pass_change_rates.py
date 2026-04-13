import pandas as pd

from unittest.mock import patch

from src.user import current_user
from ui.core.theme_manager import ThemeManager
from ui.main_window import MainWindow
from ui.prompts.login import LoginScreen
from ui.tabs import AdminSettingsTab, SearchTicketsTab
from ui.tabs.create_new import CreateNewTab
from ui.tabs.subtabs.rates import CRTab
from services.delete_item import delete_item

from utils import parse_consignment_table as c_table

"""
    Sequence:
    ### 1 - open program
    ### 2 - main window opens -> lands on create new
    ### 3 - click on admin settings
    ### 4 - click on admin rates
    ### 5 - change all three values 
        # cold food: 5%
        # hot food: 10%
        # general food: 15%
    ### 6 - click on create new tab
    ### 7 - set/emit values into vendor and product fields
    ### 8 - click on create record -> successful
    ### 9 - click on search ticket tab
    ### 10 - search up the newest ticket
    ### 11 - check on the ticket to see if rates match or not
    ### 12 - delete ticket
    ### 13 - click on admin settings
    ### 14 - click on admin rates
    ### 15 - change back the three values
"""

def test_e2e_pass_change_rates(app):
    ### 1 - open program
    theme_manager = ThemeManager()
    login_screen = LoginScreen(theme_manager)

    login_screen.username_input.setText('admin')
    login_screen.password_input.setText('asdf')
    login_screen.login_btn.click()
    assert current_user != "user", "Expected to be set as current_user after successful login"

    ### 2 - main window opens -> lands on create new
    window = MainWindow()
    assert isinstance(window.tabs.currentWidget(), CreateNewTab), "Expected to land on CreateNewTab"

    # 3 - click on admin settings
    window.tabs.setCurrentWidget(window.admin_settings_tab)
    admin = window.admin_settings_tab
    assert isinstance(window.tabs.currentWidget(), AdminSettingsTab), "Expected to land on AdminSettingsTab"

    ### 4 - click on admin rates
    admin.tabs.setCurrentWidget(admin.cr_tab)
    rates = admin.cr_tab
    assert isinstance(admin.tabs.currentWidget(), CRTab), "Expected to land on RatesTab"

    ### 5 - change all three values
    df = pd.read_csv('./src/SPOT_CR.csv')
    df = df.set_index('Type')
    entry_list = c_table.fetch_consignment_data()
    old_value = dict()
    for key, value in entry_list.items():
        old_value.update({key: value})
        if key == 'Hot Food':
            df.loc[key, 'Rate'] = int(5)
        elif key == 'General':
            df.loc[key, 'Rate'] = int(10)
        elif key == 'Produce':
            df.loc[key, 'Rate'] = int(15)
    df.to_csv('./src/SPOT_CR.csv')

    ### 6 - click on create new tab
    window.tabs.setCurrentWidget(window.create_new_tab)
    assert isinstance(window.tabs.currentWidget(), CreateNewTab), "Expected to land CreateNewTab"
    create_new = window.create_new_tab

    ### 7 - set/emit values into vendor and product fields

    ticket_number = create_new.ticket_input.text().strip()

    create_new.vendor_id_input.setText("1")
    create_new.vendor_id_input.returnPressed.emit()

    prod_price = '$100.00'
    prod_qty = str(1)

    create_new.product_sections[0]['product_id'].setText('1')
    create_new.product_sections[0]['product_id'].returnPressed.emit()
    create_new.product_sections[0]['product_type'].setCurrentIndex(0)
    create_new.product_sections[0]['price'].textEdited.emit(prod_price)
    create_new.product_sections[0]['quantity'].setText(prod_qty)

    create_new.product_sections[1]['product_id'].setText('2')
    create_new.product_sections[1]['product_id'].returnPressed.emit()
    create_new.product_sections[1]['product_type'].setCurrentIndex(1)
    create_new.product_sections[1]['price'].textEdited.emit(prod_price)
    create_new.product_sections[1]['quantity'].setText(prod_qty)

    create_new.product_sections[2]['product_id'].setText('3')
    create_new.product_sections[2]['product_id'].returnPressed.emit()
    create_new.product_sections[2]['product_type'].setCurrentIndex(2)
    create_new.product_sections[2]['price'].textEdited.emit(prod_price)
    create_new.product_sections[2]['quantity'].setText(prod_qty)

    ### 8 - click on create record -> successful
    create_new.create_btn.click()
    assert create_new.vendor_id_input.text() == "", "Expected form to be cleared after successful record creation"

    ### 9 - click on search ticket tab
    window.tabs.setCurrentWidget(window.search_tickets_tab)
    assert isinstance(window.tabs.currentWidget(), SearchTicketsTab), "Expected to land on SearchTicketsTab"
    search_tickets = window.search_tickets_tab

    ### 10 - search up the newest ticket
    search_tickets.ticket_number_input.setText(ticket_number)
    search_tickets.search_btn.click()


    ### 11 - check on the ticket to see if rates match or not
    search_tickets.tickets_section[0]['view_btn'].click()
    open_view_ticket = search_tickets.tickets_section[0]['view_ticket']

    prod_sold_qty = str(1)
    open_view_ticket.product_widgets[0]['sold_edit'].setText(prod_sold_qty)  # the widget index is used
    with patch("ui.core.view_ticket.QMessageBox"), \
            patch("ui.core.revenue_payout.QMessageBox"):
        open_view_ticket.product_widgets[0]['update_btn'].click()

    open_view_ticket.product_widgets[1]['sold_edit'].setText(prod_sold_qty)
    with patch("ui.core.view_ticket.QMessageBox"), \
            patch("ui.core.revenue_payout.QMessageBox"):
        open_view_ticket.product_widgets[1]['update_btn'].click()

    open_view_ticket.product_widgets[2]['sold_edit'].setText(prod_sold_qty)
    with patch("ui.core.view_ticket.QMessageBox"), \
            patch("ui.core.revenue_payout.QMessageBox"):
        open_view_ticket.product_widgets[2]['update_btn'].click()

    with patch("ui.core.view_ticket.QMessageBox"), \
            patch("ui.core.revenue_payout.QMessageBox"):
        open_view_ticket.payout_widget.calc_btn.click()

    assert open_view_ticket.payout_widget.vendor_input.text() == "$270.00"
    assert open_view_ticket.rev_by_type.revenue_records[0]['total_edit'].text() == "$95.00"
    assert open_view_ticket.rev_by_type.revenue_records[1]['total_edit'].text() == "$90.00"
    assert open_view_ticket.rev_by_type.revenue_records[2]['total_edit'].text() == "$85.00"

    ### 12 - Delete the ticket
    result = delete_item("Consignments", "consignment", ticket_number)
    assert result == 0, "Failed to delete created item"

    ### 13 - click on admin settings
    window.tabs.setCurrentWidget(window.admin_settings_tab)
    admin = window.admin_settings_tab
    assert isinstance(window.tabs.currentWidget(), AdminSettingsTab), "Expected to land on AdminSettingsTab"

    ### 14 - click on admin rates
    admin.tabs.setCurrentWidget(admin.cr_tab)
    rates = admin.cr_tab
    assert isinstance(admin.tabs.currentWidget(), CRTab), "Expected to land on RatesTab"

    ### 15 - change back the three values
    df = pd.read_csv('./src/SPOT_CR.csv')
    df = df.set_index('Type')
    entry_list = c_table.fetch_consignment_data()
    for key, value in entry_list.items():
        if key == 'Hot Food':
            df.loc[key, 'Rate'] = old_value[key]
        elif key == 'General':
            df.loc[key, 'Rate'] = old_value[key]
        elif key == 'Produce':
            df.loc[key, 'Rate'] = old_value[key]
    df.to_csv('./src/SPOT_CR.csv')