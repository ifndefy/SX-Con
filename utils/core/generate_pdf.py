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
        self.pdf_filename = None
        self.cursor = None
        self.vendor_id = None
        self.ticket_data = None
        self.vendor_data = None

        if str(self.ticket_num).upper() != "LIVE":
            self.set_ticket_data()
            self.set_vendor_num()
            self.set_vendor_data()
            self.set_pdf_filename()
            self.set_cursor(self.pdf_filename)

        self.num_prods = len(self.ticket_data["price_data"]["products"])

    def set_ticket_data(self):
        self.ticket_data = get_item_by_property("Consignments", "consignment", "ticket_number", self.ticket_num)

    def set_vendor_num(self, ):
        self.vendor_id = self.ticket_data["vendor_id"]

    def set_vendor_data(self):
        self.vendor_data = get_item_by_property("Entities", "vendor", "vendor_id", self.vendor_id)

    def set_pdf_filename(self):
        self.pdf_filename = os.path.join(self.tickets_dir, f"{str(self.ticket_num)}.pdf")

    def set_cursor(self, f_name):
        if f_name:
            self.pdf_filename = f_name
        if self.pdf_filename is None:
            raise Exception("PDF name could not be set")
        self.cursor = canvas.Canvas(self.pdf_filename, pagesize=letter)

    # todo: def get_current_user()

    def create_supermarket_ticket(self):
        if self.num_prods <= 8:
            self.draw_header(self.cursor, self.y)
            self.draw_ticket_content(self.cursor, self.y)
            self.draw_footer(self.cursor, self.y)
            self.cursor.line(30, self.height / 2, self.width - 30, self.height / 2)
            self.y = self.height / 2 - 30
            self.draw_header(self.cursor, self.y)
            self.draw_ticket_content(self.cursor, self.y)
            self.draw_footer(self.cursor, self.y)
        else:
            self.draw_header(self.cursor, self.y)
            self.draw_ticket_content(self.cursor, self.y)
            self.draw_footer(self.cursor, self.y)
            self.cursor.showPage()
            self.y = self.height - 30
            self.draw_header(self.cursor, self.y)
            self.draw_ticket_content(self.cursor, self.y)
            self.draw_footer(self.cursor, self.y)
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

        self.save_y(y)

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
            c.drawString(533 + 3, y_prod + 1, prod.get("total", ""))
            y_prod -= 20
            count += 1
            if count == 27 and self.num_prods < 33: # can fit 27 items per page with tables and footing
                self.cursor.line(30, y_prod, self.width - 30, y_prod)
                self.cursor.showPage()
                self.y = self.height - 30
                self.draw_header(self.cursor, self.y)
                y_prod = self.y
            if count == 33 and self.num_prods >= 38: # fits 33 max per page with no tables nor footing
                self.cursor.line(30, y_prod, self.width - 30, y_prod)
                self.cursor.showPage()
                self.y = self.height - 30
                self.draw_header(self.cursor, self.y)
                y_prod = self.y
        y = y_prod
        c.line(30, y + 5, self.width - 30, y + 5)
        y -= 15
        y_type = y
        self.save_y(y)

        c.setFont("Helvetica-Bold", 10)
        c.drawCentredString(118, y, "Shared Revenues")
        y_pot = y - 15

        c.setFont("Helvetica-Bold", 10)
        c.drawCentredString(60, y_pot, "Vendor")
        c.drawCentredString(118, y_pot, "Amount Sold")
        c.drawCentredString(175, y_pot, "Super X")
        y_pot -= 18

        for cut in self.ticket_data["revenue"]["shared"]:
            c.setFont("Helvetica", 10)
            c.drawString(34, y_pot, str(cut.get("vendor")))
            c.rect(34 - 3, y_pot - 3, 60, 15)
            c.drawCentredString(118, y_pot, str(cut.get("percentage")))
            c.drawString(148, y_pot, str(cut.get("super_x")))
            c.rect(148 - 3, y_pot - 3, 60, 15)
            y_pot -= 18

        c.setFont("Helvetica-Bold", 10)
        c.drawCentredString(285, y_type, "Revenue by Type")
        y_type -= 15
        c.setFont("Helvetica-Bold", 10)
        c.drawCentredString(241, y_type, "Type")
        c.drawCentredString(315, y_type, "Total")
        y_type -= 18

        rev_groups = self.ticket_data.get('revenue', {}).get('grouped', [])
        prod_type_total = {}
        for group in rev_groups:
            prod_type_total[group['product_type']] = group['total']

        c.setFont("Helvetica-Bold", 10)
        for type in ["Hot Food", "General", "Produce", "Total"]:
            total = prod_type_total.get(type, "$0.00")
            c.setFont("Helvetica", 10)
            c.drawString(216, y_type, str(type))
            c.rect(216 - 3, y_type - 3, 60, 15)
            c.drawString(290, y_type, total)
            c.rect(290 - 3, y_type - 3, 60, 15)
            y_type -= 18

    def draw_footer(self, cursor, y_axis):
        c = cursor
        y = y_axis - 15
        c.setFont("Helvetica-Bold", 10)
        c.drawString(360, y, "Vendor Name:")
        c.rect(429, y - 3, 153, 15)
        c.drawString(432, y + 1, (" ".join([self.vendor_data["first_name"], self.vendor_data["last_name"]])))
        y -= 18
        c.drawString(360, y, "Vendor Signature:")
        c.line(447, y, 582, y)
        y -= 20

        # todo: populate employee fields
        c.drawString(360, y, "Employee Name:")
        c.rect(442, y - 3, 140, 15)
        c.drawString(445, y + 1, "123456789012345678901234") # todo: popoulate with user data
        y -= 18
        c.drawString(360, y, "Employee Signature: ")
        c.line(460, y, 582, y)
        y -= 18
        c.drawString(395, y, "** Not Official unless signed **")

    def save_y(self, y_axis):
        self.y = y_axis