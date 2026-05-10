import os
import subprocess
import win32print
import sys

from pathlib import Path
from src import SPOT
import utils.logger.logger as log

class Sxcprinter:
    def __init__(self, ticket_number):        
        self.root_path = Path(sys.executable).parent if getattr(sys, 'frozen', False) else (Path(__file__).parent.parent.parent)
        self.sumatra_exe = self.root_path / SPOT.SUMATRA_RELATIVE_PATH

        self.pdf_rel_dir = r"tickets" if getattr(sys, 'frozen', False) else r"utils\tickets"

        self.printer_name = None
        self.ticket_number = None
        self.pdf_path = None

        # List of fake printers to avoid misdirections
        self.FAKE_KEYWORDS = {
            "microsoft print to pdf",
            "xps document writer",
            "onenote",
            "fax",
            "adobe pdf",
            "pdf creator",
            "send to",
            "virtual",
            "null",
            "microsoft xps document writer",
            "one note",
            "snagit",
            "do pdf",
            "foxit phantom pdf printer",
            "bullzip",
            "cute pdf",
            "pdf24",
            "pdf architect",
            "nova pdf",
            "pdf-xchange",
            "pdf factory"
        }

        self.set_ticket_number(ticket_number)
        self.set_pdf_path_from_ticket(self.ticket_number)
        self.printer_name = self.get_printer_name()

    def set_ticket_number(self, ticket_number):
        self.ticket_number = ticket_number

    def get_ticket_number(self):
        return self.ticket_number

    def set_pdf_path_from_ticket(self, ticket_number):
        wanted_path = self.root_path / self.pdf_rel_dir / f"{str(ticket_number)}.pdf"
        self.pdf_path = wanted_path

    def set_printer_name(self, printer_name):
        self.printer_name = printer_name

    def get_printer_name(self):
        printer_name = self.find_printer()
        return printer_name

    def get_real_printers(self):
        """
        Method: Gets a list of printers, then skips over printers with fake keywords in their name
        Returns: list of printers
        Author(s): Joe Lee
        """
        printers = []
        try:
            flags = win32print.PRINTER_ENUM_LOCAL | win32print.PRINTER_ENUM_CONNECTIONS
            for printer in win32print.EnumPrinters(flags):
                name = printer[2]
                if not name:
                    continue

                lower_name = name.lower()
                if any(fake_kw in lower_name for fake_kw in self.FAKE_KEYWORDS):
                    continue

                try:
                    handle = win32print.OpenPrinter(name)
                    info = win32print.GetPrinter(handle, 2)
                    win32print.ClosePrinter(handle)
                    status = info.get('Status', 0)
                    if status != 0:
                        continue
                except Exception:
                    continue

                printers.append(name)
        except Exception as e:
            log.error(f"Failed to enumerate printers: {e}")

        return printers

    def find_printer(self):
        """
        :Purpose: return the default printer if not then return printer at index 0
        :Returns: default printer or printer[0]
        :Raises: exception if printer is found but unavailable
        :Author(s): Joe Lee
        """
        # filter the virtual printers
        real_printers = self.get_real_printers()
        if not real_printers:
            message = "No real and ready printer found."
            log.error(message)
            raise Exception(message)

        # Get default printer if there is one
        try:
            default_printer = win32print.GetDefaultPrinter()
            if default_printer in real_printers:
                self._assert_printer_ready(default_printer)
                return default_printer
        except Exception:
            if not real_printers:
                message = "No real and ready printer found."
                log.error(message)
                raise Exception(message)

        # Fallback plan, typically index 0 is the "default" printer / real printer
        fallback_printer = real_printers[0]
        self._assert_printer_ready(fallback_printer)
        return fallback_printer

    def _assert_printer_ready(self, printer_name: str):
        """
        :purpose: Checks printer status and raises if it is not ready to print.
        :Author(s): Joe Lee
        """
        UNAVAILABLE_STATUSES = {
            win32print.PRINTER_STATUS_BUSY: "busy",
            win32print.PRINTER_STATUS_DOOR_OPEN: "door open",
            win32print.PRINTER_STATUS_ERROR: "in error state",
            win32print.PRINTER_STATUS_NO_TONER: "out of toner",
            win32print.PRINTER_STATUS_NOT_AVAILABLE: "not available",
            win32print.PRINTER_STATUS_OFFLINE: "offline",
            win32print.PRINTER_STATUS_OUT_OF_MEMORY: "out of memory",
            win32print.PRINTER_STATUS_OUTPUT_BIN_FULL: "output bin full",
            win32print.PRINTER_STATUS_PAGE_PUNT: "page punt error",
            win32print.PRINTER_STATUS_PAPER_JAM: "paper jam",
            win32print.PRINTER_STATUS_PAPER_OUT: "out of paper",
            win32print.PRINTER_STATUS_PAPER_PROBLEM: "paper problem",
            win32print.PRINTER_STATUS_USER_INTERVENTION: "requires user intervention",
        }

        try:
            printer_handle = win32print.OpenPrinter(printer_name)
        except Exception:
            message = f"Printer '{printer_name}' could not be opened — it may be offline or in an error state."
            log.error(message)
            raise Exception(message)
        try:
            printer_info = win32print.GetPrinter(printer_handle, 2)
            status = printer_info["Status"]

            for status_flag, description in UNAVAILABLE_STATUSES.items():
                if status & status_flag:  # needs to use bitwise and due to printer codes
                    message = f"Printer '{printer_name}' is unavailable: {description}."
                    log.error(message)
                    raise Exception(message)
        except Exception:
            win32print.ClosePrinter(printer_handle)
            raise

        win32print.ClosePrinter(printer_handle)

    def val_pdf_path(self, pdf_path):
        if not os.path.exists(pdf_path):
            log.error(f"Error: {pdf_path} is not valid")
            return False
        return True

    def val_dependencies(self):
        sumatra_path = self.root_path / SPOT.SUMATRA_RELATIVE_PATH
        if not os.path.exists(sumatra_path):
            log.error(f"Portable SumatraPDF not found at: {SPOT.SUMATRA_RELATIVE_PATH}")
            return False
        return True

    def print_pdf(self, pdf_path=None, ticket_number=None, printer_name=None):
        """
        Purpose: Prints a pdf, it is likely this can print other file types as well, but this program only uses PDFs
        Method: Verifies dependency files exist, then calls find_printer for a printer to print from
        Author(s): Joe Lee
        """
        if ticket_number:
            self.set_pdf_path_from_ticket(str(ticket_number))
            pdf_path = self.pdf_path

        if not self.val_pdf_path(pdf_path):
            return
        if not self.val_dependencies():
            return

        if printer_name is None:
            printer_name = self.find_printer()
            log.info(f"Using printer: {printer_name}")
        else:
            try:
                handle = win32print.OpenPrinter(printer_name)
                win32print.ClosePrinter(handle)
            except Exception as e:
                log.error(f"Printer '{printer_name}' is not available. {e}")

        cmd = [
            self.sumatra_exe,
            "-print-to", printer_name,
            "-print-settings", "1x", # number of copies
            "-silent",
            "-exit-on-print",
            pdf_path
        ]

        try:
            subprocess.run(
                cmd,
                check=True,
                capture_output=True,
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            log.info(f"Successfully sent to printer: {os.path.basename(pdf_path)}")
        except subprocess.CalledProcessError as e:
            # Sumatra 3.5.2 is known to return a harmless error even on success
            if e.returncode == 3221226356:
                log.warning("Warning: Sumatra returned known harmless error – print likely succeeded.")
            else:
                log.error(f"Error: {e}")
                raise RuntimeError(f"Error: Printing failed (error {e.returncode}): {e.stderr or e}") from e