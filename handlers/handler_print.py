import os

import utils.logger.logger as log
from utils.core.print_pdf import Sxcprinter

def handler_print(tic_num):
    try:
        if validate_pdf_exists(tic_num):
            sxc_printer = Sxcprinter(ticket_number=tic_num)
            sxc_printer.print_pdf(ticket_number=tic_num)
    except Exception as e:
        log.error(f"Failed to print {tic_num} : {e}")
        raise

def validate_pdf_exists(tic_num):
    check_path = get_pdf_path(tic_num)
    if not os.path.exists(check_path):
        log.error(f"PDF {tic_num} path does not exist: {check_path}")
        return False
    return True

def get_pdf_path(ticket_number):
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, "utils", "tickets", f"{ticket_number}.pdf")