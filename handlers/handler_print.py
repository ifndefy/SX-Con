import os
import sys

from pathlib import Path
import utils.logger.logger as log
from utils.core.print_pdf import Sxcprinter

#Compute once at import time to avoid re computing the general path each time
current_dir = Path(sys.executable).parent if getattr(sys, 'frozen', False) else (Path(__file__).parent.parent / "utils")
tickets_dir = current_dir / "tickets"

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
    """
    :Purpose: Fetches the PDF path
    :param: ticket_number: Ticket number
    :Author(s): Joe Lee
    """
    return tickets_dir / f"{ticket_number}.pdf"
