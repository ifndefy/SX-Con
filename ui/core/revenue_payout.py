from PyQt6.QtWidgets import QWidget
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtWidgets import QHBoxLayout
from PyQt6.QtWidgets import QLabel
from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtCore import Qt
from decimal import Decimal
from decimal import ROUND_HALF_UP
from datetime import datetime

from services.get_item import get_item
from services.get_property import get_property
from services.update_property import update_property
from src.user import current_user
from ui.core.revenue_generation import RevenueGeneration
from ui.prompts.view_history import ViewPayoutHistory

import utils.logger.logger as log


class RevenuePayout(QWidget):
    def __init__(self):
        super().__init__()
        self.calc_btn = None
        self.payout_btn = None
        self.history_btn = None
        self.vendor_input = None
        self.super_x_input = None
        self.products = []
        self.consignment_id = None
        self.on_calculated = None
        self.on_payout_committed = None
        self.payout_list = []
        self.setup_ui()

    def setup_ui(self):
        """
        :purpose: initializes the payout section with preview and history button
        :author(s): Joe Lee
        """
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Header row
        header_layout = QHBoxLayout()

        vendor_header = QLabel("Vendor Payout")
        vendor_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        vendor_header.setFixedWidth(120)
        header_layout.addWidget(vendor_header)

        super_x_header = QLabel("Super X")
        super_x_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        super_x_header.setFixedWidth(120)
        header_layout.addWidget(super_x_header)

        main_layout.addLayout(header_layout)

        data_layout = QHBoxLayout()
        data_layout.setSpacing(5)

        self.vendor_input = QLineEdit()
        self.vendor_input.setText("$0.00")
        self.vendor_input.setObjectName("READ_ONLY")
        self.vendor_input.setReadOnly(True)
        self.vendor_input.setFixedWidth(120)
        data_layout.addWidget(self.vendor_input)

        self.super_x_input = QLineEdit()
        self.super_x_input.setText("$0.00")
        self.super_x_input.setObjectName("READ_ONLY")
        self.super_x_input.setReadOnly(True)
        self.super_x_input.setFixedWidth(120)
        data_layout.addWidget(self.super_x_input)

        main_layout.addLayout(data_layout)

        btn_layout = QHBoxLayout()

        self.calc_btn = QPushButton("Calculate")
        self.calc_btn.clicked.connect(self.handle_calculate)
        btn_layout.addWidget(self.calc_btn)

        self.payout_btn = QPushButton("Payout")
        self.payout_btn.clicked.connect(self.handle_payout)
        btn_layout.addWidget(self.payout_btn)

        main_layout.addLayout(btn_layout)

        self.history_btn = QPushButton("View Payout History")
        self.history_btn.clicked.connect(self._show_history)
        main_layout.addWidget(self.history_btn)

        main_layout.addStretch()

    def set_products(self, products: list, consignment_id: str):
        """
        :purpose: loads product data and existing payout history
        :author(s): Joe Lee
        """
        self.products = products
        self.consignment_id = consignment_id
        consignment = get_item("Consignments", "consignment", self.consignment_id)
        if consignment:
            self.payout_list = consignment.get('revenue', {}).get('payout', [])
            if consignment.get('status') == "CLOSED":
                self.calc_btn.setEnabled(False)
                self.calc_btn.setObjectName('LOCKED')
                self.calc_btn.setText('TICKET CLOSED')
                self.payout_btn.setEnabled(False)
                self.payout_btn.setObjectName('LOCKED')
                self.payout_btn.setText('TICKET CLOSED')

    def calculate_payout(self):
        """
        :purpose: calculates delta revenue for products sold since last payout
        :return: dict of revenue data
        :author(s): Joe Lee
        """
        consignment = get_item("Consignments", "consignment", self.consignment_id)
        if not consignment:
            log.error("Failed to fetch consignment for payout calculation")
            return None

        products = consignment.get('products', [])
        previous_sold = self._build_previous_sold_map()
        product_payouts = self._calculate_product_deltas(products, previous_sold)

        return self._aggregate_payouts(product_payouts)

    def _build_previous_sold_map(self):
        """
        :purpose: sums sold quantities across all previous payouts per product to prevent duplicate payouts
        :return: dict mapping product_id to total previously paid sold count
        :author(s): Joe Lee
        """
        previous_sold = {}
        for payout in self.payout_list:
            for product in payout.get('products', []):
                p_id = product['product_id']
                previous_sold[p_id] = previous_sold.get(p_id, 0) + product.get('sold', 0)
        return previous_sold

    def _calculate_product_deltas(self, products, previous_sold):
        """
        :purpose: calculates revenue deltas for each product against previous payouts
        :return: list of product payout dicts with delta sold and revenue amounts
        :author(s): Joe Lee
        """
        product_payouts = []

        for prod in products:
            product_id = prod['product_id']
            price = float(prod['price'])
            current_sold = int(prod['sold'])
            rate = prod['rate']

            prev_sold = previous_sold.get(product_id, 0)
            delta_sold = current_sold - prev_sold

            if delta_sold <= 0:
                continue

            result = RevenueGeneration.calculate_revenues(price, delta_sold, "100%", rate)
            if result == -1:
                log.error(f"Failed to calculate payout for product {product_id}")
                continue

            product_name = get_property("Entities", "product_name", "product", product_id)
            if product_name == "-1":
                product_name = ''

            product_payouts.append({
                'product_id': product_id,
                'product_name': product_name,
                'product_type': prod['product_type'],
                'sold': delta_sold,
                'vendor': result['vendor'],
                'super_x': result['super_x']
            })

        return product_payouts

    def _aggregate_payouts(self, product_payouts):
        """
        :purpose: totals vendor and super_x amounts, groups by product type
        :return: dict with vendor, super_x, products, grouped, type_totals
        :author(s): Joe Lee
        """
        q2 = Decimal("0.01")
        total_vendor = Decimal("0.00")
        total_super_x = Decimal("0.00")
        vendor_by_type = {}
        super_x_by_type = {}

        for prod in product_payouts:
            total_vendor += prod['vendor']
            total_super_x += prod['super_x']

            prod_type = prod['product_type']
            if prod_type not in vendor_by_type:
                vendor_by_type[prod_type] = Decimal("0.00")
                super_x_by_type[prod_type] = Decimal("0.00")
            vendor_by_type[prod_type] += prod['vendor']
            super_x_by_type[prod_type] += prod['super_x']

        grouped = []
        type_totals = {}
        for prod_type in vendor_by_type:
            vendor_val = float(vendor_by_type[prod_type].quantize(q2, rounding=ROUND_HALF_UP))
            super_val = float(super_x_by_type[prod_type].quantize(q2, rounding=ROUND_HALF_UP))
            grouped.append({
                'product_type': prod_type,
                'vendor': vendor_val,
                'super_x': super_val
            })
            type_totals[prod_type] = vendor_val

        grand_total = float(total_vendor.quantize(q2, rounding=ROUND_HALF_UP))
        grand_super_x = float(total_super_x.quantize(q2, rounding=ROUND_HALF_UP))
        type_totals['Total'] = grand_total

        for prod in product_payouts:
            prod['vendor'] = float(prod['vendor'].quantize(q2, rounding=ROUND_HALF_UP))
            prod['super_x'] = float(prod['super_x'].quantize(q2, rounding=ROUND_HALF_UP))
            del prod['product_type']

        revenues = {
            'vendor': grand_total,
            'super_x': grand_super_x,
            'products': product_payouts,
            'grouped': grouped,
            'type_totals': type_totals
        }
        return revenues

    def handle_calculate(self):
        """
        :purpose: previews payout calculation without saving to DB
        :author(s): Joe Lee
        """
        payout = self.calculate_payout()
        if not payout:
            return

        if not payout['products']:
            QMessageBox.warning(self, "No Changes", "No new sales since the last payout")
            return

        self.vendor_input.setText(f"${payout['vendor']:.2f}")
        self.super_x_input.setText(f"${payout['super_x']:.2f}")

        if payout['vendor'] > 0:
            self.payout_btn.setObjectName('green_btn')
        else:
            self.payout_btn.setObjectName('DEFAULT')
        self.payout_btn.style().unpolish(self.payout_btn)
        self.payout_btn.style().polish(self.payout_btn)

        if self.on_calculated:
            self.on_calculated(payout['type_totals'])

        return payout['type_totals']

    def handle_payout(self):
        """
        :purpose: pushes calculated totals to DB
        :author(s): Joe Lee
        """
        payout = self.calculate_payout()
        if not payout or not payout['products']:
            QMessageBox.warning(self, "No Changes", "No new sales since the last payout")
            return

        payout_num = len(self.payout_list) + 1
        confirm = QMessageBox.question(
            self,
            "Confirm Payout",
            f"Pushed payout #{payout_num}?\n\nVendor: ${payout['vendor']:.2f}\nSuper X: ${payout['super_x']:.2f}",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if confirm != QMessageBox.StandardButton.Yes:
            return

        if not self._save_payout(payout):
            return

        QMessageBox.information(self, "Success", f"Payout #{payout_num} saved")
        log.info(f"Payout #{payout_num} saved for consignment {self.consignment_id}")

        if self.on_calculated:
            self.on_calculated(payout['type_totals'])

        if self.on_payout_committed:
            self.on_payout_committed()

        self.vendor_input.setText("$0.00")
        self.super_x_input.setText("$0.00")

        self.payout_btn.setObjectName('DEFAULT')
        self.payout_btn.style().unpolish(self.payout_btn)
        self.payout_btn.style().polish(self.payout_btn)

        return payout['type_totals']

    def _save_payout(self, payout):
        """
        :purpose: builds payout entry, appends to list, writes payout and accumulated to DB
        :return: True on success, False on failure
        :author(s): Joe Lee
        """
        payout_data = {
            'vendor': payout['vendor'],
            'super_x': payout['super_x'],
            'user': ', '.join([current_user.get_username(), current_user.get_user_full_name()]),
            'datetime': datetime.now().strftime("%m/%d/%y -- %H:%M"),
            'products': payout['products'],
            'grouped': payout['grouped']
        }

        self.payout_list.append(payout_data)

        result = update_property(
            "Consignments", "consignment", self.consignment_id,
            "revenue.payout", self.payout_list
        )
        if result != 0:
            log.error("Failed to save payout to database")
            self.payout_list.pop()
            return False

        consignment = get_item("Consignments", "consignment", self.consignment_id)
        shared = consignment['revenue']['shared']

        acc_vendor = 0.0
        acc_super_x = 0.0
        for payout in self.payout_list:
            acc_vendor += float(payout['vendor'])
            acc_super_x += float(payout['super_x'])

        update_property(
            "Consignments", "consignment", self.consignment_id,
            "revenue.accumulated", {
                'vendor': acc_vendor,
                'super_x': acc_super_x,
                'signed_vendor': float(shared[-1]['vendor']),
                'signed_super_x': float(shared[-1]['super_x'])
            }
        )

        return True

    def _show_history(self):
        """
        :purpose: opens a dialog showing all payout history cards
        :author(s): Joe Lee
        """
        self.history_dialog = ViewPayoutHistory(self, self.payout_list, self.consignment_id)
        self.history_dialog.open()

    def clear(self):
        """
        :purpose: resets payout fields and history
        :author(s): Joe Lee
        """
        self.products = []
        self.payout_list = []
        self.vendor_input.setText("$0.00")
        self.super_x_input.setText("$0.00")

    def get_payout_data(self):
        vendor = float(self.vendor_input.text().replace("$", ""))
        super_x = float(self.super_x_input.text().replace("$", ""))
        return {"vendor": vendor, "super_x": super_x}