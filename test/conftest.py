import pytest
from PyQt6.QtWidgets import QApplication
import os

os.environ["QT_LOGGING_RULES"] = "*.warning=false"

@pytest.fixture(scope="session")
def app():
    app = QApplication.instance() or QApplication([])
    yield app