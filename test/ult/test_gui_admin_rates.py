import pytest
from unittest.mock import MagicMock
from unittest.mock import patch

from ui.tabs.subtabs.rates import CRTab
from ui.tabs.subtabs.rates import _CREntry

@pytest.fixture
def rates_tab(app):
    fake_api = MagicMock()
    fake_data = {"Hot Food": 30, "General": 25, "Produce": 25}
    with patch('ui.tabs.subtabs.rates.c_table.fetch_consignment_data', return_value=fake_data):
        yield CRTab(fake_api)

def test_cr_entry_count(rates_tab):
    assert len(rates_tab.findChildren(_CREntry)) == 3

def test_cr_entry_values(rates_tab):
    entries = rates_tab.findChildren(_CREntry)
    assert entries[0].get_type() == 'Hot Food', "Expected type to be 'Hot Food' in entry 0"
    assert entries[0].get_rate() == '30', "Expected rate to be '30' in entry 0"
    assert entries[1].get_type() == 'General', "Expected type to be 'General' in entry 1"
    assert entries[1].get_rate() == '25', "Expected rate to be '25' in entry 1"
    assert entries[2].get_type() == 'Produce', "Expected type to be 'Produce' in entry 2"
    assert entries[2].get_rate() == '25', "Expected rate to be '25' in entry 2"