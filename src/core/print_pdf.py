import os
import subprocess
import win32print

from src import SPOT

# List of fake printers to avoid misdirections
FAKE_KEYWORDS = {
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

def get_real_printers():
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
            if any(fake_kw in lower_name for fake_kw in FAKE_KEYWORDS):
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
        raise RuntimeError(f"Failed to enumerate printers: {e}")

    return printers


def find_printer():
    """
    Purpose: Return the default printer if not then return printer at index 0
    Returns: default printer | printer[0]
    Author(s): Joe Lee
    """
    # Get real printers
    real_printers = get_real_printers()
    if not real_printers:
        raise RuntimeError("No real, ready printer found.")

    # Get default printer if there is one
    try:
        default_printer = win32print.GetDefaultPrinter()
        if default_printer in real_printers:
            return default_printer
    except Exception:
        # printer_name will remain as "None"
        pass

    # Fallback plan, typically index 0 is the "default" printer / real printer
    return real_printers[0]


def print_pdf(pdf_path, printer_name=None):
    """
    Purpose: Prints a pdf, it is likely this can print other file types as well, but this program only uses PDFs
    :todo: check if printing xlsx is possible
    Method: Verifies dependency files exist, then calls find_printer for a printer to print from
    Author(s): Joe Lee
    """
    # Validate files
    pdf_path = os.path.abspath(pdf_path)
    if not os.path.isfile(pdf_path):
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")
    if not os.path.isfile(SPOT.SUMATRA_RELATIVE_PATH):
        raise FileNotFoundError(
            f"Error: Portable SumatraPDF not found at: {SPOT.SUMATRA_RELATIVE_PATH}"
        )

    if printer_name is None:
        printer_name = find_printer()
        print(f"Using printer: {printer_name}")
    else:
        try:
            handle = win32print.OpenPrinter(printer_name)
            win32print.ClosePrinter(handle)
        except Exception:
            raise ValueError(f"Printer '{printer_name}' is not available.")

    cmd = [
        SPOT.SUMATRA_RELATIVE_PATH,
        "-print-to", printer_name,
        "-print-settings", "1x",
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
        print(f"Successfully sent to printer: {os.path.basename(pdf_path)}")
    except subprocess.CalledProcessError as e:
        # Sumatra 3.5.2 is known to return a harmless error even on success
        if e.returncode == 3221226356:
            print("Warning: Sumatra returned known harmless error – print likely succeeded.")
        else:
            raise RuntimeError(f"Error: Printing failed (error {e.returncode}): {e.stderr or e}") from e

# Uncomment and pass in PDF path to test print
# print_pdf(r"D:\SX-Con\utils\tickets\ticket_test_trial.pdf")