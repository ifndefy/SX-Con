import os
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

from src.user import current_user
from src.imgs import img_helpers
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

        self.num_prods = 0
        if self.ticket_data:
            for product in self.ticket_data["products"]:
                for prop in ("product_id", "product_name", "price", "quantity"):
                    if product.get(prop) not in (None, "", "NULL", 0, 0.0, "$0.00", "0"):
                        self.num_prods += 1
                        break

    def set_ticket_data(self):
        self.ticket_data = get_item_by_property("Consignments", "consignment", "consignment_id", self.ticket_num)

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

    def create_supermarket_ticket(self):
        if self.num_prods <= 9:
            self.draw_2_in_one()
        else:
            valid_products = []
            for p in self.ticket_data["products"]:
                if self._is_valid_product(p):
                    valid_products.append(p)

            rows_per_page = 29
            total_pages = (len(valid_products) + rows_per_page - 1) // rows_per_page
            i = 0
            page_num = 1
            while i < len(valid_products):
                chunk = valid_products[i:i + rows_per_page]
                is_last = (i + rows_per_page) >= len(valid_products)
                self.y = self.height - 30
                self.draw_header(self.cursor, self.y)
                # Pass page number and total pages to draw_ticket_content
                self.draw_ticket_content(self.cursor, self.y, products=chunk,
                                         page_num=page_num, total_pages=total_pages)
                if is_last:
                    self.draw_footer(self.cursor, self.y)
                self.cursor.showPage()
                i += rows_per_page
                page_num += 1
        self.cursor.save()

    def draw_2_in_one(self):
        self.draw_header(self.cursor, self.y)
        self.draw_ticket_content(self.cursor, self.y)
        self.draw_footer(self.cursor, self.y)
        self.cursor.line(30, self.height / 2, self.width - 30, self.height / 2)
        self.y = self.height / 2 - 30
        self.draw_header(self.cursor, self.y)
        self.draw_ticket_content(self.cursor, self.y)
        self.draw_footer(self.cursor, self.y)

    def draw_header(self, cursor, y_axis):
        y = y_axis
        c = cursor

        logo_path = img_helpers.get_window_logo_path()
        logo = ImageReader(logo_path)

        c.saveState()
        c.setStrokeColorRGB(1, 1, 1, 0)
        c.drawImage(logo, 30, y - 50, width=305, height=73, preserveAspectRatio=True, mask='auto')
        c.restoreState()

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
        c.setFont("Helvetica-Bold", 12)
        c.drawString(400, y, "Date Time:")
        c.rect(475, y - 3, 105, 15)
        c.drawString(475 + 6, y, self.ticket_data['datetime'])
        y -= 20

        c.line(30, y, self.width - 30, y)
        y -= 20

        self.save_y(y)

    @staticmethod
    def _is_valid_product(product):
        """
        :purpose: validate if a product is fully null
        :Author(s): Joe lee
        """
        property = ("product_id", "product_name", "price", "quantity")
        for prop in property:
            if product.get(prop) not in (None, "", "NULL", 0, 0.0, "$0.00", "0"):
                return True
        return False

    def draw_ticket_content(self, cursor, y_axis, products=None,
                            page_num=None, total_pages=None):
        y_prod = y_axis
        c = cursor

        if products is None:
            valid_products = []
            for prod in self.ticket_data["products"]:
                if self._is_valid_product(prod):
                    valid_products.append(prod)
        else:
            valid_products = products

        payout_products = []
        if "revenue" in self.ticket_data and "payout" in self.ticket_data["revenue"]:
            payout_list = self.ticket_data["revenue"]["payout"]
            if payout_list and len(payout_list) > 0:
                payout_products = payout_list[0].get("products", [])

        payout_index = 0
        for prod in valid_products:
            vendor_amount = 0
            if payout_index < len(payout_products): # need this for when multiples of the same product_id are in a consignment
                vendor_amount = payout_products[payout_index].get("vendor", 0)
                payout_index += 1

            c.setFont("Helvetica-Bold", 10)
            c.drawString(30, y_prod, "ID:")
            c.rect(45, y_prod - 3, 34, 15)
            c.drawString(45 + 3, y_prod + 1, str(prod.get("product_id", "")))
            c.drawString(84, y_prod, "Name:")
            c.rect(116, y_prod - 3, 173, 15)
            c.drawString(116 + 3, y_prod + 1, prod.get("product_name", ""))
            c.drawString(293, y_prod, "Price:")
            c.rect(322, y_prod - 3, 43, 15)
            c.drawString(322 + 3, y_prod + 1, f"${prod.get('price', 0):.2f}")
            c.drawString(369, y_prod, "Signed:")
            c.rect(410, y_prod - 3, 29, 15)
            c.drawString(410 + 3, y_prod + 1, str(prod.get("quantity", "")))
            c.drawString(444, y_prod, "Sold:")
            c.rect(471, y_prod - 3, 29, 15)
            c.drawString(471 + 3, y_prod + 1, str(prod.get("sold", "")))
            c.drawString(505, y_prod, "Total:")
            c.rect(533, y_prod - 3, 48, 15)
            c.drawString(533 + 3, y_prod + 1, f"${vendor_amount:.2f}" if vendor_amount else "TBD")
            y_prod -= 20

        # Replace line with page number if both arguments are provided
        if page_num is not None and total_pages is not None:
            c.setFont("Helvetica", 10)
            page_text = f"Page {page_num} of {total_pages}"
            c.drawCentredString(self.width / 2, y_prod - 5, page_text)
        else:
            c.setFont("Helvetica", 10)
            page_text = f"Page 1 of 1"
            c.drawCentredString(self.width / 2, y_prod - 5, page_text)

        y_prod -= 20
        self.y = y_prod

    def draw_footer(self, cursor, y_axis):
        c = cursor
        y = y_axis
        c.line(30, y, self.width - 30, y)

        y -= 15

        y_type = y - 15
        c.setFont("Helvetica-Bold", 10)
        c.drawCentredString(118, y, "Potential at Signing")
        y_pot = y - 15

        c.setFont("Helvetica-Bold", 10)
        c.drawCentredString(60, y_pot, "Vendor")
        c.drawCentredString(118, y_pot, "Amount Sold")
        c.drawCentredString(175, y_pot, "Super X")
        y_pot -= 18

        shared = self.ticket_data["revenue"]["shared"]
        if shared:
            last_cut = shared[-1]
            c.setFont("Helvetica", 10)
            c.drawString(34, y_pot, f"${last_cut.get('vendor', 0):.2f}")
            c.rect(34 - 3, y_pot - 3, 60, 15)
            c.drawCentredString(118, y_pot, str(last_cut.get("percentage")))
            c.drawString(148, y_pot, f"${last_cut.get('super_x', 0):.2f}")
            c.rect(148 - 3, y_pot - 3, 60, 15)
            y_pot -= 18

        y_pot -= 18
        c.setFont("Helvetica-Bold", 10)
        c.drawCentredString(118, y_pot, "Payout")
        y_pot -= 18
        payout = self.ticket_data['revenue']['payout']
        if payout:
            cashed_out = payout[-1]
            c.setFont("Helvetica", 10)
            c.drawString(34, y_pot, f"${cashed_out.get('vendor', 0):.2f}")
            c.rect(34 - 3, y_pot - 3, 60, 15)
            c.drawString(148, y_pot, f"${cashed_out.get('super_x', 0):.2f}")
            c.rect(148 - 3, y_pot - 3, 60, 15)
            y_pot -= 18
        else:
            c.setFont("Helvetica", 10)
            c.drawString(34, y_pot, f"TBD")
            c.rect(34 - 3, y_pot - 3, 60, 15)
            c.drawString(148, y_pot, f"TBD")
            c.rect(148 - 3, y_pot - 3, 60, 15)
            y_pot -= 18


        c.setFont("Helvetica-Bold", 10)
        c.drawCentredString(285, y, "Revenue by Type")
        c.setFont("Helvetica-Bold", 10)
        c.drawCentredString(241, y_type, "Type")
        c.drawCentredString(315, y_type, "Total")
        y_type -= 18

        payout_list = self.ticket_data.get('revenue', {}).get('payout', [])
        prod_type_total = {}
        if payout_list and payout_list[-1].get('grouped'):
            for item in payout_list[-1]['grouped']:
                prod_type_total[item['product_type']] = item['vendor']
            prod_type_total['Total'] = payout_list[-1].get('vendor', 0)

        c.setFont("Helvetica-Bold", 10)
        for type in ["Hot Food", "General", "Produce", "Total"]:
            total = prod_type_total.get(type, 0)
            c.setFont("Helvetica", 10)
            c.drawString(216, y_type, str(type))
            c.rect(216 - 3, y_type - 3, 60, 15)
            c.drawString(290, y_type, f"${total:.2f}" if total else "TBD")
            c.rect(290 - 3, y_type - 3, 60, 15)
            y_type -= 18

        y = y_axis - 15
        c.setFont("Helvetica-Bold", 10)
        c.drawString(445, y, "Signatures")
        y_sign = y - 15
        c.setFont("Helvetica-Bold", 10)
        c.drawString(360, y_sign, "Vendor Name:")
        c.rect(429, y_sign - 3, 153, 15)
        c.drawString(432, y_sign + 1, " ".join([
            self.vendor_data.get("first_name") or "",
            self.vendor_data.get("last_name") or ""
        ]).strip())
        y_sign -= 18
        c.drawString(360, y_sign, "Vendor Signature:")
        c.line(447, y_sign, 582, y_sign)
        y_sign -= 18

        c.drawString(360, y_sign, "Employee Name:")
        c.rect(442, y_sign - 3, 140, 15)
        c.drawString(445, y_sign + 1, f"{current_user.get_user_full_name()}")
        y_sign -= 18
        c.drawString(360, y_sign, "Employee Signature: ")
        c.line(460, y_sign, 582, y_sign)
        y_sign -= 18
        c.drawString(395, y_sign, "** Not Official unless signed **")

    def save_y(self, y_axis):
        self.y = y_axis