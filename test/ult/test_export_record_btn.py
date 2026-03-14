import os
from unittest.mock import patch

from src import SPOT

from ui.tabs import CreateNewTab

def test_export_record_btn_exists(app, monkeypatch):
    monkeypatch.setattr(SPOT, 'OFFLINE', True)
    tab = CreateNewTab(api_handler=None, db_connection=None)
    assert tab.export_btn is not None, "Expected Export Record button to exist"
    assert tab.create_btn is None, "Expected Create Record button to not exist"

import json

def test_export_record_btn_works(app, monkeypatch):
    monkeypatch.setattr(SPOT, 'OFFLINE', True)
    tab = CreateNewTab(api_handler=None, db_connection=None)
    tab.vendor_id_input.setText("1")
    tab.vendor_id_input.returnPressed.emit()

    tab.first_name_input.setText("Test")
    tab.last_name_input.setText("ABCDE")

    sec = tab.product_sections[0]
    sec['product_id'].setText("1")
    sec['product_id'].returnPressed.emit()

    sec['product_type'].setCurrentText("Hot Food")
    sec['product_name'].setText("Not Hot food")
    sec['price'].textEdited.emit('1234')
    sec['quantity'].setText("12")

    ticket = tab.ticket_input.text().strip()
    with patch('ui.tabs.create_new.QMessageBox'):
        tab.export_btn.click()

    offline_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath("utils/core/export_doc.py"))), "OFFLINE_tickets")
    expected_path = os.path.join(offline_dir, f"{ticket}.json")
    assert os.path.exists(expected_path), f"Expected exported file at {expected_path}"

    with open(expected_path, 'r') as f:
        data = json.load(f)

    assert data['vendor']['vendor_id'] == 1
    assert data['vendor']['first_name'] == "Test"
    assert data['vendor']['last_name'] == "ABCDE"

    prod = data['product'][0]
    assert prod['product_id'] == 1
    assert prod['product_type'] == "Hot Food"
    assert prod['product_name'] == "not hot food"
    assert prod['price'] == 12.34
    assert prod['quantity'] == 12

    os.remove(expected_path)