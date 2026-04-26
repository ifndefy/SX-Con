import pytest
import pandas as pd
from unittest.mock import patch
from PyQt6.QtTest import QTest
from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtWidgets import QComboBox
from services.connect_database import db_connection

from services.insert_item import insert_item
from services.delete_item import delete_item
from ui.tabs.subtabs.products import ProductsTab
from handlers.api_handler import APIHandler

@pytest.fixture
def test_new_product():
    new_prod_id = 42626
    new_prod_name = "testreport"
    temp_product_data = {
        "product_id" : int(new_prod_id),
        "product_name" : new_prod_name,
        "product_type" : "General"
    }
    insert_item("Entities", "product", temp_product_data)
    yield temp_product_data
    delete_item("Entities", "product", temp_product_data.get("product_id"))

@pytest.fixture
def products_subtab(app):
    api = APIHandler()
    tab = ProductsTab(api, db_connection)
    tab.setup_ui()
    yield tab

def test_search_fields_exist(products_subtab):
    #Test that the subtab has the appropriate elements
    tab = products_subtab
    
    prod_id_field = tab.product_id_input
    prod_name_field = tab.product_name_input
    prod_date_field = tab.last_consignment_input
    prod_type_dropdown = tab.product_type_input

    assert isinstance(prod_id_field, QLineEdit), f"Expected product id field to exist"
    assert isinstance(prod_name_field, QLineEdit), f"Expected product name field to exist"
    assert isinstance(prod_date_field, QLineEdit), f"Expected product date field to exist"
    assert isinstance(prod_type_dropdown, QComboBox), f"Expected product type field to exist"

def test_id_field_input(products_subtab, test_new_product):
    tab = products_subtab
    prod_id_field = tab.product_id_input
    assert prod_id_field is not None, "Expected ID Input to exist"
    
    #Invalid: non-int chars
    QTest.keyClicks(prod_id_field, 'asdf./')
    assert prod_id_field.text() == '', "Expected non-num chars to be filtered"
    assert tab.products_layout.count() == 0, "Expected no tickets for product id: 'asdf./' search"

    #Valid: int ID
    prod_id_field.clear()
    QTest.keyClicks(prod_id_field, str(test_new_product.get("product_id")))
    assert prod_id_field.text() == str(test_new_product.get("product_id")), "Expected valid integer to not be filtered"

    QTest.qWait(400)
    expected = test_new_product.get("product_id")
    assert tab.products_layout.count() > 0, f"Expected ticket(s) for ID: {expected}"

def test_name_field_valid_input(products_subtab, test_new_product):
    tab = products_subtab
    prod_name_field = tab.product_name_input
    assert prod_name_field is not None, "Expected name Input to exist"
    
    #Invalid: ints
    QTest.keyClicks(prod_name_field, '1234654665')
    assert prod_name_field.text() == '', "Expected integer chars to be filtered"
    assert tab.products_layout.count() == 0, "Expected no tickets for product id: 'asdf./' search"

    #Valid: name
    prod_name_field.clear()
    QTest.keyClicks(prod_name_field, test_new_product.get("product_name"))
    assert prod_name_field.text() == test_new_product.get("product_name"), "Expected valid name to not be filtered"

    QTest.qWait(400)

    expected = test_new_product.get("product_name")
    assert tab.products_layout.count() > 0, f"Expected ticket(s) for name: {expected}"

def test_date_field_valid_input(products_subtab):
    tab = products_subtab
    prod_date_field = tab.last_consignment_input
    assert prod_date_field is not None, "Expected Datetime Input to exist"
    
    #Invalid: non-date
    QTest.keyClicks(prod_date_field, 'asdf./')
    QTest.qWait(400)
    assert tab.products_layout.count() == 0, "Expected no tickets for product id: 'asdf./' search"

    #Valid: date
    prod_date_field.clear()
    QTest.keyClicks(prod_date_field, '04/26/26')
    QTest.qWait(400)

    assert tab.products_layout.count() > 0, "Expected ticket(s) for date: 04/26/26"

def test_type_field_valid_input(products_subtab):
    tab = products_subtab
    prod_type_dropdown = tab.product_type_input

    prod_type_dropdown.setCurrentText("General")
    QTest.qWait(400)

    assert tab.products_layout.count() > 0, "Expected ticket(s) for Type: General"

def test_clear_btn(products_subtab, test_new_product):
    tab = products_subtab
    clear_btn = tab.clear_btn
    prod_id_field = tab.product_id_input
    assert clear_btn is not None, "Expected Clear button to exist"
    assert prod_id_field is not None, "Expected ID Input to exist"
    
    prod_id_field.clear()
    QTest.keyClicks(prod_id_field, str(test_new_product.get("product_id")))
    assert prod_id_field.text() == str(test_new_product.get("product_id")), "Expected valid integer to not be filtered"
    QTest.qWait(400)

    assert tab.products_layout.count() > 0, "Expected ticket(s) for ID: 1"

    clear_btn.click()

    assert tab.products_layout.count() == 0, "Expected Layout to be cleared"
