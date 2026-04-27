import pytest
from unittest.mock import patch
from PyQt6.QtTest import QTest
from PyQt6.QtWidgets import QDialog
from PyQt6.QtCore import QTimer
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

def test_search_button(products_subtab):
    tab = products_subtab
    search_btn = tab.search_btn
    clear_btn = tab.clear_btn

    assert search_btn is not None, "Expected Search button to exist"
    assert clear_btn is not None, "Expected Clear button to exist"

    clear_btn.click()

    assert tab.products_layout.count() == 0, "Expected no tickets in a cleared tab"

    search_btn.click()
    QTest.qWait(400)

    assert tab.products_layout.count() > 0, "Expected ticket(s) to be fetched on empty input"

def test_edit_save_btn(products_subtab, test_new_product):
    tab = products_subtab
    prod_id_field = tab.product_id_input
    prod_id_field.clear()

    QTest.keyClicks(prod_id_field, str(test_new_product.get("product_id")))
    QTest.qWait(400)

    assert tab.products_layout.count() > 0, "Expected to have at least one result"

    tickets = []
    for i in range(tab.products_layout.count()):
        item = tab.products_layout.itemAt(i)
        widget = item.widget()
        if widget is not None:
            tickets.append(widget)

    ticket_row_3 = tickets[0].layout().itemAt(2).layout()

    edit_btn = ticket_row_3.itemAt(0).widget()
    assert edit_btn is not None, "Expected Edit button to exist"

    edit_btn.click()
    assert edit_btn.text() == "Save", "Expected to switch to save button"

    edit_btn.click()
    assert edit_btn.text() == "Edit", "Expected to switch back to edit button"

def test_edit_product_name(products_subtab, test_new_product):
    tab = products_subtab
    prod_id_field = tab.product_id_input
    prod_id_field.clear()

    QTest.keyClicks(prod_id_field, str(test_new_product.get("product_id")))
    QTest.qWait(400)

    assert tab.products_layout.count() > 0, "Expected to have at least one result"

    tickets = []
    for i in range(tab.products_layout.count()):
        item = tab.products_layout.itemAt(i)
        widget = item.widget()
        if widget is not None:
            tickets.append(widget)

    ticket_row_1 = tickets[0].layout().itemAt(0).layout()
    ticket_row_3 = tickets[0].layout().itemAt(2).layout()

    edit_btn = ticket_row_3.itemAt(0).widget()
    assert edit_btn is not None, "Expected Edit button to exist"

    edit_btn.click()

    prod_edit_name_field = ticket_row_1.itemAt(3).widget()

    #Valid: chars
    assert prod_edit_name_field is not None, "Expected Name Input to exist"
    assert prod_edit_name_field.text() == "testreport", "Expected to grab the product name"

    prod_edit_name_field.clear()
    assert prod_edit_name_field.text() == "", "Expected Name Input be cleared"

    QTest.keyClicks(prod_edit_name_field, str("testreport"))
    assert prod_edit_name_field.text() == "testreport", "Expected Name Input to be changed"

    #Invalid: Ints
    prod_edit_name_field.clear()
    assert prod_edit_name_field.text() == "", "Expected Name Input be cleared"

    QTest.keyClicks(prod_edit_name_field, str("123456"))
    assert prod_edit_name_field.text() == "", "Expected Name Input to be ignored"

    edit_btn.click()

def test_create_new_product_btn(products_subtab, test_new_product):
    tab = products_subtab
    create_new_product_btn = tab.create_btn

    assert create_new_product_btn is not None, "Expected create new product btn to exist"

    with patch('ui.tabs.subtabs.products.QDialog') as mock_dialog, \
            patch('ui.tabs.subtabs.products.ProductsTab') as mock_tab:
        mock_tab.create_btn.click()

        assert mock_dialog.create_btn is not None, "Expected to be able to create new product"
        assert mock_dialog.cancel_btn is not None, "Expect to be able to cancel create new product"

def test_create_new_product_id_valid(products_subtab, test_new_product):
    tab = products_subtab

    #valid: int
    def populate():
        create_product_dialog = tab.findChild(QDialog)

        QTest.keyClicks(create_product_dialog.findChild(QLineEdit, "product_id_input"), str(test_new_product.get("product_id")))
        QTest.keyClicks(create_product_dialog.findChild(QLineEdit, "product_name_input"), str(test_new_product.get("product_name")))
        create_product_dialog.findChild(QComboBox, "product_type_input").setCurrentIndex(1)

        assert create_product_dialog.findChild(QLineEdit, "product_id_input").text() == str(test_new_product.get("product_id")), "Expected new product ID to be entered"

        create_product_dialog.reject()

    with patch("ui.tabs.subtabs.products.QMessageBox"):
        QTimer.singleShot(0, populate)
        tab.create_btn.click()

def test_create_new_product_id_invalid(products_subtab, test_new_product):
    tab = products_subtab

    #invalid: char
    def populate():
        create_product_dialog = tab.findChild(QDialog)

        QTest.keyClicks(create_product_dialog.findChild(QLineEdit, "product_id_input"), str("asdf./"))
        QTest.keyClicks(create_product_dialog.findChild(QLineEdit, "product_name_input"), str(test_new_product.get("product_name")))
        create_product_dialog.findChild(QComboBox, "product_type_input").setCurrentIndex(1)

        assert create_product_dialog.findChild(QLineEdit, "product_id_input").text() == "", "Expected attempted input to be cleared"

        create_product_dialog.reject()

    with patch("ui.tabs.subtabs.products.QMessageBox"):
        QTimer.singleShot(0, populate)
        tab.create_btn.click()

def test_create_new_product_name_valid(products_subtab, test_new_product):
    tab = products_subtab

    #valid: char
    def populate():
        create_product_dialog = tab.findChild(QDialog)

        QTest.keyClicks(create_product_dialog.findChild(QLineEdit, "product_id_input"), str(test_new_product.get("product_id")))
        QTest.keyClicks(create_product_dialog.findChild(QLineEdit, "product_name_input"), str(test_new_product.get("product_name")))
        create_product_dialog.findChild(QComboBox, "product_type_input").setCurrentIndex(1)

        assert create_product_dialog.findChild(QLineEdit, "product_name_input").text() == str(test_new_product.get("product_name")), "Expected new product name to be entered"

        create_product_dialog.reject()

    with patch("ui.tabs.subtabs.products.QMessageBox"):
        QTimer.singleShot(0, populate)
        tab.create_btn.click()

def test_create_new_product_name_invalid(products_subtab, test_new_product):
    tab = products_subtab

    #invalid: int
    def populate():
        create_product_dialog = tab.findChild(QDialog)

        QTest.keyClicks(create_product_dialog.findChild(QLineEdit, "product_id_input"), str(test_new_product.get("product_id")))
        QTest.keyClicks(create_product_dialog.findChild(QLineEdit, "product_name_input"), str("123456"))
        create_product_dialog.findChild(QComboBox, "product_type_input").setCurrentIndex(1)

        assert create_product_dialog.findChild(QLineEdit, "product_name_input").text() == "", "Expected attempted input to be cleared"

        create_product_dialog.reject()

    with patch("ui.tabs.subtabs.products.QMessageBox"):
        QTimer.singleShot(0, populate)
        tab.create_btn.click()