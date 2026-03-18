import os
import pytest
from unittest.mock import patch
from utils.core.generate_excel import generate_excel


@pytest.fixture
def cleanup_excel():
    created_files = []
    yield created_files
    for file in created_files:
        if os.path.exists(file):
            os.remove(file)

def test_excel_creates_file(cleanup_excel):
    test_path = os.path.abspath("test_output.xlsx")
    cleanup_excel.append(test_path)

    test_data = {
        "fake_dataset": [{"1": "2", "3": "4"}]
    }

    with patch("utils.core.generate_excel.QFileDialog.getSaveFileName",
               return_value=(test_path, "Excel File (*.xlsx)")):
        generate_excel(test_data)

    assert os.path.exists(test_path)