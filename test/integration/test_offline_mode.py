from src import SPOT
from src.user import current_user
from ui.main_window import MainWindow

def test_offline_user_cpy_flow(app, monkeypatch):
    monkeypatch.setattr(SPOT, 'OFFLINE', True)
    current_user.set_user("offline", False)
    window = MainWindow(offline_mode=True)
    assert current_user.get_username() == "offline", "Expected current_user to be 'offline'"

def test_offline_tab_count(app, monkeypatch):
    monkeypatch.setattr(SPOT, 'OFFLINE', True)
    window = MainWindow(offline_mode=True)
    assert window.tabs.count() == 1, "Expected only 1 tab in offline mode"