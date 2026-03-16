import pytest
from unittest.mock import MagicMock

from PyQt6.QtTest import QTest

from ui.tabs.subtabs.products import ProductsTab

@pytest.fixture
def products_tab(app):
    fake_api = MagicMock()
    fake_db = MagicMock()
    yield ProductsTab(fake_api, fake_db)

def test_product_id_input(products_tab):
    tab = products_tab
    assert tab.product_id_input is not None, 'Expected Vendor ID Input to exist'
    QTest.keyClicks(tab.product_id_input, 'abc123./') # don't put commas
    assert tab.product_id_input.text() == '123', 'Expected only integers to be accepted'

def test_product_type_input(products_tab):
    tab = products_tab
    types = ['Hot Food', 'General', 'Produce']
    assert tab.product_type_input.count() == len(types)
    for i in range(len(types)):
        assert tab.product_type_input.itemText(i) == types[i]

def test_product_name(products_tab):
    tab = products_tab
    assert tab.product_name_input is not None, 'Expected First Name Input to exist'
    QTest.keyClicks(tab.product_name_input, 'abc123./')
    assert tab.product_name_input.text().strip() == 'abc', 'Expected only alpha characters in first name'

def test_button_exists(products_tab):
    tab = products_tab
    assert tab.create_btn is not None, 'Expected Create New Product button to exist'
    assert tab.clear_btn is not None, 'Expected Clear button to exist'
    assert tab.search_btn is not None, 'Expected Search button to exist'