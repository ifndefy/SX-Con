import pytest
from PyQt6.QtWidgets import QApplication
import os

os.environ["QT_LOGGING_RULES"] = "*.warning=false"
os.environ["QT_QPA_PLATFORM"] = "offscreen"

@pytest.fixture(scope="session")
def app():
    app = QApplication.instance() or QApplication([])
    yield app