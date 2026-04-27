import os
import pytest
import re
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtTest import QTest
from PyQt6.QtWidgets import QDialog
from PyQt6.QtWidgets import QPushButton
from unittest.mock import patch

from handlers.api_handler import APIHandler
from services.connect_database import db_connection
from services.delete_item import delete_item
from ui.tabs.create_new import CreateNewTab
from utils.core.generate_pdf import PDF

@pytest.fixture
def create_new_tab(app):
    api = APIHandler()
    yield CreateNewTab(api, db_connection)

def test_ticket_number(create_new_tab):
    """
    :Purpose: verifies that the ticket number field exists and its value is generated
    :Author(s): Joe Lee
    """
    tab = create_new_tab
    assert tab.ticket_input is not None, 'Expected Ticket Number field to exist'
    assert tab.ticket_input.text() != 'OFFLINE', 'Expected Ticket Number field to have a valid value'

def test_vendor_id(create_new_tab):
    """
    :Purpose: verifies that the vendor id field exists and only accepts integers
    :Author(s): Joe Lee
    """
    tab = create_new_tab
    assert tab.vendor_id_input is not None, 'Expected vendor id field to exist'
    assert tab.vendor_id_input.text().strip() == '', 'Expected vendor id field to not instantiate with a value'
    QTest.keyClicks(tab.vendor_id_input, "./asdf")
    assert tab.vendor_id_input.text().strip() == '', 'Expected constraints to reject all character inputs'
    QTest.keyClicks(tab.vendor_id_input, "./asdf1")
    assert tab.vendor_id_input.text().strip() == '1', "Expected field to have value '1'"

def test_vendor_id_autopop(create_new_tab):
    """
    :Purpose: verifies that the vendor id autopop executes successfully
    :Author(s): Joe Lee
    """
    tab = create_new_tab
    QTest.keyClicks(tab.vendor_id_input, "./asdf1")
    assert tab.vendor_id_input.text().strip() == '1', "Expected field to have value '1'"

    assert not tab.vendor_id_input.isReadOnly(), 'Expected vendor id field to not be locked'
    assert not tab.phone_input.isReadOnly(), 'Expected phone field to not be locked'
    assert not tab.first_name_input.isReadOnly(), 'Expected first_name field to not be locked'
    assert not tab.middle_name_input.isReadOnly(), 'Expected middle_name field to not be locked'
    assert not tab.last_name_input.isReadOnly(), 'Expected last_name field to not be locked'
    assert not tab.address_input.isReadOnly(), 'Expected address field to not be locked'
    assert not tab.city_input.isReadOnly(), 'Expected city field to not be locked'
    assert not tab.state_input.isReadOnly(), 'Expected state field to not be locked'
    assert not tab.zip_input.isReadOnly(), 'Expected zip field to not be locked'
    QTest.keyPress(tab.vendor_id_input, Qt.Key.Key_Return)
    assert not tab.vendor_id_input.isReadOnly(), 'Expected vendor id field to be enabled'
    assert tab.phone_input.isReadOnly(), 'Expected phone field to be locked'
    assert tab.first_name_input.isReadOnly(), 'Expected first_name field to be locked'
    assert tab.middle_name_input.isReadOnly(), 'Expected middle_name field to be locked'
    assert tab.last_name_input.isReadOnly(), 'Expected last_name field to be locked'
    assert tab.address_input.isReadOnly(), 'Expected address field to be locked'
    assert tab.city_input.isReadOnly(), 'Expected city field to be locked'
    assert tab.state_input.isReadOnly(), 'Expected state field to be locked'
    assert tab.zip_input.isReadOnly(), 'Expected zip field to be locked'

def test_phone_number(create_new_tab):
    """
    :Purpose: verifies that the phone number field exists and only accepts integers
    :Author(s): Joe Lee
    """
    tab = create_new_tab
    assert tab.phone_input is not None, 'Expected phone number field to exist'
    assert tab.phone_input.text().strip() == '', 'Expected phone number field to not instantiate with a value'
    QTest.keyClicks(tab.phone_input, "./asdf")
    assert tab.phone_input.text().strip() == '', 'Expected constraints to reject all character inputs'
    QTest.keyClicks(tab.phone_input, "1111111111")
    assert tab.phone_input.text().strip() == '111-111-1111', "Expected field to have value '111-111-1111' after mask applies"

def test_phone_number_autopop(create_new_tab):
    """
    :Purpose: verifies that phone number autopop successfully executes
    :Author(s): Joe Lee
    """
    tab = create_new_tab
    assert not tab.vendor_id_input.isReadOnly(), 'Expected vendor id field to not be locked'
    assert not tab.phone_input.isReadOnly(), 'Expected phone field to not be locked'
    assert not tab.first_name_input.isReadOnly(), 'Expected first_name field to not be locked'
    assert not tab.middle_name_input.isReadOnly(), 'Expected middle_name field to not be locked'
    assert not tab.last_name_input.isReadOnly(), 'Expected last_name field to not be locked'
    assert not tab.address_input.isReadOnly(), 'Expected address field to not be locked'
    assert not tab.city_input.isReadOnly(), 'Expected city field to not be locked'
    assert not tab.state_input.isReadOnly(), 'Expected state field to not be locked'
    assert not tab.zip_input.isReadOnly(), 'Expected zip field to not be locked'

    QTest.keyClicks(tab.phone_input, '1111111111')
    assert tab.phone_input.text() == '111-111-1111', 'Expected phone to be masked'

    def click_confirm():
        dialog = tab.findChild(QDialog)
        if dialog:
            for btn in dialog.findChildren(QPushButton):
                if btn.text() == 'Confirm':
                    btn.click()
                    return

    QTimer.singleShot(500, click_confirm)
    QTest.keyPress(tab.phone_input, Qt.Key.Key_Return)
    QTest.qWait(600)

    assert tab.vendor_id_input.isReadOnly(), 'Expected vendor id field to be enabled'
    assert not tab.phone_input.isReadOnly(), 'Expected phone field to be locked'
    assert tab.first_name_input.isReadOnly(), 'Expected first_name field to be locked'
    assert tab.middle_name_input.isReadOnly(), 'Expected middle_name field to be locked'
    assert tab.last_name_input.isReadOnly(), 'Expected last_name field to be locked'
    assert tab.address_input.isReadOnly(), 'Expected address field to be locked'
    assert tab.city_input.isReadOnly(), 'Expected city field to be locked'
    assert tab.state_input.isReadOnly(), 'Expected state field to be locked'
    assert tab.zip_input.isReadOnly(), 'Expected zip field to be locked'

def test_datetime(create_new_tab):
    """
    :Purpose: verifies that the datetime field exists and is read only
    """
    tab = create_new_tab
    assert tab.datetime_input is not None, 'Expected datetime field to exist'
    assert tab.datetime_input.isReadOnly(), 'Expected datetime field to be readOnly'
    assert re.match(r'\d{2}/\d{2}/\d{2} -- \d{2}:\d{2} (AM|PM)', tab.datetime_input.text().strip()), "Expected datetime field to have format 'MM\\DD\\YY -- %I:%M %p"

def test_first_name_inputs(create_new_tab):
    """
    :Purpose: verifies that the first name field only takes alphabetical characters
    :Author(s): Joe Lee
    """
    tab = create_new_tab
    assert tab.first_name_input is not None, 'Expected First Name Input to exist'
    QTest.keyClicks(tab.first_name_input, '123./')
    assert tab.first_name_input.text() == '', 'Expected field validator to reject all entered input'
    tab.first_name_input.clear()
    QTest.keyClicks(tab.first_name_input, 'first123./')
    assert tab.first_name_input.text().strip() == 'first', 'Expected only alpha characters in first name'

def test_middle_name_inputs(create_new_tab):
    """
    :Purpose: verifies that the middle name field only takes alphabetical characters
    :Author(s): Joe Lee
    """
    tab = create_new_tab
    assert tab.middle_name_input is not None, 'Expected Middle Name Input to exist'
    QTest.keyClicks(tab.middle_name_input, '123./')
    assert tab.middle_name_input.text() == '', 'Expected field validator to reject all entered input'
    tab.middle_name_input.clear()
    QTest.keyClicks(tab.middle_name_input, 'first123./')
    assert tab.middle_name_input.text().strip() == 'first', 'Expected only alpha characters in middle name'

def test_last_name_input(create_new_tab):
    """
    :Purpose: verifies that the last name field only takes alphabetical characters
    :Author(s): Joe Lee
    """
    tab = create_new_tab
    assert tab.last_name_input is not None, 'Expected Last Name Input to exist'
    QTest.keyClicks(tab.last_name_input, '123./')
    assert tab.last_name_input.text() == '', 'Expected field validator to reject all entered input'
    tab.last_name_input.clear()
    QTest.keyClicks(tab.last_name_input, 'first123./')
    assert tab.last_name_input.text().strip() == 'first', 'Expected only alpha characters in last name'

def test_address_input(create_new_tab):
    """
    :Purpose: verifies that the address field only takes alphanumerical characters
    :Author(s): Joe Lee
    """
    tab = create_new_tab
    assert tab.address_input is not None, 'Expected Address Input to exist'
    QTest.keyClicks(tab.address_input, './')
    assert tab.address_input.text() == '', 'Expected field validator to reject all entered input'
    tab.address_input.clear()
    QTest.keyClicks(tab.address_input, '111 first./')
    assert tab.address_input.text().strip() == '111 first', 'Expected only alphanumeric characters in address'

def test_city_input(create_new_tab):
    """
    :Purpose: verifies that the city field only takes alphabetical characters
    :Author(s): Joe Lee
    """
    tab = create_new_tab
    assert tab.city_input is not None, 'Expected City Input to exist'
    QTest.keyClicks(tab.city_input, '123./')
    assert tab.city_input.text() == '', 'Expected field validator to reject all entered input'
    tab.city_input.clear()
    QTest.keyClicks(tab.city_input, 'first123./')
    assert tab.city_input.text().strip() == 'first', 'Expected only alpha characters in city'

def test_state_input(create_new_tab):
    """
    :Purpose: verifies that the state field only takes integers and results in a successful query
    :Author(s): Joe Lee
    """
    tab = create_new_tab
    assert tab.state_input is not None, 'Expected State Input to exist'
    QTest.keyClicks(tab.state_input, '123./')
    assert tab.state_input.text() == '', 'Expected field validator to reject all entered input'
    tab.state_input.clear()
    QTest.keyClicks(tab.state_input, 'ft123./')
    assert tab.state_input.text().strip() == 'FT', 'Expected input to be masked and limited to 2 chars'

def test_zip_input(create_new_tab):
    """
    :Purpose: verifies that the zip field only takes integers
    :Author(s): Joe Lee
    """
    tab = create_new_tab
    assert tab.zip_input is not None, 'Expected ZIP Input to exist'
    QTest.keyClicks(tab.zip_input, 'abc./')
    assert tab.zip_input.text() == '', 'Expected field validator to reject all entered input'
    tab.zip_input.clear()
    QTest.keyClicks(tab.zip_input, 'abc11111./')
    assert tab.zip_input.text().strip() == '11111', 'Expected only numeric values in zip'

def test_product_sections(create_new_tab):
    """
    :Purpose: verifies that the product sections exist
    :Author(s): Joe Lee
    """
    tab = create_new_tab
    assert len(tab.product_sections) == 3, 'Expected 3 product sections on start up'
    for i in range(len(tab.product_sections)):
        assert tab.product_sections[i]['product_id'] is not None, 'Expected Product ID Input to exist'
        assert tab.product_sections[i]['product_type'] is not None, 'Expected Product Type Input to exist'
        assert tab.product_sections[i]['product_name'] is not None, 'Expected Product Name Input to exist'
        assert tab.product_sections[i]['notes'] is not None, 'Expected Product Notes Input to exist'
        assert tab.product_sections[i]['rate'] is not None, 'Expected Product Rate field to exist'
        assert tab.product_sections[i]['price'] is not None, 'Expected Product Price Input to exist'
        assert tab.product_sections[i]['quantity'] is not None, 'Expected Product Quantity Input to exist'
        assert tab.product_sections[i]['total'] is not None, 'Expected Product Total field to exist'

def test_product_id(create_new_tab):
    """
    :Purpose: verifies that the product id field applies constraints
    :Author(s): Joe Lee
    """
    tab = create_new_tab
    for i in range(len(tab.product_sections)):
        QTest.keyClicks(tab.product_sections[i]['product_id'], 'abc./')
        assert tab.product_sections[i]['product_id'].text().strip() == '', 'Expected constraints to reject all entered characters'
        QTest.keyClicks(tab.product_sections[i]['product_id'], 'abc./1')
        assert tab.product_sections[i]['product_id'].text().strip() == '1', "Expected value of '1' to be retained"

def test_product_id_autopop(create_new_tab):
    """
    :Purpose: verifies that the product id field can successfully trigger autopopulation
    :Author(s): Joe Lee
    """
    tab = create_new_tab
    for i in range(len(tab.product_sections)):
        assert not tab.product_sections[i]['product_id'].isReadOnly(), 'Expected Product ID Input to not be locked'
        assert tab.product_sections[i]['product_type'].isEnabled(), 'Expected Product Type Input not be locked'
        assert not tab.product_sections[i]['product_name'].isReadOnly(), 'Expected Product Name Input to not be locked'
        assert tab.product_sections[i]['product_name'].text().strip() == '', 'Expected Product Name input to not have a value'
        assert not tab.product_sections[i]['notes'].isReadOnly(), 'Expected Product Notes Input to not be locked'
        assert tab.product_sections[i]['rate'].isReadOnly(), 'Expected Product Rate field to be locked'
        assert not tab.product_sections[i]['price'].isReadOnly(), 'Expected Product Price Input to not be locked'
        assert not tab.product_sections[i]['quantity'].isReadOnly(), 'Expected Product Quantity Input to not be locked'
        assert tab.product_sections[i]['total'].isReadOnly(), 'Expected Product Total field to be locked'
        QTest.keyClicks(tab.product_sections[i]['product_id'], '1')
        QTest.keyPress(tab.product_sections[i]['product_id'], Qt.Key.Key_Return)
        assert not tab.product_sections[i]['product_id'].isReadOnly(), 'Expected Product ID Input to not be locked'
        assert not tab.product_sections[i]['product_type'].isEnabled(), 'Expected Product Type Input to be locked'
        assert tab.product_sections[i]['product_type'].currentText().strip() == 'Hot Food', "Expected 'Hot Food'"
        assert tab.product_sections[i]['product_name'].isReadOnly(), 'Expected Product Name Input to be locked'
        assert tab.product_sections[i]['product_name'].text().strip() != '', 'Expected Product Name input to have a value'
        assert not tab.product_sections[i]['notes'].isReadOnly(), 'Expected Product Notes Input to not be locked'
        assert tab.product_sections[i]['rate'].isReadOnly(), 'Expected Product Rate field to be locked'
        assert not tab.product_sections[i]['price'].isReadOnly(), 'Expected Product Price Input to not be locked'
        assert not tab.product_sections[i]['quantity'].isReadOnly(), 'Expected Product Quantity Input to not be locked'
        assert tab.product_sections[i]['total'].isReadOnly(), 'Expected Product Total field to be locked'

def test_product_type(create_new_tab):
    """
    :Purpose: verifies that the product type field has the required types
    :Author(s): Joe Lee
    """
    tab = create_new_tab
    for i in range(len(tab.product_sections)):
        tab.product_sections[i]['product_type'].setCurrentIndex(0)
        assert tab.product_sections[i]['product_type'].currentText().strip() == 'Hot Food', "Expected 'Hot Food"
        tab.product_sections[i]['product_type'].setCurrentIndex(1)
        assert tab.product_sections[i]['product_type'].currentText().strip() == 'General', "Expected 'General"
        tab.product_sections[i]['product_type'].setCurrentIndex(2)
        assert tab.product_sections[i]['product_type'].currentText().strip() == 'Produce', "Expected 'Produce"

def test_product_name(create_new_tab):
    """
    :Purpose: verifies that the product name field's constraints apply
    :Author(s): Joe Lee
    """
    tab = create_new_tab
    for i in range(len(tab.product_sections)):
        QTest.keyClicks(tab.product_sections[i]['product_name'], '123./')
        assert tab.product_sections[i]['product_name'].text().strip() == '', 'Expected constraints to reject all entered characters'
        tab.product_sections[i]['product_name'].clear()
        QTest.keyClicks(tab.product_sections[i]['product_name'], 'abc./')
        assert tab.product_sections[i]['product_name'].text().strip() == 'abc', 'Expected constraints to reject all entered characters'
        tab.product_sections[i]['product_name'].clear()
        QTest.keyClicks(tab.product_sections[i]['product_name'], 'abc./1')
        assert tab.product_sections[i]['product_name'].text().strip() == 'abc', "Expected value of '1' to be retained"

def test_product_name_autopop(create_new_tab):
    """
    :Purpose: verifies that the product name field can successfully trigger autopopulation
    :Author(s): Joe Lee
    """
    tab = create_new_tab
    for i in range(len(tab.product_sections)):
        assert not tab.product_sections[i]['product_id'].isReadOnly(), 'Expected Product ID Input to not be locked'
        assert tab.product_sections[i]['product_type'].isEnabled(), 'Expected Product Type Input not be locked'
        assert not tab.product_sections[i]['product_name'].isReadOnly(), 'Expected Product Name Input to not be locked'
        assert tab.product_sections[i]['product_name'].text().strip() == '', 'Expected Product Name input to not have a value'
        assert not tab.product_sections[i]['notes'].isReadOnly(), 'Expected Product Notes Input to not be locked'
        assert tab.product_sections[i]['rate'].isReadOnly(), 'Expected Product Rate field to be locked'
        assert not tab.product_sections[i]['price'].isReadOnly(), 'Expected Product Price Input to not be locked'
        assert not tab.product_sections[i]['quantity'].isReadOnly(), 'Expected Product Quantity Input to not be locked'
        assert tab.product_sections[i]['total'].isReadOnly(), 'Expected Product Total field to be locked'
        QTest.keyClicks(tab.product_sections[i]['product_name'], 'Hot Food')
        QTest.keyPress(tab.product_sections[i]['product_name'], Qt.Key.Key_Return)
        assert tab.product_sections[i]['product_id'].isReadOnly(), 'Expected Product ID Input to be locked'
        assert not tab.product_sections[i]['product_type'].isEnabled(), 'Expected Product Type Input to be locked'
        assert tab.product_sections[i]['product_type'].currentText().strip() == 'Hot Food', "Expected 'Hot Food'"
        assert not tab.product_sections[i]['product_name'].isReadOnly(), 'Expected Product Name Input to not be locked'
        assert tab.product_sections[i]['product_name'].text().strip() != '', 'Expected Product Name input to have a value'
        assert not tab.product_sections[i]['notes'].isReadOnly(), 'Expected Product Notes Input to not be locked'
        assert tab.product_sections[i]['rate'].isReadOnly(), 'Expected Product Rate field to be locked'
        assert not tab.product_sections[i]['price'].isReadOnly(), 'Expected Product Price Input to not be locked'
        assert not tab.product_sections[i]['quantity'].isReadOnly(), 'Expected Product Quantity Input to not be locked'
        assert tab.product_sections[i]['total'].isReadOnly(), 'Expected Product Total field to be locked'

def test_product_notes(create_new_tab):
    """
    :Purpose: verifies that the product notes field's has no constraints
    :Author(s): Joe Lee
    """
    tab = create_new_tab
    for i in range(len(tab.product_sections)):
        QTest.keyClicks(tab.product_sections[i]['notes'], 'abc123./')
        assert tab.product_sections[i]['notes'].text().strip() == 'abc123./', 'Expected there to be no constraints'
        tab.product_sections[i]['notes'].clear()

def test_product_rate(create_new_tab):
    """
    :Purpose: verifies that the product rate field updates according to the product type
    :Author(s): Joe Lee
    """
    tab = create_new_tab
    for i in range(len(tab.product_sections)):
        assert tab.product_sections[i]['rate'].text().strip() == '', 'Expected rate field to not have a starting value'
        tab.product_sections[i]['product_type'].setCurrentIndex(0)
        assert tab.product_sections[i]['rate'].text().strip() == '30%', "Expected rate field to have a value of '30%'"
        tab.product_sections[i]['product_type'].setCurrentIndex(1)
        assert tab.product_sections[i]['rate'].text().strip() == '25%', "Expected rate field to have a value of '25%'"
        tab.product_sections[i]['product_type'].setCurrentIndex(2)
        assert tab.product_sections[i]['rate'].text().strip() == '25%', "Expected rate field to have a value of '25%'"

def test_product_price(create_new_tab):
    """
    :Purpose: verifies that the product price field's has no constraints
    :Author(s): Joe Lee
    """
    tab = create_new_tab
    for i in range(len(tab.product_sections)):
        QTest.keyClicks(tab.product_sections[i]['price'], 'abc123./')
        assert tab.product_sections[i]['price'].text().strip() == '$1.23', "Expected to receive '1.23' as the price"
        tab.product_sections[i]['price'].clear()

def test_product_quantity(create_new_tab):
    """
    :Purpose: verifies that the product quantity field's has no constraints
    :Author(s): Joe Lee
    """
    tab = create_new_tab
    for i in range(len(tab.product_sections)):
        QTest.keyClicks(tab.product_sections[i]['quantity'], 'abc123./')
        assert tab.product_sections[i]['quantity'].text().strip() == '123', "Expected to receive '123' as the quantity"
        tab.product_sections[i]['quantity'].clear()

def test_product_total(create_new_tab):
    """
    :Purpose: verifies that the product total field's is a product of price and quantity
    :Author(s): Joe Lee
    """
    tab = create_new_tab
    for i in range(len(tab.product_sections)):
        tab.product_sections[i]['product_type'].setCurrentIndex(0)
        QTest.keyClicks(tab.product_sections[i]['price'], '1000')
        QTest.keyClicks(tab.product_sections[i]['quantity'], '1')
        assert tab.product_sections[i]['total'].text().strip() == '$7.00', "Expected Total field ot have value of '$7.00"

def test_remove_product_line(create_new_tab):
    """
    :Purpose: verifies that the remove product line button executes successfully
    :Author(s): Joe Lee
    """
    tab = create_new_tab
    counter = len(tab.product_sections)
    for i in range(counter):
        section_widget = tab.products_layout.itemAt(0).widget()
        for btn in section_widget.findChildren(QPushButton):
            if btn.text() == 'Remove Product Line':
                with patch.object(tab, 'show_remove_product_warning', return_value=True):
                    btn.click()
                break
        assert len(tab.product_sections) == counter - (i + 1), f'Expected {counter - (i + 1)} product sections after removal'
    assert len(tab.product_sections) == 0, 'Expected all product sections to be removed'

def test_remove_product_line_cancel(create_new_tab):
    """
    :Purpose: verifies that the remove product line button cancels successfully
    :Author(s): Joe Lee
    """
    tab = create_new_tab
    counter = len(tab.product_sections)
    section_widget = tab.products_layout.itemAt(0).widget()
    for btn in section_widget.findChildren(QPushButton):
        if btn.text() == 'Remove Product Line':
            with patch.object(tab, 'show_remove_product_warning', return_value=False):
                btn.click()
            break
    assert len(tab.product_sections) == counter, 'Expected product sections to remain unchanged after cancel'

def test_add_product_line(create_new_tab):
    """
    :Purpose: verifies that the add product line button executes successfully
    :Author(s): Joe Lee
    """
    tab = create_new_tab
    start = len(tab.product_sections)
    tab.add_product_btn.click()
    new = len(tab.product_sections)
    assert new != start, f'Expected {new} product sections after add'

def test_rev_by_prod_type(create_new_tab):
    """
    :Purpose: verifies that the revenue by product type widget exists
    :Author(s): Joe Lee
    """
    tab = create_new_tab
    assert tab.rev_by_prod is not None, 'Expected Revenue by Product Type widget to exist'
    assert len(tab.rev_by_prod.revenue_records) == 4, 'Expected 4 rows in Revenue by Product Type'
    prod_types = ['Hot Food', 'General', 'Produce', 'Total']
    for idx, group in enumerate(tab.rev_by_prod.revenue_records):
        assert group['type_label'] is not None, f'Expected type label for row {idx}'
        assert group['total_edit'] is not None, f'Expected total field for row {idx}'
        assert group['product_type'] == prod_types[idx], f'Expected product type {prod_types[idx]} at row {idx}'
        assert group['total_edit'].isReadOnly(), f'Expected total field to be read only for row {idx}'
        assert group['total_edit'].text().strip() == '$0.00', "Expected initial values to be '$0.00'"

    QTest.keyClicks(tab.product_sections[0]['product_id'], '1')
    QTest.keyPress(tab.product_sections[0]['product_id'], Qt.Key.Key_Return)
    QTest.keyClicks(tab.product_sections[0]['price'], '1000')
    QTest.keyClicks(tab.product_sections[0]['quantity'], '1')
    QTest.keyClicks(tab.product_sections[1]['product_id'], '2')
    QTest.keyPress(tab.product_sections[1]['product_id'], Qt.Key.Key_Return)
    QTest.keyClicks(tab.product_sections[1]['price'], '1000')
    QTest.keyClicks(tab.product_sections[1]['quantity'], '1')
    QTest.keyClicks(tab.product_sections[2]['product_id'], '3')
    QTest.keyPress(tab.product_sections[2]['product_id'], Qt.Key.Key_Return)
    QTest.keyClicks(tab.product_sections[2]['price'], '1000')
    QTest.keyClicks(tab.product_sections[2]['quantity'], '1')
    tab.calc_btn.click()
    for group in tab.rev_by_prod.revenue_records:
        if group['product_type'] == 'Hot Food':
            assert group['total_edit'].text().strip() == '$7.00', "Expected 'Hot Food' group to be '$7.00'"
        elif group['product_type'] == 'General':
            assert group['total_edit'].text().strip() == '$7.50', "Expected 'General' group to be '$7.50'"
        elif group['product_type'] == 'Produce':
            assert group['total_edit'].text().strip() == '$7.50', "Expected 'Produce' group to be '$7.50'"
        elif group['product_type'] == 'Total':
            assert group['total_edit'].text().strip() == '$22.00', "Expected Total to be '$22.00'"

def test_revenue_sharing(create_new_tab):
    """
    :Purpose: verifies that the revenue sharing widget exists and updates accordingly
    :Author(s): Joe Lee
    """
    tab = create_new_tab
    assert tab.revenue_generation is not None, 'Expected Revenue Sharing widget to exist'
    assert len(tab.revenue_generation.revenue_records) == 4, 'Expected 4 rows in Revenue Sharing'
    percentages = ['25%', '50%', '75%', '100%']
    for idx, record in enumerate(tab.revenue_generation.revenue_records):
        assert record['vendor'] is not None, f'Expected vendor field for row {idx}'
        assert record['vendor'].isReadOnly(), f'Expected vendor field to be read only for row {idx}'
        assert record['super_x'] is not None, f'Expected super x field for row {idx}'
        assert record['super_x'].isReadOnly(), f'Expected super x field to be read only for row {idx}'
        assert record['percentage'].text() == percentages[
            idx], f'Expected percentage to be {percentages[idx]} at row {idx}'
        assert record['vendor'].text().strip() == '$0.00', 'Expected initial vendor value to be $0.00'
        assert record['super_x'].text().strip() == '$0.00', 'Expected initial super x value to be $0.00'

    QTest.keyClicks(tab.product_sections[0]['product_id'], '1')
    QTest.keyPress(tab.product_sections[0]['product_id'], Qt.Key.Key_Return)
    QTest.keyClicks(tab.product_sections[0]['price'], '1000')
    QTest.keyClicks(tab.product_sections[0]['quantity'], '1')
    tab.calc_btn.click()

    for idx, record in enumerate(tab.revenue_generation.revenue_records):
        assert record['vendor'].text().strip() != '$0.00', f'Expected vendor to be updated at row {idx}'
        assert record['super_x'].text().strip() != '$0.00', f'Expected super x to be updated at row {idx}'

def test_clear_btn(create_new_tab):
    """
    :Purpose: verifies that the clear_btn exists and executes successfully
    :Author(s): Joe Lee
    """
    tab = create_new_tab
    assert tab.clear_btn is not None, 'Expected clear_btn to exist'
    QTest.keyClicks(tab.vendor_id_input, '1')
    QTest.keyPress(tab.vendor_id_input, Qt.Key.Key_Return)
    QTest.keyClicks(tab.product_sections[0]['product_id'], '1')
    QTest.keyPress(tab.product_sections[0]['product_id'], Qt.Key.Key_Return)
    QTest.keyClicks(tab.product_sections[0]['notes'], "blah")
    QTest.keyClicks(tab.product_sections[0]['price'], "1234")
    QTest.keyClicks(tab.product_sections[0]['quantity'], "1234")
    tab.clear_btn.click()
    assert tab.vendor_id_input.text().strip() == '', 'Expected vendor_id input to be cleared'
    assert tab.phone_input.text().strip() == '', 'Expected phone input to be cleared'
    assert tab.first_name_input.text().strip() == '', 'Expected first name input to be cleared'
    assert tab.middle_name_input.text().strip() == '', 'Expected middle name input to be cleared'
    assert tab.last_name_input.text().strip() == '', 'Expected last name input to be cleared'
    assert tab.address_input.text().strip() == '', 'Expected address input to be cleared'
    assert tab.city_input.text().strip() == '', 'Expected city input to be cleared'
    assert tab.state_input.text().strip() == '', 'Expected state input to be cleared'
    assert tab.zip_input.text().strip() == '', 'Expected zip input to be cleared'
    assert tab.product_sections[0]['product_id'].text().strip() == '', "Expected product id to be cleared"
    assert tab.product_sections[0]['notes'].text().strip() == '', 'Expected notes input to be cleared'
    assert tab.product_sections[0]['price'].text().strip() == '', 'Expected price input to be cleared'
    assert tab.product_sections[0]['quantity'].text().strip() == '', 'Expected quantity input to be cleared'

def test_excel_btn(create_new_tab):
    """
    :Purpose: verifies that the excel btn exists and executes successfully
    :Author(s): Joe Lee
    """
    tab = create_new_tab
    assert tab.excel_btn is not None, 'Expected excel_btn to exist'
    QTest.keyClicks(tab.vendor_id_input, '1')
    QTest.keyPress(tab.vendor_id_input, Qt.Key.Key_Return)
    QTest.keyClicks(tab.product_sections[0]['product_id'], '1')
    QTest.keyPress(tab.product_sections[0]['product_id'], Qt.Key.Key_Return)
    QTest.keyClicks(tab.product_sections[0]['price'], '1000')
    QTest.keyClicks(tab.product_sections[0]['quantity'], '1')
    output_path = os.path.join(os.path.dirname(__file__), 'test_excel_btn.xlsx')
    with patch('utils.core.generate_excel.QFileDialog.getSaveFileName',
               return_value=(output_path, 'Excel File (*.xlsx)')):
        tab.excel_btn.click()
    assert os.path.exists(output_path), 'Expected Excel file to be generated'
    os.remove(output_path)

def test_pdf_btn(create_new_tab):
    """
    :Purpose: verifies that the pdf btn exists and executes successfully
    :Author(s): Joe Lee
    """
    tab = create_new_tab
    assert tab.pdf_btn is not None, 'Expected pdf_btn to exist'
    QTest.keyClicks(tab.vendor_id_input, '1')
    QTest.keyPress(tab.vendor_id_input, Qt.Key.Key_Return)
    QTest.keyClicks(tab.product_sections[0]['product_id'], '1')
    QTest.keyPress(tab.product_sections[0]['product_id'], Qt.Key.Key_Return)
    QTest.keyClicks(tab.product_sections[0]['price'], '1000')
    QTest.keyClicks(tab.product_sections[0]['quantity'], '1')
    pdf_output = os.path.join(os.path.dirname(__file__), 'test_pdf_btn.pdf')

    def set_pdf_filename(self, payout_number=None):
        self.pdf_filename = pdf_output

    with patch.object(PDF, 'set_pdf_filename', set_pdf_filename), \
            patch('ui.tabs.create_new.QMessageBox.information'):
        tab.pdf_btn.click()
    assert os.path.exists(pdf_output), 'Expected PDF to be generated'
    os.remove(pdf_output)

def test_print_btn(create_new_tab):
    """
    :Purpose: verifies that the print btn exists and executes successfully, physically printing has been patched out
    :Author(s): Joe Lee
    """
    tab = create_new_tab
    assert tab.print_btn is not None, 'Expected print_btn to exist'
    QTest.keyClicks(tab.vendor_id_input, '1')
    QTest.keyPress(tab.vendor_id_input, Qt.Key.Key_Return)
    QTest.keyClicks(tab.product_sections[0]['product_id'], '1')
    QTest.keyPress(tab.product_sections[0]['product_id'], Qt.Key.Key_Return)
    QTest.keyClicks(tab.product_sections[0]['price'], '1000')
    QTest.keyClicks(tab.product_sections[0]['quantity'], '1')

    pdf_output = os.path.join(os.path.dirname(__file__), 'test_print_btn.pdf')

    def set_pdf_filename(self):
        self.pdf_filename = os.path.join(os.path.dirname(__file__), 'test_print_btn.pdf')

    with patch.object(PDF, 'set_pdf_filename', set_pdf_filename), \
            patch.object(tab, '_wait_for_pdf', return_value=True), \
            patch('ui.tabs.create_new.handler_print.handler_print'), \
            patch('ui.tabs.create_new.QMessageBox.information'):
        tab.print_btn.click()
    assert os.path.exists(pdf_output), 'Expected PDF to be generated'
    os.remove(pdf_output)

def test_create_btn(create_new_tab):
    """
    :Purpose: verifies that the create btn exists and executes successfully
    :Author(s): Joe Lee
    """
    tab = create_new_tab
    assert tab.create_btn is not None, 'Expected create_btn to exist'
    QTest.keyClicks(tab.vendor_id_input, '1')
    QTest.keyPress(tab.vendor_id_input, Qt.Key.Key_Return)
    QTest.keyClicks(tab.product_sections[0]['product_id'], '1')
    QTest.keyPress(tab.product_sections[0]['product_id'], Qt.Key.Key_Return)
    QTest.keyClicks(tab.product_sections[0]['price'], '1000')
    QTest.keyClicks(tab.product_sections[0]['quantity'], '1')

    ticket_number = int(tab.ticket_input.text().strip())
    pdf_output = os.path.join(os.path.dirname(__file__), f'{ticket_number}.pdf')

    def set_pdf_filename(self, payout_number=None):
        self.pdf_filename = pdf_output

    with patch.object(PDF, 'set_pdf_filename', set_pdf_filename), \
            patch.object(tab, '_wait_for_pdf', return_value=True), \
            patch('ui.tabs.create_new.handler_print.handler_print'), \
            patch('ui.tabs.create_new.QMessageBox.information'):
        tab.create_btn.click()

    assert tab.vendor_id_input.text() == '', 'Expected form to be cleared after successful record creation'

    if os.path.exists(pdf_output):
        os.remove(pdf_output)
    delete_item('Consignments', 'consignment', ticket_number)