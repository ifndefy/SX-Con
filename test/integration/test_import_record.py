from unittest.mock import patch
from pathlib import Path
from src import SPOT
from src.user import current_user
from ui.tabs import CreateNewTab
from ui.tabs import SettingsTab
from services.delete_item import delete_item
from services.get_item_by_property import get_item_by_property
from services.get_max_value import get_max_value

def test_export(app, monkeypatch):
    monkeypatch.setattr(SPOT, 'OFFLINE', True)
    tab = CreateNewTab(api_handler=None, db_connection=None)
    tab.vendor_id_input.setText("100")
    tab.phone_input.setText("1920384298")
    tab.phone_input.textEdited.emit("1920384298")
    tab.first_name_input.setText("asdf")
    tab.last_name_input.setText("asdf")
    tab.address_input.setText("1234 asdf asfs")
    tab.city_input.setText("asdf fdsa")
    tab.state_input.setText("CA")
    tab.zip_input.setText("12345")

    sec = tab.product_sections[0]
    sec['product_id'].setText("100")
    sec['product_type'].setCurrentIndex(0)
    sec['product_name'].setText("asdf")
    sec['price'].textEdited.emit('1234')
    sec['quantity'].setText("12")

    ticket_number = tab.ticket_input.text()

    with patch('ui.tabs.create_new.QMessageBox'):
        tab.export_btn.click()

    offline_dir = Path(__file__).parent.parent.parent / "utils" / "OFFLINE_tickets"
    exported_file = offline_dir / f"{ticket_number}.json"
    assert exported_file.exists(), f"Expected exported file at {exported_file}"

def test_sync_btn_import(app, monkeypatch):
    monkeypatch.setattr(SPOT, 'OFFLINE', False)
    monkeypatch.setattr(current_user, "_raw_username", "user")
    tab = SettingsTab(api_handler=None)

    with patch('ui.tabs.settings.QMessageBox'):
        tab.sync_btn.click()

    ticket_number = int(get_max_value("Consignments", "consignment_id"))
    result = get_item_by_property("Consignments", "consignment", "consignment_id", ticket_number)
    assert result is not None, "Expected there to be a successful import"
    assert result['vendor_id'] == 100, "Expected the vendor ID to be 1"
    assert result['status'] == "OPEN", "Expected the ticket to be in open state"
    assert len(result['products']) == 1, "Expected there to be 1 product"
    assert result['products'][0]['price'] == 12.34, "Expected the price to be 12.34"
    assert result['products'][0]['quantity'] == 12, "Expected the quantity to be 12"

    delete_item("Consignments", "consignment", str(ticket_number))
    delete_item("Entities", "vendor", str(100))
    delete_item("Entities", "product", str(100))