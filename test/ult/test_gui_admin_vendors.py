import pytest
from unittest.mock import MagicMock

from PyQt6.QtTest import QTest

from ui.tabs.subtabs.vendors import VendorsTab

@pytest.fixture
def vendors_tab(app):
    fake_api = MagicMock()
    fake_db = MagicMock()
    yield VendorsTab(fake_api, fake_db)

def test_vendor_id_input(vendors_tab):
    tab = vendors_tab
    assert tab.vendor_id_input is not None, 'Expected Vendor ID Input to exist'
    QTest.keyClicks(tab.vendor_id_input, 'abc123./') # don't put commas
    assert tab.vendor_id_input.text() == '123', 'Expected only integers to be accepted'

def test_phone_number_input(vendors_tab):
    tab = vendors_tab
    assert tab.phone_number_input is not None, 'Expected Phone Input to exist'
    QTest.keyClicks(tab.phone_number_input, '01234567')
    assert tab.phone_number_input.text() == '012-345-67', 'Expected phone to be masked'
    tab.phone_number_input.clear()
    QTest.keyClicks(tab.phone_number_input, '0123456789')
    assert tab.phone_number_input.text() == '012-345-6789', 'Expected phone to be masked'

def test_name_inputs(vendors_tab):
    tab = vendors_tab
    assert tab.first_name_input is not None, 'Expected First Name Input to exist'
    QTest.keyClicks(tab.first_name_input, 'abc123./')
    assert tab.first_name_input.text().strip() == 'abc', 'Expected only alpha characters in first name'

    assert tab.middle_name_input is not None, 'Expected Middle Name Input to exist'
    QTest.keyClicks(tab.middle_name_input, 'abc123./')
    assert tab.middle_name_input.text().strip() == 'abc', 'Expected only alpha characters in middle name'

    assert tab.last_name_input is not None, 'Expected Last Name Input to exist'
    QTest.keyClicks(tab.last_name_input, 'abc123./')
    assert tab.last_name_input.text().strip() == 'abc', 'Expected only alpha characters in last name'

def test_address_input(vendors_tab):
    tab = vendors_tab
    assert tab.address_input is not None, 'Expected Address Input to exist'
    QTest.keyClicks(tab.address_input, 'abc123./')
    assert tab.address_input.text().strip() == 'abc123', 'Expected only alphanumeric characters in address'

def test_city_input(vendors_tab):
    tab = vendors_tab
    assert tab.city_input is not None, 'Expected City Input to exist'
    QTest.keyClicks(tab.city_input, 'abc123./')
    assert tab.city_input.text().strip() == 'abc', 'Expected only alpha characters in city'

def test_state_input(vendors_tab):
    tab = vendors_tab
    assert tab.state_input is not None, 'Expected State Input to exist'
    QTest.keyClicks(tab.state_input, 'abc123./')
    assert tab.state_input.text().strip() == 'AB', 'Expected input to be masked and limited to 2 chars'

def test_zip_input(vendors_tab):
    tab = vendors_tab
    assert tab.zip_input is not None, 'Expected ZIP Input to exist'
    QTest.keyClicks(tab.zip_input, 'abc12345./')
    assert tab.zip_input.text().strip() == '12345', 'Expected only numeric values in zip'

def test_button_exists(vendors_tab):
    tab = vendors_tab
    assert tab.create_btn is not None, 'Expected Create New Vendor button to exist'
    assert tab.clear_btn is not None, 'Expected Clear button to exist'
    assert tab.search_btn is not None, 'Expected Search button to exist'