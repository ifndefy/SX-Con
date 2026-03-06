import os

from utils.core.generate_pdf import PDF

def handler_live_pdf(vendor_data, product_data, revenue_data):
    """
    :param live: live indicates usage will not be able to pull from db
    :param vendor_data:
    :param product_data:
    :Purpose: Live PDF generation needs to pass data into the handler
    :Method: passes live data into generate_pdf method
    :Author(s): Joe Lee
    """
    pdf = PDF("LIVE")
    pdf.ticket_num = vendor_data.get('ticket_number')
    pdf.set_pdf_filename()
    pdf.set_cursor(pdf.pdf_filename)

    pdf.vendor_id = vendor_data.get('vendor_id')

    pdf.ticket_data = {
        "ticket_number": vendor_data.get('ticket_number'),
        "vendor_id": vendor_data.get('vendor_id'),
        "price_data": {
            "products": product_data
        },
        "revenue": revenue_data
    }
    pdf.num_prods = len(product_data)
    pdf.vendor_data = {
        "first_name": vendor_data.get('first_name'),
        "last_name": vendor_data.get('last_name')
    }
    pdf.create_supermarket_ticket()


def handler_db_pdf(ticket_num):
    pdf = PDF(ticket_num)
    pdf.create_supermarket_ticket()