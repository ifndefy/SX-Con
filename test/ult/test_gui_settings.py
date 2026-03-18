import pytest
from unittest.mock import MagicMock
from unittest.mock import patch

from ui.tabs.settings import SettingsTab

@pytest.fixture
def settings_tab(app):
    fake_api = MagicMock()
    fake_db = MagicMock()
    with patch('ui.tabs.settings.current_user') as test_user, \
         patch.object(SettingsTab, 'get_user_id_from_username', return_value=999):
        test_user.get_username.return_value = 'test_user'
        test_user.is_admin.return_value = True
        yield SettingsTab(fake_api, fake_db)

def test_btns_exist(settings_tab):
    tab = settings_tab

    assert tab.theme_dropdown_menu is not None, 'Expected Theme dropdown menu to exist'
    assert tab.current_username_input.text().strip() == 'test_user'
    assert tab.change_username_btn is not None, 'Expected Change Usenrame button to exist'
    assert tab.change_pw_btn is not None, 'Expected Change Password button to exist'
    assert tab.change_qa_btn is not None, 'Expected Change Q/A button to exist'
    assert tab.sync_btn is not None, 'Expected Sync Offline Tickets to exist'
    assert tab.load_btn is not None, 'Expected Load Settings button to exist'
    assert tab.save_btn is not None, 'Expected Save Settings button to exist'