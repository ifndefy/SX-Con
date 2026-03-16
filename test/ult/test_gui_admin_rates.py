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
    assert entries[0].get_type() == 'Hot Food'
    assert entries[0].get_rate() == '30'
    assert entries[1].get_type() == 'General'
    assert entries[1].get_rate() == '25'
    assert entries[2].get_type() == 'Produce'
    assert entries[2].get_rate() == '25'