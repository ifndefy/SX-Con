import pytest
from unittest.mock import patch
from unittest.mock import MagicMock
from PyQt6.QtTest import QTest
from datetime import datetime

from ui.tabs.create_new import CreateNewTab

@pytest.fixture
def create_new_tab(app):
    with patch('ui.tabs.create_new.get_max_value', return_value=99), \
            patch('ui.tabs.create_new.fetch_consignment_data', return_value={'Hot Food': 50, 'General': 50, 'Produce': 50}), \
            patch('ui.tabs.create_new.SPOT.OFFLINE', new=False):
        fake_api = MagicMock()
        fake_db = MagicMock()
        yield CreateNewTab(fake_api, fake_db)

def test_ticket_input(create_new_tab):
    with patch('ui.tabs.create_new.get_max_value', return_value=99) as fake_max_val:
        tab = create_new_tab
        assert tab.ticket_input is not None, 'Expected Ticket Number Input to exist'
        assert tab.ticket_input.text().strip() == str(int(fake_max_val.return_value) + 1), \
            f"Expected Ticket Number text to be set as max val + 1: {int(fake_max_val.return_value) + 1}"

def test_datetime_input(create_new_tab):
    tab = create_new_tab
    assert tab.datetime_input is not None, 'Expected Date Input to exist'
    now = datetime.now()
    format = "%m/%d/%y -- %H:%M"
    now = now.strftime(format)
    assert tab.datetime_input.text().strip() == now, f'Expected datetime text to be current date and time {now}'

def test_vendor_id_input(create_new_tab):
    tab = create_new_tab
    assert tab.vendor_id_input is not None, 'Expected Vendor ID Input to exist'
    QTest.keyClicks(tab.vendor_id_input, 'abc123./') # don't put commas
    assert tab.vendor_id_input.text() == '123', 'Expected only integers to be accepted'

def test_phone_number_input(create_new_tab):
    tab = create_new_tab
    assert tab.phone_input is not None, 'Expected Phone Input to exist'
    QTest.keyClicks(tab.phone_input, '01234567')
    assert tab.phone_input.text() == '012-345-67', 'Expected phone to be masked'
    tab.phone_input.clear()
    QTest.keyClicks(tab.phone_input, '0123456789')
    assert tab.phone_input.text() == '012-345-6789', 'Expected phone to be masked'

def test_name_inputs(create_new_tab):
    tab = create_new_tab
    assert tab.first_name_input is not None, 'Expected First Name Input to exist'
    QTest.keyClicks(tab.first_name_input, 'abc123./')
    assert tab.first_name_input.text().strip() == 'abc', 'Expected only alpha characters in first name'

    assert tab.middle_name_input is not None, 'Expected Middle Name Input to exist'
    QTest.keyClicks(tab.middle_name_input, 'abc123./')
    assert tab.middle_name_input.text().strip() == 'abc', 'Expected only alpha characters in middle name'

    assert tab.last_name_input is not None, 'Expected Last Name Input to exist'
    QTest.keyClicks(tab.last_name_input, 'abc123./')
    assert tab.last_name_input.text().strip() == 'abc', 'Expected only alpha characters in last name'

def test_address_input(create_new_tab):
    tab = create_new_tab
    assert tab.address_input is not None, 'Expected Address Input to exist'
    QTest.keyClicks(tab.address_input, 'abc123./')
    assert tab.address_input.text().strip() == 'abc123', 'Expected only alphanumeric characters in address'

def test_city_input(create_new_tab):
    tab = create_new_tab
    assert tab.city_input is not None, 'Expected City Input to exist'
    QTest.keyClicks(tab.city_input, 'abc123./')
    assert tab.city_input.text().strip() == 'abc', 'Expected only alpha characters in city'

def test_state_input(create_new_tab):
    tab = create_new_tab
    assert tab.state_input is not None, 'Expected State Input to exist'
    QTest.keyClicks(tab.state_input, 'abc123./')
    assert tab.state_input.text().strip() == 'AB', 'Expected input to be masked and limited to 2 chars'

def test_zip_input(create_new_tab):
    tab = create_new_tab
    assert tab.zip_input is not None, 'Expected ZIP Input to exist'
    QTest.keyClicks(tab.zip_input, 'abc12345./')
    assert tab.zip_input.text().strip() == '12345', 'Expected only numeric values in zip'

def test_product_sections_input(create_new_tab):
    tab = create_new_tab
    assert tab.product_sections is not None, 'Expected Product Sections to exist'
    assert len(tab.product_sections) == 3, 'Expected exactly 3 product sections on start up'

    types = ['Hot Food', 'General', 'Produce']

    for i in range(len(tab.product_sections)):
        assert tab.product_sections[i] is not None, f'Expected Product Section Input [{i}] to exist'
        assert tab.product_sections[i]['product_id'] is not None, f'Expected product id to exist for section[{i}]'
        assert tab.product_sections[i]['product_type'] is not None, f'Expected product type to exist for section[{i}]'
        assert tab.product_sections[i]['rate'] is not None, f'Expected rate field to exist for section[{i}]'
        for j in range(len(types)):
            tab.product_sections[i]['product_type'].setCurrentIndex(j)
            assert tab.product_sections[i]['rate'].text() == str(f"{tab.rates_container[types[j]]}%"), \
                f'Expected rate to be {tab.rates_container[types[j]]} for {types[j]} in section[{i}]'
        assert tab.product_sections[i]['product_name'] is not None, f'Expected product id to exist for section[{i}]'
        assert tab.product_sections[i]['notes'] is not None, f'Expected product id to exist for section[{i}]'
        assert tab.product_sections[i]['price'] is not None, f'Expected product id to exist for section[{i}]'
        assert tab.product_sections[i]['quantity'] is not None, f'Expected product id to exist for section[{i}]'
        assert tab.product_sections[i]['total'] is not None, f'Expected product id to exist for section[{i}]'

    tab.add_product_btn.click()
    assert len(tab.product_sections) == 4, 'Expected exactly 4 product sections after clicking add product once'
    assert tab.product_sections[3] is not None, 'Expected Product Section Input [3] to exist'
    assert tab.product_sections[3]['product_id'] is not None, f'Expected product id to exist for section[3]'
    assert tab.product_sections[3]['product_type'] is not None, f'Expected product id to exist for section[3]'
    assert tab.product_sections[3]['rate'] is not None, f'Expected rate field to exist for section[3]'
    for j in range(len(types)):
        tab.product_sections[3]['product_type'].setCurrentIndex(j)
        assert tab.product_sections[3]['rate'].text() == str(f"{tab.rates_container[types[j]]}%"), \
            f'Expected rate to be {tab.rates_container[types[j]]} for {types[j]} in section[3]'
    assert tab.product_sections[3]['product_name'] is not None, f'Expected product id to exist for section[3]'
    assert tab.product_sections[3]['notes'] is not None, f'Expected product id to exist for section[3]'
    assert tab.product_sections[3]['price'] is not None, f'Expected product id to exist for section[3]'
    assert tab.product_sections[3]['quantity'] is not None, f'Expected product id to exist for section[3]'
    assert tab.product_sections[3]['total'] is not None, f'Expected product id to exist for section[3]'

def test_buttons(create_new_tab):
    tab = create_new_tab
    assert tab.excel_btn is not None, 'Expected Excel Button Input to exist'
    assert tab.pdf_btn is not None, 'Expected Pdf Button Input to exist'
    assert tab.print_btn is not None, 'Expected Print Button Input to exist'

    assert tab.clear_btn is not None, 'Expected Clear Button Input to exist'
    assert tab.create_btn is not None, 'Expected Create Button Input to exist'
    assert tab.export_btn is None, 'Expected Export Button Input to exist when SPOT.OFFLINE is False'

def test_revenue_widgets(create_new_tab):
    tab = create_new_tab
    assert tab.revenue_generation is not None, 'Expected Revenue Generation widget to exist'
    assert tab.rev_by_prod is not None, 'Expected Revenue by Product widget to exist'

