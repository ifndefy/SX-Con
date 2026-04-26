import os
import pytest
import re
from PyQt6.QtCore import Qt
from PyQt6.QtTest import QTest
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtWidgets import QPushButton
from unittest.mock import patch
import pandas as pd

from ui.tabs.subtabs.rates import CRTab
from ui.tabs.subtabs.rates import _CREntry
from handlers.api_handler import APIHandler

fake_data = {
        "Type": ["test01","test02","test03"],
        "Rate": ["0", "10", "20"]
    }

@pytest.fixture
def rates_tab(app):
    with patch("pandas.read_csv", return_value = pd.DataFrame(fake_data)):
        api = APIHandler()
        tab = CRTab(api)
        tab.setup_ui()
        yield tab

def test_entries_exist(rates_tab):
    #Test that entries exist/ allign with test SPOT.csv    
    tab = rates_tab
    
    ticket_count = 0
    data_count = len(fake_data.get("Type"))

    for i in range(tab.consignments_section_layout.count()):
        if isinstance(tab.consignments_section_layout.itemAt(i).widget(), _CREntry):
            ticket_count += 1
    assert ticket_count == data_count, f"Ticket section does not accurately reflect entries in table, Expected: {data_count} Actual: {ticket_count}"

def test_rates_readonly(rates_tab):
    #Test that rates field is readonly
    tab = rates_tab
    
    for i in range(tab.consignments_section_layout.count()):
        widget = tab.consignments_section_layout.itemAt(i).widget()

        if not isinstance(widget, _CREntry):
            continue
        
        rate_field = widget.product_rate_input
        type_field = widget.product_type_input

        assert rate_field.isReadOnly() , f"Rate Field for Entry {i} in Layout was not initialized as Read-Only"
        assert type_field.isReadOnly() , f"Type Field for Entry {i} in Layout was not initialized as Read-Only"

def test_edit_btn_toggle(rates_tab):
    #Test that edit button toggles the field and swaps with cancel and save btns
    tab = rates_tab
    pass

def test_save_btn_valid_update(rates_tab):
    #Test that save btn updates SPOT.csv on valid entry, turns over btns to correct state
    tab = rates_tab
    pass

def test_save_btn_invalid_none(rates_tab):
    #Test that save btn rejects invalid field state, does not change state
    tab = rates_tab
    pass

def test_cancel_btn(rates_tab):
    #Test that cancel reverts field back to original state, swaps btn state properly
    tab = rates_tab
    pass

def test_rate_input_filter_char(rates_tab):
    #Test that field editing filters out chars, does not add to field
    tab = rates_tab
    pass

def test_rate_input_filter_valid_nums(rates_tab):
    #Test that field editing accepts valid nums
    tab = rates_tab
    pass

def test_rate_input_filter_mixed_input(rates_tab):
    #Test that field editing accepts correctly parses mixed inputs and only keeps numbers
    tab = rates_tab
    pass

def test_rate_input_filter_shift_num(rates_tab):
    #Test that field editing accepts does not accept special chars with same key as nums
    tab = rates_tab
    pass

