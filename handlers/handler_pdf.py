import os

from utils.core.generate_pdf import PDF

def handler_live_pdf(ticket_number, vendor_data, product_data, revenue_data, datetime, payout_number=None):
    """
    :Purpose: Live PDF generation needs to pass data into the handler
    :Method: passes live data into generate_pdf method
    :Param: ticket_number: Ticket number
    :Param: vendor_data: Vendor document
    :Param: product_data: Product document
    :Param: revenue_data: Revenue document
    :Param: datetime: Date and time
    :Param: payout_number: Payout number
    :Author(s): Joe Lee
    """
    pdf = PDF("LIVE")
    pdf.ticket_num = ticket_number
    pdf.set_pdf_filename(payout_number)
    pdf.set_cursor(pdf.pdf_filename)

    pdf.vendor_id = vendor_data.get('vendor_id')

    pdf.ticket_data = {
        "ticket_number": ticket_number,
        "datetime": datetime,
        "vendor_id": vendor_data.get('vendor_id'),
        "products": product_data,
        "revenue": revenue_data
    }
    pdf.num_prods = len(product_data)
    pdf.vendor_data = {
        "first_name": vendor_data.get('first_name'),
        "last_name": vendor_data.get('last_name')
    }
    pdf.create_supermarket_ticket()
    return pdf

def handler_db_pdf(ticket_num):
    """
    :Purpose: Fetches a consignment item from the database and prints the base data
    :Param: ticket_num: Ticket number
    :Author(s): Joe Lee
    """
    pdf = PDF(ticket_num)
    pdf.create_supermarket_ticket()
    return pdf