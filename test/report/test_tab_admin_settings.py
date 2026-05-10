import pytest

from handlers.api_handler import APIHandler
from services.connect_database import db_connection
from ui.tabs import AdminSettingsTab
from ui.tabs.subtabs import UsersTab, VendorsTab, ProductsTab
from ui.tabs.subtabs.rates import CRTab
from ui.tabs.subtabs.records import RecordsTab


@pytest.fixture
def admin_setting_tab(app):
    api = APIHandler()
    yield AdminSettingsTab(api, db_connection)

def test_going_through_tabs(admin_setting_tab):
    tab = admin_setting_tab
    assert tab.users_tab is not None, 'Expected user_tab to exist'
    assert tab.vendors_tab is not None, 'Expected vendors_tab to exist'
    assert tab.products_tab is not None, 'Expected products_tab to exist'
    assert tab.records_tab is not None, 'Expected records_tab to exist'
    assert tab.cr_tab is not None, 'Expected cr_tab to exist'

    tab.tabs.setCurrentWidget(tab.users_tab)
    assert isinstance(tab.tabs.currentWidget(), UsersTab), 'Expected user_tab to exist'

    tab.tabs.setCurrentWidget(tab.vendors_tab)
    assert isinstance(tab.tabs.currentWidget(), VendorsTab), 'Expected vendors_tab to exist'

    tab.tabs.setCurrentWidget(tab.products_tab)
    assert isinstance(tab.tabs.currentWidget(), ProductsTab), 'Expected products_tab to exist'

    tab.tabs.setCurrentWidget(tab.records_tab)
    assert isinstance(tab.tabs.currentWidget(), RecordsTab), 'Expected records_tab to exist'

    tab.tabs.setCurrentWidget(tab.cr_tab)
    assert isinstance(tab.tabs.currentWidget(), CRTab), 'Expected cr_tab to exist'
