import os
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from services.get_item_by_property import get_item_by_property


class PDF:
    def __init__(self, ticket_num):
        self.project_root = None
        self.current_file = __file__
        self.project_root = os.path.dirname(os.path.dirname(os.path.dirname(self.current_file)))
        self.tickets_dir = os.path.join(self.project_root, "utils", "tickets")
        os.makedirs(self.tickets_dir, exist_ok=True)

        self.width, self.height = letter
        self.y = self.height - 30

        self.ticket_num = ticket_num
        self.pdf_filename = os.path.join(self.tickets_dir, f"{str(self.ticket_num)}.pdf")

        self.cursor = canvas.Canvas(self.pdf_filename, pagesize=letter)
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

    # todo: def get_current_user()

    def create_supermarket_ticket(self):
        self.draw_header(self.cursor, self.y)
        self.draw_ticket_content(self.cursor, self.y)
        num_prods = len(self.ticket_data["price_data"]["products"])
        if num_prods <= 5:
            self.cursor.line(30, self.y / 2, self.width - 30, self.y / 2)
            self.draw_ticket_content(self.cursor, self.y / 2 - 30)
        else:
            self.cursor.showPage()
            self.y = self.height - 30
            self.draw_header(self.cursor, self.y)
            self.draw_ticket_content(self.cursor, self.y)
        self.cursor.save()

    def draw_header(self, cursor, y_axis):
        y = y_axis
        c = cursor

        logo_path = os.path.join(self.project_root, "src", "imgs", "logo.jpg")
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

        c.line(30, y, self.width - 30, y)
        y -= 20

        self.y = y

    def draw_ticket_content(self, cursor, y_axis):
        y_prod = y_axis
        c = cursor

        count = 0
        for prod in self.ticket_data["price_data"]["products"]:
            c.setFont("Helvetica-Bold", 10)
            c.drawString(30, y_prod, "Product ID:")
            c.rect(85, y_prod - 3, 34, 15)
            c.drawString(85 + 3, y_prod + 1, prod.get("product_id", ""))
            c.drawString(124, y_prod, "Product Name:")
            c.rect(196, y_prod - 3, 173, 15)
            c.drawString(196 + 3, y_prod + 1, prod.get("product_name", ""))
            c.drawString(376, y_prod, "Price:")
            c.rect(405, y_prod - 3, 43, 15)
            c.drawString(405 + 3, y_prod + 1, prod.get("price", ""))
            c.drawString(452, y_prod, "Qty:")
            c.rect(473, y_prod - 3, 29, 15)
            c.drawString(473 + 3, y_prod + 1, str(prod.get("quantity", "")))
            c.drawString(505, y_prod, "Total:")
            c.rect(533, y_prod - 3, 48, 15)
            c.drawString(533 + 3, y_prod + 1, "$2000.00") # todo: populate this field properly
            y_prod -= 20
            count += 1
            if count == 24:
                self.cursor.line(30, y_prod, self.width - 30, y_prod)
                self.cursor.showPage()
                self.y = self.height - 30
                self.draw_header(self.cursor, self.y)
                y_prod = self.y
        y = y_prod
        c.line(30, y + 5, self.width - 30, y + 5)
        y -= 15

        c.setFont("Helvetica-Bold", 10)
        c.drawCentredString(275, y, "Revenue by Type")
        y_type = y - 15

        c.setFont("Helvetica-Bold", 10)
        for type in ["Hot Foods", "General", "Produce"]: # todo: parse list to be inserted into consignment item
            c.setFont("Helvetica", 10)
            c.drawString(206, y_type, str(type))
            c.rect(206 - 3, y_type - 3, 60, 15)
            c.drawString(280, y_type, "place_holder") # todo: parse list to be inserted into consignment item
            c.rect(280 - 3, y_type - 3, 60, 15)
            y_type -= 18

        c.setFont("Helvetica-Bold", 10)
        c.drawCentredString(475, y, "Potential Revenues")
        y_pot = y - 15

        c.setFont("Helvetica-Bold", 10)
        c.drawCentredString(412, y_pot, "You")
        c.drawCentredString(470, y_pot, "Percentage")
        c.drawCentredString(528, y_pot, "Super X")
        y_pot -= 18

        for cut in self.ticket_data["revenue_sharing"]:
            c.setFont("Helvetica", 10)
            c.drawString(386, y_pot, str(cut.get("vendor")))
            c.rect(386 - 3, y_pot - 3, 60, 15)
            c.drawCentredString(470, y_pot, str(cut.get("percentage")))
            c.drawString(500, y_pot, str(cut.get("super_x")))
            c.rect(500 - 3, y_pot - 3, 60, 15)
            y_pot -= 18
        y = y_pot - 30

        c.setFont("Helvetica-Bold", 10)
        c.drawString(30, y, "Vendor Name:")
        c.rect(100, y - 3, 185, 15)
        c.drawString(100 + 3, y + 1, (" ".join([self.vendor_data["first_name"], self.vendor_data["last_name"]])))
        c.drawString(300, y, "Vendor Signature: ___________________________")
        y -= 20

        # todo: populate employee fields
        c.drawString(30, y, "Employee Name:")
        c.rect(112, y - 3, 173, 15)
        c.drawString(112 + 3, y + 1, "123456789012345678901234567890") # todo: popoulate with user data
        c.drawString(300, y, "Employee Signature: _________________________")


test = PDF(100025)
test.create_supermarket_ticket()