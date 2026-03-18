from unittest.mock import MagicMock
from ui.core.excel_button import ExcelButton

def test_excel_button_exists(app):
    fake_gatherer = MagicMock()
    fake_export = MagicMock()
    button = ExcelButton(fake_gatherer, fake_export, "Export")
    assert button is not None