import os
import pytest
from handlers.handler_pdf import handler_live_pdf

@pytest.fixture
def cleanup_pdf():
    created_files = []
    yield created_files
    for file in created_files:
        if os.path.exists(file):
            os.remove(file)

def test_handler_live_pdf_creates_file(app, cleanup_pdf):
    vendor_data = {
        "vendor_id": 1,
        "first_name": "Test",
        "last_name": "User"
    }
    product_data = [
        {
            "product_id": 1,
            "product_type": "Hot Food",
            "product_name": "Apple",
            "price": 10.00,
            "quantity": 1,
            "total": 7.00,
            "sold": 0,
            "remaining": 1
        }
    ]
    revenue_data = {
        "shared": [],
        "grouped": [],
        "payout": []
    }
    ticket_data = {
        'ticket_number': 9999,
        'datetime' : '03/14/2026 -- 03:44',
    }
    handler_live_pdf(ticket_data['ticket_number'], vendor_data, product_data, revenue_data, ticket_data['datetime'])
    pdf = handler_live_pdf(ticket_data['ticket_number'], vendor_data, product_data, revenue_data, ticket_data['datetime'])
    cleanup_pdf.append(pdf.pdf_filename)
    assert os.path.exists(pdf.pdf_filename)
