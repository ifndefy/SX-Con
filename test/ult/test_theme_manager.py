import pytest
from unittest.mock import MagicMock
from PyQt6.QtWidgets import QWidget
from ui.core.theme_manager import ThemeManager
import os

"""
Author: Kyle Valdez
Purpose: Test if the method works properly
"""

def test_get_available_themes_returns_list(app):
    manager = ThemeManager()
    themes = manager.get_available_themes()
    assert isinstance(themes, list), "Expected a list to be returned"

def test_super_theme_is_default(app):
    manager = ThemeManager()
    manager.themes_dir = os.path.join(os.path.dirname(__file__), "..", "..", "ui", "themes")
    themes = manager.get_available_themes()
    assert themes[0] == "Super", "Expected first index to be 'Super'"

def test_apply_theme_fails_if_no_widget(app):
    manager = ThemeManager()
    result = manager.apply_theme("Super", widget=None)
    assert result == False, "Expected to be able to apply 'Super' theme"

def test_apply_theme_fails_if_no_theme(app):
    manager = ThemeManager()
    widget = QWidget()
    result = manager.apply_theme("no_theme_exists", widget)
    assert result == False, "Expected to fail to apply fake theme"

def test_apply_default_theme_is_Super(app):
    manager = ThemeManager()
    widget = QWidget()
    manager.apply_default_theme(widget)
    assert manager.get_current_theme() == "Super", "Expected default theme to be 'Super'"