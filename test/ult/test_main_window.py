import pytest
from unittest.mock import MagicMock
from unittest.mock import patch

import os
from PyQt6.QtWidgets import QWidget
from ui.main_window import MainWindow

@pytest.fixture
def fake_deps():
    with patch("ui.main_window.APIHandler"), \
         patch("ui.main_window.ThemeManager"), \
         patch("ui.main_window.db_connection", MagicMock()), \
         patch("ui.main_window.current_user") as fake_user, \
         patch("ui.main_window.img_helpers.get_window_logo_path", return_value=os.path.abspath("src/imgs/logo.jpg")), \
         patch("ui.main_window.CreateNewTab", return_value=QWidget()), \
         patch("ui.main_window.VendorTicketsTab", return_value=QWidget()), \
         patch("ui.main_window.SearchTicketsTab", return_value=QWidget()), \
         patch("ui.main_window.SettingsTab", return_value=QWidget()):
        fake_user.is_admin.return_value = False
        yield

# should pass
def test_main_window_opens(app, fake_deps):
    window = MainWindow()
    assert window.windowTitle() == "SX-Con"

# should fail due to wrong title
def test_main_window_wrong_title(app, fake_deps):
    window = MainWindow()
    assert window.windowTitle() != "Not SX-Con"

# should pass, not admin level specific test
def test_main_window_has_tabs(app, fake_deps):
    window = MainWindow()
    assert window.tabs.count() >= 4

# should fail, should not instantiate all called tabs
def test_main_window_not_enough_tabs(app, fake_deps):
    window = MainWindow()
    assert window.tabs.count() != 1

# should pass, should show admin tab
def test_main_window_admin_tab(app, fake_deps):
    with patch("ui.main_window.current_user") as fake_user, \
         patch("ui.main_window.AdminSettingsTab", return_value=QWidget()):
        fake_user.is_admin.return_value = True
        window = MainWindow()
        assert window.tabs.count() == 5

# should pass, should not show admin tab
def test_main_window_no_admin_tab_for_non_admin(app, fake_deps):
    window = MainWindow()
    assert window.tabs.count() == 4