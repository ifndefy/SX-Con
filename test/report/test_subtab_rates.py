import pytest
import pandas as pd
from unittest.mock import patch
from PyQt6.QtTest import QTest

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
        widget = tab.consignments_section_layout.itemAt(i).widget()
        if not isinstance(widget, _CREntry):
            continue
        
        rate_field = widget.product_rate_input
        type_field = widget.product_type_input

        expected_rate = fake_data.get("Rate")[ticket_count]
        expected_type = fake_data.get("Type")[ticket_count]

        assert rate_field.text() == expected_rate, f"Rate for ticket {ticket_count} does not accurately reflect entry in table, Expected: {expected_rate} Actual: {rate_field.text()}"
        assert type_field.text() == expected_type, f"Type for ticket {ticket_count}  does not accurately reflect entry in table, Expected: {expected_type} Actual: {type_field.text()}"
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

    for i in range(tab.consignments_section_layout.count()):
        widget = tab.consignments_section_layout.itemAt(i).widget()
        if not isinstance(widget, _CREntry):
            continue
        
        #Fetch the appropriate subwidgets for the test
        edit_btn = widget.entry_edit_btn
        cancel_btn = widget.edit_cancel_btn
        save_btn = widget.edit_save_btn
        rate_field = widget.product_rate_input

        #Simulate Click
        edit_btn.click()

        #First, check the state of the field
        assert not rate_field.isReadOnly(), f"Rate Field for Entry {i} in Layout did not toggle to Read-Write on click"

        #Check that the buttons were properly swapped
        assert edit_btn.isHidden(), f"Edit button for Entry {i} in Layout did not toggle visibility to hidden"
        assert not cancel_btn.isHidden(), f"Cancel button for Entry {i} in Layout did not toggle visibility to visible"
        assert not save_btn.isHidden(), f"Save button for Entry {i} in Layout did not toggle visibility to visible"

def test_save_btn_valid_update(rates_tab):
    #Test that save btn updates SPOT.csv on valid entry, turns over btns to correct state
    tab = rates_tab

    #Grab the first ticket object we find
    for i in range(tab.consignments_section_layout.count()):
        widget = tab.consignments_section_layout.itemAt(i).widget()
        if isinstance(widget, _CREntry):
            break
    
    #Fetch the appropriate subwidgets for the test
    edit_btn = widget.entry_edit_btn
    cancel_btn = widget.edit_cancel_btn
    save_btn = widget.edit_save_btn
    rate_field = widget.product_rate_input
    
    #Simulate Click
    edit_btn.click()

    rate_field.setText("25")

    #Simulate Save Click and make sure we don't actually write anything to file
    with patch("ui.tabs.subtabs.rates._write_to_spot_csv", return_value = None) as mock_to_csv:
        save_btn.click()
        mock_to_csv.assert_called()

        passed_data = mock_to_csv.call_args[0][0]
        expected_arg = {'type' : fake_data.get("Type")[0], 'rate' : "25"}

        #check that the value we are writing to csv matches the expected type and rate
        assert passed_data == expected_arg, f"Expected {expected_arg} to be passed to csv writer, Actual: {passed_data}"

    #Check that the buttons were properly swapped
    assert not edit_btn.isHidden(), f"Edit button for Entry 0 in Layout did not toggle visibility to visible"
    assert cancel_btn.isHidden(), f"Cancel button for Entry 0 in Layout did not toggle visibility to hidden"
    assert save_btn.isHidden(), f"Save button for Entry 0 in Layout did not toggle visibility to hidden"

def test_save_btn_invalid_empty_string(rates_tab):
    #Test that save btn rejects invalid field state, does not change state
    tab = rates_tab

    #Grab the first ticket object we find
    for i in range(tab.consignments_section_layout.count()):
        widget = tab.consignments_section_layout.itemAt(i).widget()
        if isinstance(widget, _CREntry):
            break
    
    #Fetch the appropriate subwidgets for the test
    edit_btn = widget.entry_edit_btn
    cancel_btn = widget.edit_cancel_btn
    save_btn = widget.edit_save_btn
    rate_field = widget.product_rate_input
    
    #Simulate Click
    edit_btn.click()
    
    #Set Text to None
    rate_field.setText("")

    #Simulate Save Click and make sure we don't write anything to file
    with patch("ui.tabs.subtabs.rates._write_to_spot_csv", return_value = None) as mock_to_csv:
        save_btn.click()
        mock_to_csv.assert_not_called()

    #Check that the buttons remained in place
    assert edit_btn.isHidden(), f"Edit button for Entry 0 in Layout did not remain hidden"
    assert not cancel_btn.isHidden(), f"Cancel button for Entry 0 in Layout did not remain visible"
    assert not save_btn.isHidden(), f"Save button for Entry 0 in Layout did not remain visible"

def test_cancel_btn(rates_tab):
    #Test that cancel reverts field back to original state, swaps btn state properly
    tab = rates_tab

    #Grab the first ticket object we find
    for i in range(tab.consignments_section_layout.count()):
        widget = tab.consignments_section_layout.itemAt(i).widget()
        if isinstance(widget, _CREntry):
            break
    
    #Fetch the appropriate subwidgets for the test
    edit_btn = widget.entry_edit_btn
    cancel_btn = widget.edit_cancel_btn
    save_btn = widget.edit_save_btn
    rate_field = widget.product_rate_input

    #Simulate Click
    edit_btn.click()

    old_value = rate_field.text()

    rate_field.setText("99")

    cancel_btn.click()

    assert rate_field.text() == old_value, f"Field was not reset to {old_value} on cancel"
    
    #Check that the buttons were properly swapped
    assert not edit_btn.isHidden(), f"Edit button for Entry 0 in Layout did not toggle visibility to visible"
    assert cancel_btn.isHidden(), f"Cancel button for Entry 0 in Layout did not toggle visibility to hidden"
    assert save_btn.isHidden(), f"Save button for Entry 0 in Layout did not toggle visibility to hidden"

def test_rate_input_filter_char(rates_tab):
    #Test that field editing filters out chars, does not add to field
    tab = rates_tab
    expected = ""

    #Grab the first ticket object we find
    for i in range(tab.consignments_section_layout.count()):
        widget = tab.consignments_section_layout.itemAt(i).widget()
        if isinstance(widget, _CREntry):
            break
    
    #Fetch the appropriate subwidgets for the test
    edit_btn = widget.entry_edit_btn
    rate_field = widget.product_rate_input

    #Simulate Click to make field editable
    edit_btn.click()

    #Clear Field to test only filtering
    rate_field.setText("")
    QTest.keyClicks(rate_field, "asdf")
    
    assert rate_field.text() == expected, f"rate_field value did not filter properly. Expected: {expected} Actual: {rate_field.text()}"

def test_rate_input_filter_valid_nums(rates_tab):
    #Test that field editing accepts valid nums
    tab = rates_tab
    expected = "10"

    #Grab the first ticket object we find
    for i in range(tab.consignments_section_layout.count()):
        widget = tab.consignments_section_layout.itemAt(i).widget()
        if isinstance(widget, _CREntry):
            break
    
    #Fetch the appropriate subwidgets for the test
    edit_btn = widget.entry_edit_btn
    rate_field = widget.product_rate_input

    #Simulate Click to make field editable
    edit_btn.click()

    #Clear Field to test only filtering
    rate_field.setText("")
    QTest.keyClicks(rate_field, "10")
    
    assert rate_field.text() == expected, f"rate_field value did not filter properly. Expected: {expected} Actual: {rate_field.text()}"

def test_rate_input_filter_mixed_input(rates_tab):
    #Test that field editing accepts correctly parses mixed inputs and only keeps numbers
    tab = rates_tab
    expected = "10"

    #Grab the first ticket object we find
    for i in range(tab.consignments_section_layout.count()):
        widget = tab.consignments_section_layout.itemAt(i).widget()
        if isinstance(widget, _CREntry):
            break
    
    #Fetch the appropriate subwidgets for the test
    edit_btn = widget.entry_edit_btn
    rate_field = widget.product_rate_input

    #Simulate Click to make field editable
    edit_btn.click()

    #Clear Field to test only filtering
    rate_field.setText("")
    QTest.keyClicks(rate_field, "as1df0")
    
    assert rate_field.text() == expected, f"rate_field value did not filter properly. Expected: {expected} Actual: {rate_field.text()}"

def test_rate_input_filter_shift_num(rates_tab):
    #Test that field editing accepts does not accept special chars with same key as nums
    tab = rates_tab
    expected = ""

    #Grab the first ticket object we find
    for i in range(tab.consignments_section_layout.count()):
        widget = tab.consignments_section_layout.itemAt(i).widget()
        if isinstance(widget, _CREntry):
            break
    
    #Fetch the appropriate subwidgets for the test
    edit_btn = widget.entry_edit_btn
    rate_field = widget.product_rate_input

    #Simulate Click to make field editable
    edit_btn.click()

    #Clear Field to test only filtering
    rate_field.setText("")
    QTest.keyClicks(rate_field, "!)")
    
    assert rate_field.text() == expected, f"rate_field value did not filter properly. Expected: {expected} Actual: {rate_field.text()}"

