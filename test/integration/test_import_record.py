from unittest.mock import patch

from src import SPOT
from ui.tabs import CreateNewTab
from ui.tabs import SettingsTab
from utils.core.import_doc import import_offline_records
from services.get_item_by_property import get_item_by_property
from services.get_max_value import get_max_value

def test_export_then_import(app, monkeypatch):
    monkeypatch.setattr(SPOT, 'OFFLINE', True)
    tab = CreateNewTab(api_handler=None, db_connection=None)
    tab.vendor_id_input.setText("1")
    tab.first_name_input.setText("Test")
    tab.last_name_input.setText("ABCDE")

    sec = tab.product_sections[0]
    sec['product_id'].setText("1")
    sec['product_type'].setCurrentText("Hot Food")
    sec['product_name'].setText("Not Hot food")
    sec['price'].textEdited.emit('1234')
    sec['quantity'].setText("12")

    with patch('ui.tabs.create_new.QMessageBox'):
        tab.export_btn.click()

    monkeypatch.setattr(SPOT, 'OFFLINE', False)
    import_offline_records()

    result = get_item_by_property("Consignments", "consignment", "ticket_number", int(get_max_value("Consignments", "ticket_number")))
    assert result is not None
    assert result['vendor_id'] == 1
    assert result['status'] == "OPEN"
    assert len(result['products']) == 1
    assert result['products'][0]['product_name'] == "not hot food"
    assert result['products'][0]['quantity'] == 12

def test_sync_btn_import(app, monkeypatch):
    monkeypatch.setattr(SPOT, 'OFFLINE', True)
    tab = CreateNewTab(api_handler=None, db_connection=None)
    tab.vendor_id_input.setText("1")
    tab.first_name_input.setText("Test")
    tab.last_name_input.setText("ABCDE")

    sec = tab.product_sections[0]
    sec['product_id'].setText("1")
    sec['product_type'].setCurrentText("Hot Food")
    sec['product_name'].setText("Not Hot food")
    sec['price'].textEdited.emit('1234')
    sec['quantity'].setText("12")

    with patch('ui.tabs.create_new.QMessageBox'):
        tab.export_btn.click()

    monkeypatch.setattr(SPOT, 'OFFLINE', False)
    with patch('ui.tabs.settings.QMessageBox'):
        settings_tab = SettingsTab(api_handler=None)
        with patch('ui.tabs.settings.QMessageBox'):
            settings_tab.sync_btn.click()

    result = get_item_by_property("Consignments", "consignment", "ticket_number", int(get_max_value("Consignments", "ticket_number")))
    assert result is not None
    assert result['vendor_id'] == 1
    assert result['status'] == "OPEN"
    assert len(result['products']) == 1
    assert result['products'][0]['product_name'] == "not hot food"
    assert result['products'][0]['quantity'] == 12