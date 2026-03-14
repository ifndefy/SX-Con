from src import SPOT

from ui.tabs import CreateNewTab

def test_export_record_btn_exists(app, monkeypatch):
    monkeypatch.setattr(SPOT, 'OFFLINE', True)
    tab = CreateNewTab(api_handler=None, db_connection=None)
    assert tab.export_btn is not None, "Expected Export Record button to exist"
    assert tab.create_btn is None, "Expected Create Record button to not exist"