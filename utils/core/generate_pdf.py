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
        valid_products = []
        for p in self.ticket_data["products"]:
            if self._is_valid_product(p):
                valid_products.append(p)

        page_height = int(self.height) - 60
        header_height = 100
        footer_height = 130
        row_height = 20

        header_content = (page_height - header_height) // row_height
        header_content_footer = (page_height - header_height - footer_height) // row_height
        rows_with_footer = 5
        num_rows = len(valid_products)

        if num_rows <= 6:
            self.draw_2_in_one()
        else:
            self._draw_pages(valid_products, header_content, header_content_footer, rows_with_footer)
            self._draw_pages(valid_products, header_content, header_content_footer, rows_with_footer)

        self.cursor.save()

    def _draw_pages(self, products, header_content, header_content_footer, rows_with_footer):
        num_rows = len(products)

        if num_rows <= header_content_footer:
            total_pages = 1
        else:
            total_pages = ((num_rows - header_content_footer - 1) // header_content) + 2

        last_page_rows = num_rows - (total_pages - 1) * header_content
        if last_page_rows < rows_with_footer and total_pages > 1:
            last_page_rows = rows_with_footer

        first_pages_total = num_rows - last_page_rows

        offset = 0
        for page_num in range(1, total_pages + 1):
            self.y = self.height - 30
            is_last = page_num == total_pages

            if is_last:
                chunk = products[offset:]
            else:
                take = min(header_content, first_pages_total - offset)
                chunk = products[offset:offset + take]
                offset += take

            self.draw_header(self.cursor, self.y)
            self.draw_ticket_content(self.cursor, self.y, products=chunk,
                                     page_num=page_num, total_pages=total_pages)
            if is_last:
                self.draw_footer(self.cursor, self.y)
            self.cursor.showPage()

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
        c.drawString(30, y - 50, "Consignment Ticket")

        c.setFont("Helvetica-Bold", 12)
        c.drawString(375, y, "Ticket Number:")
        c.rect(475, y - 3, 105, 15)
        c.drawString(475 + 3, y, str(self.ticket_num))
        y -= 20
        c.setFont("Helvetica-Bold", 12)
        c.drawString(375, y, "Vendor ID:")
        c.rect(475, y - 3, 105, 15)
        c.drawString(475 + 3, y, str(self.vendor_id))
        y -= 20
        c.setFont("Helvetica-Bold", 12)
        c.drawString(375, y, "Date Time:")
        c.rect(475, y - 3, 105, 15)
        c.drawString(475 + 3, y, self.ticket_data['datetime'])
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

            c.setFont("Helvetica-Bold", 8)
            c.drawString(30, y_prod, "ID:")
            c.rect(42, y_prod - 3, 34, 15)
            c.drawString(42 + 3, y_prod + 1, str(prod.get("product_id", "")))
            c.drawString(79, y_prod, "Name:")
            c.rect(105, y_prod - 3, 157, 15)
            c.drawString(105 + 3, y_prod + 1, prod.get("product_name", ""))
            c.drawString(265, y_prod, "Price:")
            c.rect(289, y_prod - 3, 50, 15)
            c.drawString(289 + 3, y_prod + 1, f"${prod.get('price', 0):.2f}")
            c.drawString(342, y_prod, "Rate:")
            c.rect(364, y_prod - 3, 25, 15)
            c.drawString(364 + 3, y_prod + 1, f"{str(prod.get('rate'))}%")
            c.drawString(392, y_prod, "Signed:")
            c.rect(423, y_prod - 3, 29, 15)
            c.drawString(423 + 3, y_prod + 1, str(prod.get("quantity", "")))
            c.drawString(455, y_prod, "Sold:")
            c.rect(477, y_prod - 3, 29, 15)
            c.drawString(477 + 3, y_prod + 1, str(prod.get("sold", "")))
            c.drawString(509, y_prod, "Total:")
            c.rect(533, y_prod - 3, 48, 15)
            c.drawString(533 + 3, y_prod + 1, f"${vendor_amount:.2f}" if vendor_amount else "TBD")
            y_prod -= 20

        # Replace line with page number if both arguments are provided
        if page_num is not None and total_pages is not None:
            c.setFont("Helvetica-Bold", 8)
            page_text = f"Page {page_num} of {total_pages}"
            c.drawCentredString(self.width / 2, y_prod - 5, page_text)
        else:
            c.setFont("Helvetica-Bold", 8)
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
        c.drawString(30, y, "Potential at Signing")
        y_pot = y - 15
        # y_pot -= 18

        shared = self.ticket_data["revenue"]["shared"]
        if shared:
            last_cut = shared[-1]
            c.setFont("Helvetica", 10)
            c.drawString(40, y_pot, f"${last_cut.get('vendor', 0):.2f}")
            c.rect(40 - 3, y_pot - 3, 120, 15)
            y_pot -= 18

        y_pot -= 18
        c.setFont("Helvetica-Bold", 10)
        c.drawString(30, y_pot, "Payout")
        y_pot -= 18
        payout = self.ticket_data['revenue']['payout']
        if payout:
            cashed_out = payout[-1]
            c.setFont("Helvetica", 10)
            c.drawString(40, y_pot, f"${cashed_out.get('vendor', 0):.2f}")
            c.rect(40 - 3, y_pot - 3, 120, 15)
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

test = PDF(90)
test.create_supermarket_ticket()