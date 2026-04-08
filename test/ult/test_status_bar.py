import pytest
from unittest.mock import MagicMock
from ui.core.status_bar import StatusBar

def test_status_bar_exists(app):
    statbar = StatusBar("test")
    assert statbar is not None, "Expected StatusBar to be created"