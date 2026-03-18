import pytest
from unittest.mock import MagicMock

from ui.tabs.open_tickets import OpenTicketsTab

@pytest.fixture
def open_tickets_tab(app):
    fake_api = MagicMock()
    fake_db = MagicMock()
    yield OpenTicketsTab(fake_api, fake_db)

def test_btns_exist(open_tickets_tab):
    tab = open_tickets_tab

    assert tab.update_btn is not None, 'Expected update button to exist'