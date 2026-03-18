import pytest
from unittest.mock import MagicMock

from ui.tabs.search_tickets import SearchTicketsTab

@pytest.fixture
def search_tickets_tab(app):
    fake_api = MagicMock()
    fake_db = MagicMock()
    yield SearchTicketsTab(fake_api, fake_db)

def test_btns_exist(search_tickets_tab):
    tab = search_tickets_tab
    tab.clear_btn is not None, "Expectec clear button to exist"
    tab.search_btn is not None, "Expectec search btn to exist"
