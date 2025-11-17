from reportlab.pdfgen import canvas

# might remove win32, currently using os to print pdf and generate file path
import win32api
import win32print

import textwrap
from typing import Union

import os
from datetime import datetime


def generate_pdf(output_path: str, text: Union[dict, str]) -> int:
    """
    Generates a PDF file from either a pre-formatted string or dictionary, then opens it using the default PDF view
    Args:
        output_path: Path to output file
        text (Union[dict, str]) Content to include in the PDF, either a string or a dictionary
    Returns:
        success: return 0
        input type unsupported: return -1
    """
    pdf = canvas.Canvas(output_path)

    max_char_per_line = 80
    x = 82
    y = 720

    if isinstance(text, str):
        text = textwrap.dedent(text)
        lines = [line.lstrip() for line in text.strip().split("\n")]

    elif isinstance(text, dict):
        lines = [f"{key}: {value}" for key, value in text.items()]

    else:
        return -1

    for line in lines:
        wrapped = textwrap.wrap(line, width=max_char_per_line)
        for segment in wrapped:
            pdf.drawString(x, y, segment)
            y -= 14
            if y < 72:
                pdf.showPage()
                y = 720
        y -= 10
        if y < 72:
            pdf.showPage()
            y = 720

    pdf.save()
    #win32api.ShellExecute(0, "open", output_path, None, ".", 1)
    os.startfile(output_path)

    return 0

def generate_filepath(prefix: str = "record_output", extension: str = "pdf") -> str:
    """
        generates a filepath to a new file in the current user's Documents folder
        Args:
            prefix: prefix to use for the new file
            extension: extension/type for the new file
        Returns:
            filepath for the new file
        """

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    documents_folder = os.path.join(os.environ["USERPROFILE"], "Documents")

    target_folder = os.path.join(documents_folder, "SXC_tickets")
    os.makedirs(target_folder, exist_ok=True)

    filename = f"{prefix}_{timestamp}.{extension}"
    return os.path.join(target_folder, filename)



if __name__ == "__main__":
    print("Test Print")
    test_print = """
        Product id: id
        Product name: name
        Notes: Lorem ipsum dolor sit amet, consectetur adipiscing elit. Quisque tempus ut massa sed tempus. Fusce pharetra a velit sit amet tristique. Duis maximus ullamcorper ligula at mattis. Cras nec mattis orci, non convallis augue.
        Price: $12
        Quantity: 30                 
    """
    product = {
        "product id": 12345,
        "product name": "Sample Product",
        "notes": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Quisque tempus ut massa sed tempus. Fusce pharetra a velit sit amet tristique. Duis maximus ullamcorper ligula at mattis. Cras nec mattis orci, non convallis augue.",
        "price": 19.99,
        "quantity": 10
    }

    file_path = generate_filepath()

    generate_pdf(file_path, product)        # test print with a dictionary
    #generate_pdf(file_path, test_print)    # test print with a string