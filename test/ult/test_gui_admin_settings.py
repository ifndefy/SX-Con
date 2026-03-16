import pytest
from unittest.mock import MagicMock
from unittest.mock import patch

from ui.tabs.admin_settings import AdminSettingsTab

@pytest.fixture
def admin_tab_online(app):
    fake_api = MagicMock()
    fake_db = MagicMock()
    with patch('ui.tabs.admin_settings.SPOT') as fake_spot:
        fake_spot.OFFLINE = False
        yield AdminSettingsTab(fake_api, fake_db)

@pytest.fixture
def admin_tab_offline(app):
    fake_api = MagicMock()
    fake_db = MagicMock()
    with patch('ui.tabs.admin_settings.SPOT') as fake_spot:
        fake_spot.OFFLINE = True
        yield AdminSettingsTab(fake_api, fake_db)

def test_online_subtab_count(admin_tab_online):
    assert admin_tab_online.tabs.count() == 5

def test_offline_subtab_count(admin_tab_offline):
    assert admin_tab_offline.tabs.count() == 1