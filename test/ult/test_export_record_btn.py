import os
from unittest.mock import patch
import json

from src import SPOT

from ui.tabs import CreateNewTab

def test_export_record_btn_exists(app, monkeypatch):
    monkeypatch.setattr(SPOT, 'OFFLINE', True)
    tab = CreateNewTab(api_handler=None, db_connection=None)
    assert tab.export_btn is not None, "Expected Export Record button to exist"
    assert tab.create_btn is None, "Expected Create Record button to not exist"


def test_export_record_btn_works(app, monkeypatch):
    monkeypatch.setattr(SPOT, 'OFFLINE', True)
    tab = CreateNewTab(api_handler=None, db_connection=None)
    tab.vendor_id_input.setText("100")
    tab.vendor_id_input.returnPressed.emit()

    tab.phone_input.setText("1920384298")
    tab.phone_input.textEdited.emit("1920384298")
    tab.first_name_input.setText("asdf")
    tab.last_name_input.setText("asdf")
    tab.address_input.setText("1234 asdf asfs")
    tab.city_input.setText("asdf fdsa")
    tab.state_input.setText("CA")
    tab.zip_input.setText("12345")

    sec = tab.product_sections[0]
    sec['product_id'].setText("1")
    sec['product_id'].returnPressed.emit()

    sec['product_id'].setText("100")
    sec['product_type'].setCurrentIndex(0)
    sec['product_name'].setText("asdf")
    sec['price'].textEdited.emit('1234')
    sec['quantity'].setText("12")

    ticket = tab.ticket_input.text().strip()
    with patch('ui.tabs.create_new.QMessageBox'), \
        patch('validate.val_check_does_not_exist.get_item_by_property', return_value=None):
            tab.export_btn.click()

    offline_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath("utils/core/export_doc.py"))), "OFFLINE_tickets")
    expected_path = os.path.join(offline_dir, f"{ticket}.json")
    assert os.path.exists(expected_path), f"Expected exported file at {expected_path}"

    with open(expected_path, 'r') as f:
        data = json.load(f)

    assert data['vendor']['vendor_id'] == 100, "Expected vendor ID to be 100"
    assert data['vendor']['first_name'] == "asdf", "Expected vendor first name to be asdf"
    assert data['vendor']['last_name'] == "asdf", "Expected vendor last name to be asdf"

    prod = data['product'][0]
    assert prod['product_id'] == 100, "Expected product ID to be 100"
    assert prod['product_type'] == "Hot Food", "Expected product type to be Hot Food"
    assert prod['product_name'] == "asdf", "Expected product name to be asdf"
    assert prod['price'] == 12.34, "Expected price to be 12.34"
    assert prod['quantity'] == 12, "Expected quantity to be 12"

    os.remove(expected_path)