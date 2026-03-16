import pytest
from unittest.mock import MagicMock

from PyQt6.QtTest import QTest

from ui.tabs.subtabs.users import UsersTab

@pytest.fixture
def users_tab(app):
    fake_api = MagicMock()
    fake_db = MagicMock()
    yield UsersTab(fake_api, fake_db)

def test_user_id(users_tab):
    tab = users_tab
    tab.user_id_input is not None, 'Expected user_id field to exist'
    QTest.keyClicks(tab.user_id_input, 'abc123./')
    assert tab.user_id_input.text() == '123', 'Expected user_id_input to only accept integers'

def test_username(users_tab):
    tab = users_tab
    tab.username_input is not None, 'Expected username field to exist'
    QTest.keyClicks(tab.username_input, 'abc123.')
    assert tab.username_input.text() == 'abc', 'Expected username to only accept alphanumeric characters'

def test_last_consignment(users_tab):
    tab = users_tab
    tab.last_consignment_input is not None, 'Expected last_consignment field to exist'

def test_first_name(users_tab):
    tab = users_tab
    tab.first_name_input is not None, 'Expected first name field to exist'
    QTest.keyClicks(tab.first_name_input, 'abc123.')
    assert tab.first_name_input.text() == 'abc', 'Expected first_name_input to only accept alpha characters'

def test_last_name(users_tab):
    tab = users_tab
    tab.last_name_input is not None, 'Expected last name field to exist'
    QTest.keyClicks(tab.last_name_input, 'abc123.')
    assert tab.last_name_input.text() == 'abc', 'Expected last_name_input to only accept alpha characters'

def test_admin(users_tab):
    tab = users_tab
    assert tab.admin_field is not None, 'Expected admin input to exist'
    assert tab.admin_field.count() == 2
    assert tab.admin_field.itemText(0) == 'True'
    assert tab.admin_field.itemText(1) == 'False'

def test_button_exists(users_tab):
    tab = users_tab
    assert tab.create_btn is not None, 'Expected Create New User button to exist'
    assert tab.clear_btn is not None, 'Expected Clear button to exist'
    assert tab.search_btn is not None, 'Expected Search button to exist'