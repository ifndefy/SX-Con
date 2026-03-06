import pytest
from PyQt6.QtWidgets import QApplication

@pytest.fixture(scope="session")
def app():
    app = QApplication.instance() or QApplication([])
    yield app