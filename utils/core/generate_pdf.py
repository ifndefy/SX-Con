import os
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter


def create_supermarket_ticket():
    current_file = __file__
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_file)))
    tickets_dir = os.path.join(project_root, "utils", "tickets")
    os.makedirs(tickets_dir, exist_ok=True)
    pdf_filename = os.path.join(tickets_dir, "ticket_test_trial.pdf")

    c = canvas.Canvas(pdf_filename, pagesize=letter)
    width, height = letter

    def draw_ticket_content(start_y):
        y = start_y

        logo_path = os.path.join(project_root, "src", "imgs", "logo.jpg")
        logo = ImageReader(logo_path)

        c.setFont("Helvetica-Bold", 24)
        c.drawImage(logo, 20, y - 50, width=365, height=71)

        c.setFont("Helvetica-Bold", 16)
        c.drawString(400, y, "Consignment Ticket")
        y -= 20
        c.setFont("Helvetica-Bold", 12)
        c.drawString(400, y, "Ticket Number:")
        c.rect(500, y - 3, 80, 15)
        c.drawString(500 + 4, y, "ticket_num")
        y -= 20
        c.setFont("Helvetica-Bold", 12)
        c.drawString(400, y, "Vendor ID:")
        c.rect(500, y - 3, 80, 15)
        c.drawString(500 + 4, y, "vendor_id")
        y -= 20

        c.line(30, y, width - 30, y)
        y -= 20

        num_prods = 5
        for prod in range(num_prods):
            c.setFont("Helvetica-Bold", 10)
            c.drawString(30, y, "Product ID:")
            c.rect(85, y - 3, 34, 15)
            c.drawString(85 + 3, y + 1, "12345")
            c.drawString(126, y, "Product Name:")
            c.rect(198, y - 3, 173, 15)
            c.drawString(198 + 3, y + 1, "123456789012345678901234567890")
            c.drawString(378, y, "Price:")
            c.rect(407, y - 3, 53, 15)
            c.drawString(407 + 3, y + 1, "$99999.99")
            c.drawString(467, y, "Qty:")
            c.rect(488, y - 3, 34, 15)
            c.drawString(488 + 3, y + 1, "12345")
            y -= 20

        c.line(30, y + 5, width - 30, y + 5)
        y -= 15

        c.setFont("Helvetica-Bold", 10)
        c.drawCentredString(475, y, "Potential Revenues")
        y -= 15

        header_y = y
        c.setFont("Helvetica-Bold", 10)
        c.drawCentredString(412, header_y, "You")
        c.drawCentredString(470, header_y, "Percentage")
        c.drawCentredString(528, header_y, "Super X")
        y -= 15

        percentages = ["25%", "50%", "75%", "100%"]
        for i, percent in enumerate(percentages):
            c.setFont("Helvetica", 10)
            c.drawString(386, y, "$0.75")
            c.rect(386 - 3, y - 3, 60, 15)
            c.drawCentredString(470, y, percent)
            c.drawString(500, y, "$0.25")
            c.rect(500 - 3, y - 3, 60, 15)
            y -= 18

        c.setFont("Helvetica-Bold", 10)
        c.drawString(30, y, "Vendor Name:")
        c.rect(100, y - 3, 173, 15)
        c.drawString(100 + 3, y + 1, "123456789012345678901234567890")
        c.drawString(300, y, "Vendor Signature: _________________________")
        y -= 20

        c.drawString(30, y, "Employee Name:")
        c.rect(112, y - 3, 173, 15)
        c.drawString(112 + 3, y + 1, "123456789012345678901234567890")
        c.drawString(300, y, "Employee Signature: _________________________")

    draw_ticket_content(height - 30)
    c.line(30, height / 2, width - 30, height / 2)
    draw_ticket_content(height / 2 - 30)
    c.save()


create_supermarket_ticket()