import pytest

from PyQt6.QtTest import QTest

from handlers.api_handler import APIHandler
from services.insert_item import insert_item
from services.delete_item import delete_item
from ui.tabs.subtabs import VendorsTab

from services.connect_database import db_connection

@pytest.fixture
def vendor_tab(app):
    api = APIHandler()
    yield VendorsTab(api, db_connection)

@pytest.fixture
def test_vendor(vendor_tab):
    vendor_id_number = 1
    vendor = {
        "id": "vendor_1",
        "partitionKey": "vendor_1",
        "entity_type": "vendor",
        "vendor_id": vendor_id_number,
        "phone": "111-111-1111",
        "first_name": "first test",
        "middle_name": "first test",
        "last_name": "first test",
        "address": "111 first test",
        "city": "first test city",
        "state": "FT",
        "zip": 11111
    }
    insert_item('Entities','vendor', vendor)
    yield vendor_id_number
    delete_item('Entities', 'vendor', vendor)

def test_vendor_id_input(vendor_tab):
    tab = vendor_tab
    assert tab.vendor_id_input is not None, 'Expected Vendor ID Input to exist'
    QTest.keyClicks(tab.vendor_id_input, 'abc./')
    assert tab.vendor_id_input.text() == '', 'Expected field validator to reject all entered input'
    tab.vendor_id_input.clear()
    QTest.keyClicks(tab.vendor_id_input, 'abc1./')
    assert tab.vendor_id_input.text() == '1', 'Expected only integers to be accepted'
    QTest.qWait(400)
    assert tab.vendors_layout.count() > 0, 'Expected ticket sections for vendor ID: 1'

def test_phone_number_input(vendor_tab):
    tab = vendor_tab
    assert tab.phone_number_input is not None, 'Expected phone number input to exist'
    QTest.keyClicks(tab.phone_number_input, 'abc./')
    assert tab.phone_number_input.text() == '', 'Expected only integers to be accepted'
    tab.phone_number_input.clear()
    QTest.keyClicks(tab.phone_number_input, '01234567')
    assert tab.phone_number_input.text() == '012-345-67', 'Expected phone to be masked'
    tab.phone_number_input.clear()
    QTest.keyClicks(tab.phone_number_input, '1111111111')
    assert tab.phone_number_input.text() == '111-111-1111', 'Expected phone to be masked'
    QTest.qWait(400)
    assert tab.vendors_layout.count() > 0, 'Expected ticket sections for phone number: 111-111-1111'

def test_first_name_inputs(vendor_tab):
    tab = vendor_tab
    assert tab.first_name_input is not None, 'Expected First Name Input to exist'
    QTest.keyClicks(tab.first_name_input, '123./')
    assert tab.first_name_input.text() == '', 'Expected field validator to reject all entered input'
    tab.first_name_input.clear()
    QTest.keyClicks(tab.first_name_input, 'first123./')
    assert tab.first_name_input.text().strip() == 'first', 'Expected only alpha characters in first name'
    QTest.qWait(400)
    assert tab.vendors_layout.count() > 0, 'Expected ticket sections for first name: first'

def test_middle_name_inputs(vendor_tab):
    tab = vendor_tab
    assert tab.middle_name_input is not None, 'Expected Middle Name Input to exist'
    QTest.keyClicks(tab.middle_name_input, '123./')
    assert tab.middle_name_input.text() == '', 'Expected field validator to reject all entered input'
    tab.middle_name_input.clear()
    QTest.keyClicks(tab.middle_name_input, 'first123./')
    assert tab.middle_name_input.text().strip() == 'first', 'Expected only alpha characters in middle name'
    QTest.qWait(400)
    assert tab.vendors_layout.count() > 0, 'Expected ticket sections for middle name: first'

def test_last_name_input(vendor_tab):
    """
    :Purpose: verifies that the last name field only takes integers and results in a successful query
    :Author(s): Joe Lee
    """
    tab = vendor_tab
    assert tab.last_name_input is not None, 'Expected Last Name Input to exist'
    QTest.keyClicks(tab.last_name_input, '123./')
    assert tab.last_name_input.text() == '', 'Expected field validator to reject all entered input'
    tab.last_name_input.clear()
    QTest.keyClicks(tab.last_name_input, 'first123./')
    assert tab.last_name_input.text().strip() == 'first', 'Expected only alpha characters in last name'
    QTest.qWait(400)
    assert tab.vendors_layout.count() > 0, 'Expected ticket sections for last name: first'

def test_address_input(vendor_tab):
    """
    :Purpose: verifies that the address field only takes integers and results in a successful query
    :Author(s): Joe Lee
    """
    tab = vendor_tab
    assert tab.address_input is not None, 'Expected Address Input to exist'
    QTest.keyClicks(tab.address_input, './')
    assert tab.address_input.text() == '', 'Expected field validator to reject all entered input'
    tab.address_input.clear()
    QTest.keyClicks(tab.address_input, '111 first./')
    assert tab.address_input.text().strip() == '111 first', 'Expected only alphanumeric characters in address'
    QTest.qWait(400)
    assert tab.vendors_layout.count() > 0, 'Expected ticket sections for address: 111 first'

def test_city_input(vendor_tab):
    """
    :Purpose: verifies that the city field only takes integers and results in a successful query
    :Author(s): Joe Lee
    """
    tab = vendor_tab
    assert tab.city_input is not None, 'Expected City Input to exist'
    QTest.keyClicks(tab.city_input, '123./')
    assert tab.city_input.text() == '', 'Expected field validator to reject all entered input'
    tab.city_input.clear()
    QTest.keyClicks(tab.city_input, 'first123./')
    assert tab.city_input.text().strip() == 'first', 'Expected only alpha characters in city'
    QTest.qWait(400)
    assert tab.vendors_layout.count() > 0, 'Expected ticket sections for city: first'

def test_state_input(vendor_tab):
    """
    :Purpose: verifies that the state field only takes integers and results in a successful query
    :Author(s): Joe Lee
    """
    tab = vendor_tab
    assert tab.state_input is not None, 'Expected State Input to exist'
    QTest.keyClicks(tab.state_input, '123./')
    assert tab.state_input.text() == '', 'Expected field validator to reject all entered input'
    tab.state_input.clear()
    QTest.keyClicks(tab.state_input, 'ft123./')
    assert tab.state_input.text().strip() == 'FT', 'Expected input to be masked and limited to 2 chars'
    QTest.qWait(400)
    assert tab.vendors_layout.count() > 0, 'Expected ticket sections for state: ft'

def test_zip_input(vendor_tab):
    tab = vendor_tab
    assert tab.zip_input is not None, 'Expected ZIP Input to exist'
    QTest.keyClicks(tab.zip_input, 'abc./')
    assert tab.zip_input.text() == '', 'Expected field validator to reject all entered input'
    tab.zip_input.clear()
    QTest.keyClicks(tab.zip_input, 'abc11111./')
    assert tab.zip_input.text().strip() == '11111', 'Expected only numeric values in zip'
    QTest.qWait(400)
    assert tab.vendors_layout.count() > 0, 'Expected ticket sections for zip: 11111'

def test_btns_exist(vendor_tab):
    tab = vendor_tab
    assert tab.clear_btn is not None, 'Expected clear_btn to exist'
    assert tab.search_btn is not None, 'Expected search_btn to exist'
    assert tab.create_btn is not None, 'Expected create_btn to exist'

def test_vendor_section(vendor_tab):
    tab = vendor_tab
    QTest.keyClicks(tab.vendor_id_input, 'abc1./')  # don't put commas
    assert tab.vendor_id_input.text() == '1', 'Expected only integers to be accepted'
    QTest.qWait(400)
    assert tab.vendors_layout.count() > 0, 'Expected ticket sections for vendor ID: 1'
    assert tab.vendors_layout.itemAt(0).widget() is not None, 'Expected vendor section widget to not be None'