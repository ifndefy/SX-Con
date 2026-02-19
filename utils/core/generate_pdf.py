import os
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from services.get_item_by_property import get_item_by_property


class PDF:
    def __init__(self, ticket_num):
        self.ticket_num = ticket_num
        self.vendor_id = None

        self.ticket_data = None
        self.vendor_data = None

        self.set_ticket_data()
        self.set_vendor_num()
        self.set_vendor_data()

    def set_ticket_data(self):
        self.ticket_data = get_item_by_property("Consignments", "consignment", "ticket_number", self.ticket_num)

    def set_vendor_num(self):
        self.vendor_id = self.ticket_data["vendor_id"]

    def set_vendor_data(self):
        self.vendor_data = get_item_by_property("Entities", "vendor", "vendor_id", self.vendor_id)

    def create_supermarket_ticket(self):
        current_file = __file__
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_file)))
        tickets_dir = os.path.join(project_root, "utils", "tickets")
        os.makedirs(tickets_dir, exist_ok=True)
        pdf_filename = os.path.join(tickets_dir, f"{str(self.ticket_num)}.pdf")

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
            c.drawString(500 + 4, y, str(self.ticket_num))
            y -= 20
            c.setFont("Helvetica-Bold", 12)
            c.drawString(400, y, "Vendor ID:")
            c.rect(500, y - 3, 80, 15)
            c.drawString(500 + 4, y, str(self.vendor_id))
            y -= 20

            c.line(30, y, width - 30, y)
            y -= 20

            for prod in self.ticket_data["price_data"]["products"]:
                c.setFont("Helvetica-Bold", 10)
                c.drawString(30, y, "Product ID:")
                c.rect(85, y - 3, 34, 15)
                c.drawString(85 + 3, y + 1, prod.get("product_id", ""))
                c.drawString(124, y, "Product Name:")
                c.rect(196, y - 3, 173, 15)
                c.drawString(196 + 3, y + 1, prod.get("product_name", ""))
                c.drawString(376, y, "Price:")
                c.rect(405, y - 3, 43, 15)
                c.drawString(405 + 3, y + 1, prod.get("price", ""))
                c.drawString(452, y, "Qty:")
                c.rect(473, y - 3, 29, 15)
                c.drawString(473 + 3, y + 1, "9999")
                c.drawString(505, y, "Total:")
                c.rect(533, y - 3, 48, 15)
                c.drawString(533 + 3, y + 1, "$2000.00") # todo: populate this field properly
                y -= 20

            c.line(30, y + 5, width - 30, y + 5)
            y -= 15

            # todo: insert grouped aggregates
            # todo: group product type hot foods
            # todo: group product type general
            # todo: group product type produce

            c.setFont("Helvetica-Bold", 10)
            c.drawCentredString(475, y, "Potential Revenues")
            y -= 15

            header_y = y
            c.setFont("Helvetica-Bold", 10)
            c.drawCentredString(412, header_y, "You")
            c.drawCentredString(470, header_y, "Percentage")
            c.drawCentredString(528, header_y, "Super X")
            y -= 15

            for cut in self.ticket_data["revenue_sharing"]:
                c.setFont("Helvetica", 10)
                c.drawString(386, y, str(cut.get("vendor")))
                c.rect(386 - 3, y - 3, 60, 15)
                c.drawCentredString(470, y, str(cut.get("percentage")))
                c.drawString(500, y, str(cut.get("super_x")))
                c.rect(500 - 3, y - 3, 60, 15)
                y -= 18

            c.setFont("Helvetica-Bold", 10)
            c.drawString(30, y, "Vendor Name:")
            c.rect(100, y - 3, 173, 15)
            c.drawString(100 + 3, y + 1, (" ".join([self.vendor_data["first_name"], self.vendor_data["last_name"]])))
            c.drawString(300, y, "Vendor Signature: _________________________")
            y -= 20

            # todo: populate employee fields
            c.drawString(30, y, "Employee Name:")
            c.rect(112, y - 3, 173, 15)
            c.drawString(112 + 3, y + 1, "123456789012345678901234567890") # todo: popoulate with user data
            c.drawString(300, y, "Employee Signature: _________________________")

        draw_ticket_content(height - 30)
        c.line(30, height / 2, width - 30, height / 2)
        draw_ticket_content(height / 2 - 30)
        c.save()


test = PDF(100023)
test.create_supermarket_ticket()