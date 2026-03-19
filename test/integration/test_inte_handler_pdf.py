import os
import pytest
from handlers.handler_pdf import handler_db_pdf

@pytest.fixture
def cleanup_pdf():
    created_files = []
    yield created_files
    for file in created_files:
        if os.path.exists(file):
            os.remove(file)

def test_handler_db_pdf_creates_file(app, cleanup_pdf):
    pdf = handler_db_pdf(1)
    cleanup_pdf.append(pdf.pdf_filename)
    assert os.path.exists(pdf.pdf_filename), "Expected to be able to create pdf"