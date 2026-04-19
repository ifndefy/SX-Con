import os
import pytest
import re
from PyQt6.QtCore import Qt
from PyQt6.QtTest import QTest
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtWidgets import QPushButton
from unittest.mock import patch

from handlers.api_handler import APIHandler
from services.connect_database import db_connection
from services.insert_item import insert_item
from services.delete_item import delete_item
from ui.core.autogen_date import generate_host_datetime
from ui.tabs.subtabs.records import RecordsTab
from utils.core.generate_pdf import PDF

@pytest.fixture
def test_consignment(records_tab):
    ticket_number = 99999
    consignment = {
        'consignment_id': ticket_number,
        'vendor_id': 1,
        'entity_type': 'consignment',
        'datetime': str(generate_host_datetime()),
        'status': 'OPEN',
        'products': [
            {
                'product_id': 1,
                'product_type': 'General',
                'product_name': 'Test Product',
                'notes': 'test',
                'rate': 30,
                'price': 10.00,
                'quantity': 10,
                'sold': 0,
                'remaining': 10,
            }
        ],
        'revenue': {
            'shared': [{'vendor': 100.00, 'super_x': 50.00}],
            'grouped': [],
            'payout': [],
            'accumulated': {}
        }
    }
    insert_item('Consignments', 'consignment', consignment)
    yield ticket_number
    delete_item('Consignments', 'consignment', ticket_number)

@pytest.fixture
def records_tab(app):
    api = APIHandler()
    yield RecordsTab(api, db_connection)

def test_ticket_number(records_tab):
    """
    :Purpose: verifies that the ticket number field only takes integers and results in a successful query
    :Author(s): Joe Lee
    """
    tab = records_tab
    assert tab.ticket_number_input is not None, 'Expected Ticket Number field to exist'
    QTest.keyClicks(tab.ticket_number_input, 'abc3./') # don't put commas
    assert tab.ticket_number_input.text() == '3', 'Expected only integers to be accepted'
    QTest.qWait(400)
    assert len(tab.records_section) == 1, 'Expected only one ticket for ticket number: 1'

def test_datetime_input(records_tab):
    """
    :Purpose: verifies that the datetime field has no constraints and results in a successful query
    :Author(s): Joe Lee
    """
    tab = records_tab
    assert tab.datetime_input is not None, 'Expected Datetime Input to exist'
    QTest.keyClicks(tab.datetime_input, 'asdf./')
    assert tab.datetime_input.text().strip() == 'asdf./', 'Expected no input constraints'
    assert len(tab.records_section) == 0, "Expected no tickets for datetime 'asdf./'"
    tab.datetime_input.clear()
    QTest.keyClicks(tab.datetime_input, '04/18/asdf')
    assert tab.datetime_input.text().strip() == '04/18/asdf', 'Expected no input constraints'
    tab.datetime_input.clear()
    QTest.keyClicks(tab.datetime_input, '04/18')
    assert tab.datetime_input.text().strip() == '04/18', 'Expected no input constraints'
    QTest.qWait(400)
    assert len(tab.records_section) > 0, 'Expected ticket(s) for datetime 04/18'

def test_u_id_input(records_tab):
    """
    :Purpose: verifies that the user id field only accepts integers and results in a successful query
    :Author(s): Joe Lee
    """
    tab = records_tab
    assert tab.user_id_input is not None, 'Expected User ID Input to exist'
    QTest.keyClicks(tab.user_id_input, 'asdf./')
    assert tab.user_id_input.text().strip() == '', 'Expected constraints to reject all input characters'
    assert len(tab.records_section) == 0, "Expected no tickets for invalid user_id input 'asdf./' as it should not trigger a query"
    tab.user_id_input.clear()
    QTest.keyClicks(tab.user_id_input, '2./asdf')
    assert tab.user_id_input.text().strip() == '2', "Expected constraints to only accept '2'"
    QTest.qWait(400)
    assert len(tab.records_section) > 0, 'Expected ticket(s) for user id 2'

def test_v_id_input(records_tab):
    """
    :Purpose: verifies that the vendor id field only accepts integers and results in a successful query
    :Author(s): Joe Lee
    """
    tab = records_tab
    assert tab.vendor_id_input is not None, 'Expected Vendor ID Input to exist'
    QTest.keyClicks(tab.vendor_id_input, 'asdf./')
    assert tab.vendor_id_input.text().strip() == '', 'Expected constraints to reject all input characters'
    assert len(tab.records_section) == 0, "Expected no tickets for invalid vendor id input 'asdf./' as it should not trigger a query"
    tab.vendor_id_input.clear()
    QTest.keyClicks(tab.vendor_id_input, '1./asdf')
    assert tab.vendor_id_input.text().strip() == '1', "Expected constraints to only accept '1'"
    QTest.qWait(400)
    assert len(tab.records_section) > 0, "Expected ticket(s) for user id '1'"

def test_p_id_input(records_tab):
    """
    :Purpose: verifies that the product id field only accepts integers and results in a successful query
    :Author(s): Joe Lee
    """
    tab = records_tab
    assert tab.product_id_input is not None, 'Expected Product ID Input to exist'
    QTest.keyClicks(tab.product_id_input, 'asdf./')
    assert tab.product_id_input.text().strip() == '', 'Expected constraints to reject all input characters'
    assert len(tab.records_section) == 0, "Expected no tickets for invalid product id input 'asdf./' as it should not trigger a query"
    tab.product_id_input.clear()
    QTest.keyClicks(tab.product_id_input, '1./asdf')
    assert tab.product_id_input.text().strip() == '1', "Expected constraints to only accept '1'"
    QTest.qWait(400)
    assert len(tab.records_section) > 0, "Expected ticket(s) for product id '1'"

def test_status_input(records_tab):
    """
    :Purpose: verifies that the status field only takes integers and results in a successful query
    :Author(s): Joe Lee
    """
    tab = records_tab
    assert tab.status_input is not None, 'Expected Status Input to exist'
    tab.status_input.setCurrentIndex(0)
    assert tab.status_input.currentText() == 'OPEN', "Expected index 0 to be 'OPEN'"
    QTest.qWait(400)
    assert len(tab.records_section) > 0, 'Expected ticket sections for status: OPEN'
    tab.status_input.setCurrentIndex(1)
    assert tab.status_input.currentText() == 'CLOSED', "Expected index 1 to be 'CLOSED'"
    QTest.qWait(400)
    assert len(tab.records_section) > 0, 'Expected ticket sections for status: CLOSED'

def test_btns_exist(records_tab):
    """
    :Purpose: verifies that the clear and search buttons exist
    :Author(s): Joe Lee
    """
    tab = records_tab
    assert tab.clear_btn is not None, 'Expected clear_btn to exist'
    assert tab.search_btn is not None, 'Expected search_btn to exist'

def test_records_section(records_tab):
    """
    :Purpose: verifies that a query result's ticket contains the coded display fields with their respective constraints
    :Author(s): Joe Lee
    """
    tab = records_tab
    QTest.keyClicks(tab.ticket_number_input, 'abc3./') # don't put commas
    assert tab.ticket_number_input.text() == '3', 'Expected only integers to be accepted'
    QTest.qWait(400)
    assert len(tab.records_section) > 0, 'Expected ticket sections for vendor ID: 1'

    assert tab.records_section[0]['ticket_num'] is not None, 'Expected ticket number field to exist in ticket section'
    assert tab.records_section[0]['ticket_num'].isReadOnly(), 'Expected ticket number field to be read only'
    assert isinstance(int(tab.records_section[0]['ticket_num'].text()), int), 'Expected ticket number field to be an integer value'
    assert tab.records_section[0]['datetime'] is not None, 'Expected datetime field to exist in ticket section'
    assert tab.records_section[0]['datetime'].isReadOnly(), 'Expected datetime field to be read only'
    assert re.match(r'\d{2}/\d{2}/\d{2} -- \d{2}:\d{2} (AM|PM)', tab.records_section[0]['datetime'].text()), "Expected datetime field to have format 'MM\\DD\\YY -- %I:%M %p"
    assert tab.records_section[0]['status'] is not None, 'Expected status field to exist for ticket section'
    assert tab.records_section[0]['status'].isReadOnly(), 'Expected status field to be read only'
    assert re.match(r'(OPEN|CLOSED)', tab.records_section[0]['status'].text()), "Expected status field to be either 'OPEN' or 'CLOSED'"
    assert tab.records_section[0]['view_btn'] is not None, 'Expected View button to exist in product section'
    assert tab.records_section[0]['excel_btn'] is not None, 'Expected Excel button to exist in product section'
    assert tab.records_section[0]['pdf_btn'] is not None, 'Expected PDF button to exist in product section'
    assert tab.records_section[0]['print_btn'] is not None, 'Expected Print button to exist in product section'

    status = tab.records_section[0]['status'].text().strip()
    if status == 'OPEN':
        assert not tab.records_section[0]['close_btn'].isHidden()
        assert tab.records_section[0]['open_btn'].isHidden()
    elif status == 'CLOSED':
        assert not tab.records_section[0]['open_btn'].isHidden()
        assert tab.records_section[0]['close_btn'].isHidden()

def test_view_btn(records_tab):
    """
    :Purpose: verifies that a query result's ticket's view button executes successfully
    :Author(s): Joe Lee
    """
    tab = records_tab
    QTest.keyClicks(tab.ticket_number_input, '3')
    QTest.qWait(400)
    tab.setAttribute(Qt.WidgetAttribute.WA_DontShowOnScreen)
    tab.show()
    tab.records_section[0]['view_btn'].click()
    assert not tab.records_section[0]['details_container'].isHidden()
    assert tab.records_section[0]['view_btn'].text() == 'Hide'
    tab.records_section[0]['view_btn'].click()
    assert tab.records_section[0]['details_container'].isHidden()
    assert tab.records_section[0]['view_btn'].text() == 'View'

def test_open_close_btns(records_tab):
    """
    :Purpose: verifies that a query result's ticket's open or close button executes successfully
    :Author(s): Joe Lee
    """
    tab = records_tab
    QTest.keyClicks(tab.ticket_number_input, '3')
    QTest.qWait(400)

    status = tab.records_section[0]['status'].text().strip()

    if status == 'OPEN':
        with patch('ui.tabs.subtabs.records.QMessageBox.information'):
            tab.records_section[0]['close_btn'].click()
        assert tab.records_section[0]['status'].text().strip() == 'CLOSED'
        assert not tab.records_section[0]['open_btn'].isHidden()
        assert tab.records_section[0]['close_btn'].isHidden()

        with patch('ui.tabs.subtabs.records.QMessageBox.information'):
            tab.records_section[0]['open_btn'].click()
        assert tab.records_section[0]['status'].text().strip() == 'OPEN'
        assert not tab.records_section[0]['close_btn'].isHidden()
        assert tab.records_section[0]['open_btn'].isHidden()

    elif status == 'CLOSED':
        with patch('ui.tabs.subtabs.records.QMessageBox.information'):
            tab.records_section[0]['open_btn'].click()
        assert tab.records_section[0]['status'].text().strip() == 'OPEN'
        assert not tab.records_section[0]['close_btn'].isHidden()
        assert tab.records_section[0]['open_btn'].isHidden()

        with patch('ui.tabs.subtabs.records.QMessageBox.information'):
            tab.records_section[0]['close_btn'].click()
        assert tab.records_section[0]['status'].text().strip() == 'CLOSED'
        assert not tab.records_section[0]['open_btn'].isHidden()
        assert tab.records_section[0]['close_btn'].isHidden()

def test_pdf_btn(records_tab):
    """
    :Purpose: verifies that a query result's ticket's pdf button executes successfully
    :Author(s): Joe Lee
    """
    tab = records_tab
    QTest.keyClicks(tab.ticket_number_input, '3')
    QTest.qWait(400)

    pdf_output = os.path.join(os.path.dirname(__file__), 'test_pdf_btn.pdf')

    def set_pdf_filename(self):
        self.pdf_filename = pdf_output

    with patch.object(PDF, 'set_pdf_filename', set_pdf_filename), \
            patch('ui.tabs.subtabs.records.QMessageBox.information'):
        tab.records_section[0]['pdf_btn'].click()

    assert os.path.exists(pdf_output), 'Expected PDF to be generated'
    os.remove(pdf_output)

def test_print_btn(records_tab):
    """
    :Purpose: verifies that a query result's ticket's print button can execute, physically printing has been patched out
    :Author(s): Joe Lee
    """
    tab = records_tab
    QTest.keyClicks(tab.ticket_number_input, '3')
    QTest.qWait(400)
    with patch('ui.tabs.subtabs.records.handler_print'), \
            patch('ui.tabs.subtabs.records.QMessageBox.information'):
        tab.records_section[0]['print_btn'].click()

def test_excel_btn(records_tab):
    """
    :Purpose: verifies that a query result's ticket's excel button executes successfully
    :Author(s): Joe Lee
    """
    tab = records_tab
    QTest.keyClicks(tab.ticket_number_input, '3')
    QTest.qWait(400)
    output_path = os.path.join(os.path.dirname(__file__), 'test_excel_btn.xlsx')
    with patch('utils.core.generate_excel.QFileDialog.getSaveFileName',
               return_value=(output_path, 'Excel File (*.xlsx)')):
        tab.records_section[0]['excel_btn'].click()
    assert os.path.exists(output_path), 'Expected Excel file to be generated'
    os.remove(output_path)

def test_view_btn_details(records_tab):
    """
    :Purpose: verifies that a query result's ticket's view section displays the appropriate details
    :Author(s): Joe Lee
    """
    tab = records_tab
    QTest.keyClicks(tab.ticket_number_input, '3')
    QTest.qWait(400)
    tab.setAttribute(Qt.WidgetAttribute.WA_DontShowOnScreen)
    tab.show()
    tab.records_section[0]['view_btn'].click()

    ticket_number = tab.records_section[0]['ticket_num'].text().strip()
    ticket_details = tab.view(ticket_number)
    expected_products = 0
    for product in ticket_details['ticket_data']['products']:
        if product.get('product_id') and product.get('product_id') != 'NULL':
            expected_products += 1

    view_ticket = tab.records_section[0]['view_ticket']
    assert len(view_ticket.product_widgets) == expected_products, f'Expected {expected_products} product sections'

    for idx in range(expected_products):
        widgets = view_ticket.product_widgets[idx]
        assert widgets['sold_edit'] is not None, f'Expected sold_edit for product {idx}'
        assert widgets['remaining_display'] is not None, f'Expected remaining_display for product {idx}'
        assert widgets['remaining_display'].isReadOnly(), f'Expected remaining_display to be read only for product {idx}'
        assert widgets['quantity_display'] is not None, f'Expected quantity_display for product {idx}'
        assert widgets['quantity_display'].isReadOnly(), f'Expected quantity_display to be read only for product {idx}'
        assert widgets['sold_display'] is not None, f'Expected sold_display for product {idx}'
        assert widgets['sold_display'].isReadOnly(), f'Expected sold_display to be read only for product {idx}'
        assert widgets['update_btn'] is not None, f'Expected update_btn for product {idx}'
        assert widgets['product_name'] is not None, f'Expected product_name for product {idx}'

    quantity = int(view_ticket.product_widgets[0]['quantity_display'].text())
    view_ticket.product_widgets[0]['sold_edit'].clear()
    QTest.keyClicks(view_ticket.product_widgets[0]['sold_edit'], str(quantity))
    assert view_ticket.product_widgets[0]['sold_edit'].text() == str(quantity), 'Expected sold field to accept quantity signed value'

def test_view_btn_accumulated_payout(records_tab):
    """
    :Purpose: verifies that a query result's ticket's view section displays the accumulated payout widget
    :Author(s): Joe Lee
    """
    tab = records_tab
    QTest.keyClicks(tab.ticket_number_input, '3')
    QTest.qWait(400)
    tab.setAttribute(Qt.WidgetAttribute.WA_DontShowOnScreen)
    tab.show()
    tab.records_section[0]['view_btn'].click()

    view_ticket = tab.records_section[0]['view_ticket']
    accumulated = view_ticket.accumulated_widget

    assert accumulated is not None, 'Expected accumulated payout widget to exist'
    assert accumulated.signed_vendor is not None, 'Expected signed vendor field to exist'
    assert accumulated.signed_vendor.isReadOnly(), 'Expected signed vendor field to be read only'
    assert accumulated.signed_super_x is not None, 'Expected signed super x field to exist'
    assert accumulated.signed_super_x.isReadOnly(), 'Expected signed super x field to be read only'
    assert accumulated.accumulated_vendor is not None, 'Expected accumulated vendor field to exist'
    assert accumulated.accumulated_vendor.isReadOnly(), 'Expected accumulated vendor field to be read only'
    assert accumulated.accumulated_super_x is not None, 'Expected accumulated super x field to exist'
    assert accumulated.accumulated_super_x.isReadOnly(), 'Expected accumulated super x field to be read only'
    assert accumulated.remaining_vendor is not None, 'Expected remaining vendor field to exist'
    assert accumulated.remaining_vendor.isReadOnly(), 'Expected remaining vendor field to be read only'
    assert accumulated.remaining_super_x is not None, 'Expected remaining super x field to exist'
    assert accumulated.remaining_super_x.isReadOnly(), 'Expected remaining super x field to be read only'

def test_view_btn_revenue_by_type(records_tab):
    """
    :Purpose: verifies that a query result's ticket's view section displays the revenue by type widget
    :Author(s): Joe Lee
    """
    tab = records_tab
    QTest.keyClicks(tab.ticket_number_input, '3')
    QTest.qWait(400)
    tab.setAttribute(Qt.WidgetAttribute.WA_DontShowOnScreen)
    tab.show()
    tab.records_section[0]['view_btn'].click()

    view_ticket = tab.records_section[0]['view_ticket']
    rev_by_type = view_ticket.rev_by_type

    assert rev_by_type is not None, 'Expected revenue by product type widget to exist'
    assert len(rev_by_type.revenue_records) == 4, 'Expected 4 product type rows (Hot Food, General, Produce, Total)'

    expected_types = ['Hot Food', 'General', 'Produce', 'Total']
    for idx, record in enumerate(rev_by_type.revenue_records):
        assert record['type_label'] is not None, f'Expected type label for row {idx}'
        assert record['total_edit'] is not None, f'Expected total field for row {idx}'
        assert record['product_type'] == expected_types[idx], f'Expected product type {expected_types[idx]} at row {idx}'

def test_view_btn_revenue_payout(records_tab):
    """
    :Purpose: verifies that a query result's ticket's view section displays the payout widget
    :Author(s): Joe Lee
    """
    tab = records_tab
    QTest.keyClicks(tab.ticket_number_input, '3')
    QTest.qWait(400)
    tab.setAttribute(Qt.WidgetAttribute.WA_DontShowOnScreen)
    tab.show()
    tab.records_section[0]['view_btn'].click()

    view_ticket = tab.records_section[0]['view_ticket']
    payout = view_ticket.payout_widget

    assert payout is not None, 'Expected payout widget to exist'
    assert payout.vendor_input is not None, 'Expected vendor input to exist'
    assert payout.super_x_input is not None, 'Expected super x input to exist'
    assert payout.calc_btn is not None, 'Expected calculate button to exist'
    assert payout.payout_btn is not None, 'Expected payout button to exist'
    assert payout.history_btn is not None, 'Expected history button to exist'

def test_view_ticket_btn_states(records_tab):
    """
    :Purpose: verifies that a query result's ticket's view section buttons change states based on ticket status
    :Author(s): Joe Lee
    """
    tab = records_tab
    QTest.keyClicks(tab.ticket_number_input, '3')
    QTest.qWait(400)
    tab.setAttribute(Qt.WidgetAttribute.WA_DontShowOnScreen)
    tab.show()

    status = tab.records_section[0]['status'].text().strip()
    if status == 'OPEN':
        with patch('ui.tabs.subtabs.records.QMessageBox.information'):
            tab.records_section[0]['close_btn'].click()

    tab.records_section[0]['view_btn'].click()
    view_ticket = tab.records_section[0]['view_ticket']
    payout = view_ticket.payout_widget

    for idx, widgets in view_ticket.product_widgets.items():
        assert not widgets['update_btn'].isEnabled(), f'Expected update_btn to be locked for product {idx}'
    assert not payout.calc_btn.isEnabled(), 'Expected calc_btn to be locked'
    assert not payout.payout_btn.isEnabled(), 'Expected payout_btn to be locked'

    tab.records_section[0]['view_btn'].click()
    with patch('ui.tabs.subtabs.records.QMessageBox.information'):
        tab.records_section[0]['open_btn'].click()

    tab.records_section[0]['view_btn'].click()
    view_ticket = tab.records_section[0]['view_ticket']
    payout = view_ticket.payout_widget

    for idx, widgets in view_ticket.product_widgets.items():
        assert widgets['update_btn'].isEnabled(), f'Expected update_btn to be enabled for product {idx}'
    assert payout.calc_btn.isEnabled(), 'Expected calc_btn to be enabled'
    assert payout.payout_btn.isEnabled(), 'Expected payout_btn to be enabled'

def test_view_btn_revenue_payout_btns(records_tab, test_consignment):
    """
    :Purpose: verifies that the payout widget's buttons work using a fixture ticket to guarantee that there is a ticket to update
    :Author(s): Joe Lee
    """
    tab = records_tab
    QTest.keyClicks(tab.ticket_number_input, '99999')
    QTest.qWait(400)
    tab.setAttribute(Qt.WidgetAttribute.WA_DontShowOnScreen)
    tab.show()

    target_section = None
    for section in tab.records_section:
        if section['ticket_num'].text().strip() == str(test_consignment):
            section['view_btn'].click()
            target_section = section
            break

    assert target_section is not None, 'Expected test consignment to appear in results'
    view_ticket = target_section['view_ticket']
    payout = view_ticket.payout_widget

    view_ticket.product_widgets[0]['sold_edit'].clear()
    view_ticket.product_widgets[0]['sold_edit'].setText('5')
    with patch('ui.core.view_ticket.QMessageBox'), \
            patch('ui.core.revenue_payout.QMessageBox'):
        view_ticket.product_widgets[0]['update_btn'].click()

    assert payout.vendor_input.text() != '$0.00', 'Expected vendor payout to be calculated'
    assert payout.super_x_input.text() != '$0.00', 'Expected super x payout to be calculated'

    confirm_payout = QMessageBox.StandardButton.Yes
    with patch('ui.core.revenue_payout.current_user') as mock_user:
        mock_user.get_username.return_value = 'test'
        mock_user.get_user_full_name.return_value = 'Test User'
        with patch('ui.core.revenue_payout.QMessageBox.question', return_value=confirm_payout), \
                patch('ui.core.revenue_payout.QMessageBox.information'), \
                patch('ui.core.revenue_payout.QMessageBox.warning'):
            payout.payout_btn.click()

    assert payout.vendor_input.text() == '$0.00', 'Expected vendor payout to reset after commit'
    assert payout.super_x_input.text() == '$0.00', 'Expected super x payout to reset after commit'

def test_view_btn_revenue_payout_history_btn(records_tab):
    """
    :Purpose: verifies that a query result's ticket's view section's payout section's history button opens a dialog
    :Author(s): Joe Lee
    """
    tab = records_tab
    QTest.keyClicks(tab.ticket_number_input, '3')
    QTest.qWait(400)
    tab.setAttribute(Qt.WidgetAttribute.WA_DontShowOnScreen)
    tab.show()
    tab.records_section[0]['view_btn'].click()
    payout = tab.records_section[0]['view_ticket'].payout_widget
    payout.history_btn.click()
    dialog = payout.history_dialog
    assert dialog is not None, 'Expected history dialog to exist'
    assert len(dialog.payout_list) == len(payout.payout_list), 'Expected dialog to have same payout count'
    dialog.close()

def test_view_payout_history_cards_exist(records_tab):
    """
    :Purpose: verifies that history dialog contains payout cards
    :Author(s): Joe Lee
    """
    tab = records_tab
    QTest.keyClicks(tab.ticket_number_input, '3')
    QTest.qWait(400)
    tab.setAttribute(Qt.WidgetAttribute.WA_DontShowOnScreen)
    tab.show()
    tab.records_section[0]['view_btn'].click()
    payout = tab.records_section[0]['view_ticket'].payout_widget
    payout.history_btn.click()
    dialog = payout.history_dialog
    layout = dialog.layout()
    assert layout.count() > 0, 'Expected at least one card in the dialog'
    dialog.close()

def test_view_payout_history_card_toggle(records_tab):
    """
    :Purpose: verifies that history dialog view button executes successfully
    :Author(s): Joe Lee
    """
    tab = records_tab
    QTest.keyClicks(tab.ticket_number_input, '3')
    QTest.qWait(400)
    tab.setAttribute(Qt.WidgetAttribute.WA_DontShowOnScreen)
    tab.show()
    tab.records_section[0]['view_btn'].click()
    payout = tab.records_section[0]['view_ticket'].payout_widget
    payout.history_btn.click()
    dialog = payout.history_dialog
    card = dialog.layout().itemAt(0).widget()
    expand_btn = None
    for i in range(card.layout().count()):
        item = card.layout().itemAt(i)
        if item and item.layout():
            top_layout = item.layout()
            for j in range(top_layout.count()):
                widget = top_layout.itemAt(j).widget()
                if isinstance(widget, QPushButton) and widget.text() == 'View':
                    expand_btn = widget
                    break
    assert expand_btn is not None, 'Expected expand button to exist'
    details = card.layout().itemAt(1).widget()
    assert details.isHidden(), 'Expected details to be hidden initially'
    expand_btn.click()
    assert not details.isHidden(), 'Expected details to be visible after clicking View'
    assert expand_btn.text() == 'Hide', 'Expected button text to change to Hide'
    expand_btn.click()
    assert details.isHidden(), 'Expected details to be hidden after clicking Hide'
    assert expand_btn.text() == 'View', 'Expected button text to change back to View'
    dialog.close()

def test_view_payout_history_card_content(records_tab):
    """
    :Purpose: verifies that payout cards contain the appropriate details
    :Author(s): Joe Lee
    """
    tab = records_tab
    QTest.keyClicks(tab.ticket_number_input, '3')
    QTest.qWait(400)
    tab.setAttribute(Qt.WidgetAttribute.WA_DontShowOnScreen)
    tab.show()
    tab.records_section[0]['view_btn'].click()
    payout = tab.records_section[0]['view_ticket'].payout_widget
    payout.history_btn.click()
    dialog = payout.history_dialog
    card = dialog.layout().itemAt(0).widget()
    expand_btn = None
    details = card.layout().itemAt(1).widget()
    for i in range(card.layout().count()):
        item = card.layout().itemAt(i)
        if item and item.layout():
            top_layout = item.layout()
            for j in range(top_layout.count()):
                widget = top_layout.itemAt(j).widget()
                if isinstance(widget, QPushButton) and widget.text() == 'View':
                    expand_btn = widget
                    break
    expand_btn.click()
    details_layout = details.layout()
    found_excel = found_pdf = found_print = False
    for i in range(details_layout.count()):
        item = details_layout.itemAt(i)
        if item and item.layout():
            for j in range(item.layout().count()):
                widget = item.layout().itemAt(j).widget()
                if isinstance(widget, QPushButton):
                    if widget.text() == 'Excel':
                        found_excel = True
                    elif widget.text() == 'PDF':
                        found_pdf = True
                    elif widget.text() == 'Print':
                        found_print = True
    assert found_excel, 'Expected Excel button in card'
    assert found_pdf, 'Expected PDF button in card'
    assert found_print, 'Expected Print button in card'
    dialog.close()

def test_view_payout_history_pdf_btn(records_tab):
    """
    :Purpose: verifies that payout card's pdf button executes successfully
    :Author(s): Joe Lee
    """
    tab = records_tab
    QTest.keyClicks(tab.ticket_number_input, '3')
    QTest.qWait(400)
    tab.setAttribute(Qt.WidgetAttribute.WA_DontShowOnScreen)
    tab.show()
    tab.records_section[0]['view_btn'].click()
    payout = tab.records_section[0]['view_ticket'].payout_widget
    payout.history_btn.click()
    dialog = payout.history_dialog
    card = dialog.layout().itemAt(0).widget()
    expand_btn = None
    details = card.layout().itemAt(1).widget()
    for i in range(card.layout().count()):
        item = card.layout().itemAt(i)
        if item and item.layout():
            top_layout = item.layout()
            for j in range(top_layout.count()):
                widget = top_layout.itemAt(j).widget()
                if isinstance(widget, QPushButton) and widget.text() == 'View':
                    expand_btn = widget
                    break
    expand_btn.click()
    pdf_btn = None
    for i in range(details.layout().count()):
        item = details.layout().itemAt(i)
        if item and item.layout():
            for j in range(item.layout().count()):
                widget = item.layout().itemAt(j).widget()
                if isinstance(widget, QPushButton) and widget.text() == 'PDF':
                    pdf_btn = widget
                    break
    with patch('ui.prompts.view_history.handler_db_pdf') as mock_pdf, \
            patch('ui.prompts.view_history.QMessageBox.information'):
        pdf_btn.click()
    mock_pdf.assert_called_once()
    dialog.close()

def test_view_payout_history_print_btn(records_tab):
    """
    :Purpose: verifies that payout card's print button can execute
    :Author(s): Joe Lee
    """
    tab = records_tab
    QTest.keyClicks(tab.ticket_number_input, '3')
    QTest.qWait(400)
    tab.setAttribute(Qt.WidgetAttribute.WA_DontShowOnScreen)
    tab.show()
    tab.records_section[0]['view_btn'].click()
    payout = tab.records_section[0]['view_ticket'].payout_widget
    payout.history_btn.click()
    dialog = payout.history_dialog
    card = dialog.layout().itemAt(0).widget()
    expand_btn = None
    details = card.layout().itemAt(1).widget()
    for i in range(card.layout().count()):
        item = card.layout().itemAt(i)
        if item and item.layout():
            top_layout = item.layout()
            for j in range(top_layout.count()):
                widget = top_layout.itemAt(j).widget()
                if isinstance(widget, QPushButton) and widget.text() == 'View':
                    expand_btn = widget
                    break
    expand_btn.click()
    print_btn = None
    for i in range(details.layout().count()):
        item = details.layout().itemAt(i)
        if item and item.layout():
            for j in range(item.layout().count()):
                widget = item.layout().itemAt(j).widget()
                if isinstance(widget, QPushButton) and widget.text() == 'Print':
                    print_btn = widget
                    break
    with patch('ui.prompts.view_history.handler_db_pdf'), \
            patch('ui.prompts.view_history.handler_print'), \
            patch('ui.prompts.view_history.QMessageBox.information'):
        print_btn.click()
    dialog.close()

def test_view_payout_history_excel_btn(records_tab):
    """
    :Purpose: verifies that payout card's excel button executes successfully
    :Author(s): Joe Lee
    """
    tab = records_tab
    QTest.keyClicks(tab.ticket_number_input, '3')
    QTest.qWait(400)
    tab.setAttribute(Qt.WidgetAttribute.WA_DontShowOnScreen)
    tab.show()
    tab.records_section[0]['view_btn'].click()
    payout = tab.records_section[0]['view_ticket'].payout_widget
    payout.history_btn.click()
    dialog = payout.history_dialog

    card = dialog.layout().itemAt(0).widget()
    top_layout = card.layout().itemAt(0).layout()
    expand_btn = top_layout.itemAt(5).widget()
    details = card.layout().itemAt(1).widget()
    expand_btn.click()

    details_layout = details.layout()
    totals_layout = details_layout.itemAt(details_layout.count() - 1).layout()
    excel_btn = totals_layout.itemAt(0).widget()

    output_path = os.path.join(os.path.dirname(__file__), 'test_history_excel.xlsx')
    with patch('utils.core.generate_excel.QFileDialog.getSaveFileName',
               return_value=(output_path, 'Excel File (*.xlsx)')), \
            patch('ui.prompts.view_history.QMessageBox.information'):
        excel_btn.click()
    assert os.path.exists(output_path), 'Expected Excel file to be generated'
    os.remove(output_path)
    dialog.close()