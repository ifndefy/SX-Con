from unittest.mock import patch
import os
import json
import random
from pathlib import Path

from src import SPOT
from src.user import current_user

from ui.main_window import MainWindow
from ui.prompts.login import LoginScreen
from ui.tabs.create_new import CreateNewTab
from ui.core.theme_manager import ThemeManager

from services.delete_item import delete_item
from services.get_max_value import get_max_value
from services.get_item import get_item
from utils.core.generate_pdf import PDF


"""
Sequence:
    ### 1 - offline mode -> should auto move to main window
    ### 2 - main window opens -> lands on create new
        ### only create new tab should be instantiated
    ### 3 - set/emit values into vendor and product fields
    ### 4 - clicks utility buttons (excel, pdf)
        ### they will already trigger calculate button
    ### 5 - click on export record -> successful
    ### 6 - Verify that record exported into json file
    ### 7 - Verify that input values are the same ones exported
    ### 8 - Go online, logout
    ### 9 - Login with valid credentials
    ### 10 - Go to settings tab
    ### 11 - Click on Sync
    ### 12 - Verifies that record now exists in DB
    ### 13 - Delete the inserted items
"""


def test_e2e_pass_offline_porting(app, monkeypatch, tmp_path):
    monkeypatch.setattr(SPOT, 'OFFLINE', True)
    current_user.set_user("offline", False)

    ### 1 - offline mode
    assert current_user.get_username() == "offline"

    ### 2 - main window opens -> lands on create new
    window = MainWindow(offline_mode=True)
    window.show()

    assert isinstance(window.create_new_tab, CreateNewTab)
    assert window.tabs.count() == 1, "Expected only CreateNewTab in offline mode"
    assert window.tabs.tabText(0) == "Create New"
    assert window.tabs.currentIndex() == 0
    assert window.vendor_tickets_tab is None
    assert window.open_tickets_tab is None
    assert window.settings_tab is None
    assert window.admin_settings_tab is None

    ### 3 - set/emit values into vendor and product fields
    currentTab = window.create_new_tab
    v_data = {
        'v_id': random.randint(1000, 9999),
        'phone': '000010110',
        'fname': 'e2e',
        'mname': '',
        'lname': 'test',
        'address': '111 e2e test',
        'city': 'Oakland',
        'state': 'CA',
        'zip': 12345,
    }
    currentTab.vendor_id_input.setText(str(v_data['v_id']))
    currentTab.phone_input.textEdited.emit(v_data['phone'])
    currentTab.first_name_input.setText(v_data['fname'])
    currentTab.middle_name_input.setText(v_data['mname'])
    currentTab.last_name_input.setText(v_data['lname'])
    currentTab.address_input.setText(v_data['address'])
    currentTab.city_input.setText(v_data['city'])
    currentTab.state_input.setText(v_data['state'])
    currentTab.zip_input.setText(str(v_data['zip']))

    product_types = ['Hot Food', 'General', 'Produce']
    p_data = {
        'p_id': random.randint(1000, 9999),
        'type': random.choice(product_types),
        'p_name': "Super Random Product",
        'price': 1234,
        'qty': 10,
    }
    currentTab.product_sections[0]['product_id'].setText(str(p_data['p_id']))
    currentTab.product_sections[0]['product_type'].setCurrentIndex(product_types.index(p_data['type']))
    currentTab.product_sections[0]['product_name'].setText(p_data['p_name'])
    currentTab.product_sections[0]['price'].textEdited.emit(str(p_data['price']))
    assert currentTab.product_sections[0]['price'].text() == "$12.34"
    currentTab.product_sections[0]['quantity'].setText(str(p_data['qty']))

    ### 4 - clicks utility buttons (excel, pdf)
    output_path = os.path.join(os.path.dirname(__file__), "test_e2e_jxl.xlsx")
    with patch("utils.core.generate_excel.QFileDialog.getSaveFileName",
               return_value=(output_path, "Excel File (*.xlsx)")):
        currentTab.excel_btn.click()
    assert os.path.exists(output_path)
    os.remove(output_path)

    pdf_output = os.path.join(os.path.dirname(__file__), "e2e_test.pdf")
    def set_pdf_filename(self):
        self.pdf_filename = pdf_output

    with patch.object(PDF, "set_pdf_filename", set_pdf_filename), \
            patch('ui.tabs.create_new.QMessageBox.information'):
        currentTab.pdf_btn.click()
    assert os.path.exists(pdf_output)
    os.remove(pdf_output)

    ### 5 - click on export record -> successful
    ticket_number = currentTab.ticket_input.text()
    offline_dir = Path(__file__).parent.parent.parent / "utils" / "OFFLINE_tickets"
    with patch('ui.tabs.create_new.QMessageBox.information'):
        currentTab.export_btn.click()

    ### 6 - Verify that record exported into json file
    exported_file = offline_dir / f"{ticket_number}.json"
    assert exported_file.exists()

    ### 7 - Verify that input values are the same ones exported
    record = json.loads(exported_file.read_text())
    assert record['vendor']['vendor_id'] == v_data['v_id']
    assert record['consignment']['ticket_number'] == ticket_number

    ### 8 - Go online, close offline window
    monkeypatch.setattr(SPOT, 'OFFLINE', False)
    window.close()

    ### 9 - Login with valid credentials
    theme_manager = ThemeManager()
    login = LoginScreen(theme_manager)

    login.username_input.setText("user")
    login.password_input.setText("asdf")
    login.login_btn.click()

    assert current_user.get_username() == "user"

    ### 10 - Go to settings tab
    window = MainWindow()
    settings_index = None
    for i in range(window.tabs.count()):
        if window.tabs.tabText(i) == "Settings":
            settings_index = i
            break
    assert settings_index is not None, "Settings tab not found"
    window.tabs.setCurrentIndex(settings_index)

    ### 11 - Click on Sync
    with patch('ui.tabs.settings.QMessageBox.information'):
        window.settings_tab.sync_btn.click()

    ### 12 - Verifies that record now exists in DB
    new_ticket_number = str(get_max_value("Consignments", "ticket_number"))
    result = get_item("Consignments", "consignment", new_ticket_number)
    assert result is not None, f"Expected synced ticket to exist in DB"
    assert result['vendor_id'] == v_data['v_id']

    ### 13 - Delete the items
    delete_item("Consignments", "consignment", new_ticket_number)
    delete_item("Entities", "vendor", v_data['v_id'])
    delete_item("Entities", "product", p_data['p_id'])