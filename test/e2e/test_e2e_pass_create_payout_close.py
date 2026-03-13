import pytest
from unittest.mock import MagicMock
from unittest.mock import patch
import os
import random

from src.user import current_user
from ui.core.theme_manager import ThemeManager
from ui.main_window import MainWindow
from ui.prompts.login import LoginScreen
from ui.tabs import VendorTicketsTab
from ui.tabs.create_new import CreateNewTab

from services.delete_item import delete_item
from utils.core.generate_pdf import PDF


"""
Sequence:
    ### 1 - opens program (login screen)
    ### 2 - main window opens -> lands on create new
    ### 3 - set/emit values into vendor and product fields
    ### 4 - clicks add product section button to add a fourth product
    ### 5 - clicks utility buttons (excel, pdf, don't click print --> tested outside already)
    ### 6 - click on create record -> successful
    ### 7 - Go to Vendor Tickets Tab
    ### 8 - search for vendor 1 tickets
    ### 9 - update sold values for each product
    ### 10 - Recalculate using payout's calculate button
    ### 11 - prints ticket -> emulate success
        # commented out
    ### 12 - clicks close ticket -> succeeds
    ### 13 - Delete the ticket
        # this is commented out to generate some data for the DB
"""


def test_e2e_create_payout_close(app):
    ### 1 - opens program (login screen)
    theme_manager = ThemeManager()
    login_screen = LoginScreen(theme_manager)

    # enter valid credentials
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

    ## Get the ticket number
    ticket_number = current_tab.ticket_input.text().strip()

    # enter 1 into vendor_id field and then press enter to autopopulate
    current_tab.vendor_id_input.setText("1")
    current_tab.vendor_id_input.returnPressed.emit()

    ## generate some prices and quantities
    prod_1_price = str(random.randint(299, 1099))
    prod_1_qty = str(random.randint(1, 50))
    prod_2_price = str(random.randint(299, 1099))
    prod_2_qty = str(random.randint(1, 50))
    prod_3_price = str(random.randint(299, 1099))
    prod_3_qty = str(random.randint(1, 50))
    prod_4_price = str(random.randint(299, 1099))
    prod_4_qty = str(random.randint(1, 50))

    # enter 1 into product_id field 0 and press enter to autopopulate
    current_tab.product_sections[0]['product_id'].setText('1')
    current_tab.product_sections[0]['product_id'].returnPressed.emit()
    current_tab.product_sections[0]['notes'].setText('e2e test - jxl')
    current_tab.product_sections[0]['price'].textEdited.emit(prod_1_price) # this becomes 100.00
    current_tab.product_sections[0]['quantity'].setText(prod_1_qty)

    current_tab.product_sections[1]['product_id'].setText('2')
    current_tab.product_sections[1]['product_id'].returnPressed.emit()
    current_tab.product_sections[1]['notes'].setText('e2e test - jxl')
    current_tab.product_sections[1]['price'].textEdited.emit(prod_2_price)
    current_tab.product_sections[1]['quantity'].setText(prod_2_qty)

    current_tab.product_sections[2]['product_id'].setText('3')
    current_tab.product_sections[2]['product_id'].returnPressed.emit()
    current_tab.product_sections[2]['notes'].setText('e2e test - jxl')
    current_tab.product_sections[2]['price'].textEdited.emit(prod_3_price)
    current_tab.product_sections[2]['quantity'].setText(prod_3_qty)

    ### 4 - clicks add product section button to add a fourth product
    current_tab.add_product_btn.click()
    current_tab.product_sections[3]['product_id'].setText('4')
    current_tab.product_sections[3]['product_id'].returnPressed.emit()
    current_tab.product_sections[3]['notes'].setText('e2e test - jxl')
    current_tab.product_sections[3]['price'].textEdited.emit(prod_4_price)
    current_tab.product_sections[3]['quantity'].setText(prod_4_qty)

    ### 5 - clicks utility buttons (excel, pdf, don't click print --> tested outside already)
    output_path = os.path.join(os.path.dirname(__file__), "test_e2e_jxl.xlsx")
    with patch("utils.core.generate_excel.QFileDialog.getSaveFileName",
               return_value=(output_path, "Excel File (*.xlsx)")):
        current_tab.excel_btn.click()
    assert os.path.exists(output_path), f"Expected excel file to be created at {output_path}"
    os.remove(output_path)

    pdf_output = os.path.join(os.path.dirname(__file__), "e2e_test.pdf")
    def set_pdf_filename(self):
        self.pdf_filename = pdf_output

    with patch.object(PDF, "set_pdf_filename", set_pdf_filename), \
            patch('ui.tabs.create_new.QMessageBox.information') :
        current_tab.pdf_btn.click()

    assert os.path.exists(pdf_output), "Expected PDF to be generated"
    os.remove(pdf_output)

    # not testing print functionality, it will print every time the test runs
    # current_tab.print_btn.click() # uncomment this line if you want to see if print actually works

    ### 6 - click on create record -> successful
    current_tab.create_btn.click()
    assert current_tab.vendor_id_input.text() == "", "Expected form to be cleared after successful record creation"

    ### 7 - Go to Vendor Tickets Tab
    window.tabs.setCurrentIndex(1)
    assert isinstance(window.tabs.currentWidget(), VendorTicketsTab), "Expected to move into VendorTicketsTab"

    ### 8 - search for vendor 1 tickets
    current_tab = window.vendor_tickets_tab
    current_tab.vendor_id_input.textChanged.emit("1") # this tab is on text changed
    current_tab.search_btn.click()

    # check if the latest ticket actually exists
    assert current_tab.tickets_section[0]['ticket_num'].text() == ticket_number, "Expected to see the created ticket here"

    ### 9 - update sold values for each product
    ## does not test the buttons, that is already being done in another test
    current_tab.tickets_section[0]['view_btn'].click()
    open_view_ticket = current_tab.tickets_section[0]['view_ticket']

    ## generate some sold_qty values
    prod_1_sold_qty = str(random.randint(1, int(prod_1_qty)))
    prod_2_sold_qty = str(random.randint(1, int(prod_2_qty)))
    prod_3_sold_qty = str(random.randint(1, int(prod_3_qty)))
    prod_4_sold_qty = str(random.randint(1, int(prod_4_qty)))

    open_view_ticket.product_widgets[0]['sold_edit'].setText(prod_1_sold_qty) # the widget index is used
    open_view_ticket.product_widgets[0]['update_btn'].click()

    open_view_ticket.product_widgets[1]['sold_edit'].setText(prod_2_sold_qty)
    open_view_ticket.product_widgets[1]['update_btn'].click()

    open_view_ticket.product_widgets[2]['sold_edit'].setText(prod_3_sold_qty)
    open_view_ticket.product_widgets[2]['update_btn'].click()

    open_view_ticket.product_widgets[3]['sold_edit'].setText(prod_4_sold_qty)
    open_view_ticket.product_widgets[3]['update_btn'].click()

    ### 10 - Recalculate using payout's calculate button
    open_view_ticket.payout_widget.calc_btn.click()
    # don't need to test if the out is correct, it is being tested elsewhere
    assert open_view_ticket.payout_widget.vendor_input.text() != "$0.00", "Expected Vendor's payout to not be zero"
    assert open_view_ticket.payout_widget.super_x_input.text() != "$0.00", "Expected SuperX's payout to not be zero"

    ### 11 - prints ticket -> emulate success
    ## uncomment to see that it worked
    # current_tab.tickets_section[0]['print_btn'].click()

    ### 12 - clicks close ticket -> succeeds
    with patch('ui.tabs.vendor_tickets.QMessageBox.information') :
        current_tab.tickets_section[0]['close_btn'].click()
    assert current_tab.tickets_section[0]['status'].text() == "CLOSED", "Expected ticket to be closed"

    ### 13 - Delete the ticket
    # result = delete_item("Consignments", "consignment", ticket_number)
    # assert result == 0, "Failed to delete created item"