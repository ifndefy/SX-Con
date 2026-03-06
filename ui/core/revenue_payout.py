from PyQt6.QtWidgets import QWidget
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtWidgets import QHBoxLayout
from PyQt6.QtWidgets import QLabel
from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtCore import Qt
from decimal import Decimal
from decimal import ROUND_HALF_UP

from services.update_property import update_property
from src.user import current_user

import utils.logger.logger as log


class RevenuePayout(QWidget):
    def __init__(self):
        super().__init__()
        self.vendor_input = None
        self.super_x_input = None
        self.sold_input = None
        self.products = []
        self.setup_ui()

    def setup_ui(self):
        """
        :purpose: initializes the payout section
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

        super_x_header = QLabel("Super X Retain")
        super_x_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        super_x_header.setFixedWidth(120)
        header_layout.addWidget(super_x_header)

        main_layout.addLayout(header_layout)

        # Data row
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

        # Calculate button
        self.calc_btn = QPushButton("Calculate Payout")
        self.calc_btn.clicked.connect(self.handle_calculate)
        main_layout.addWidget(self.calc_btn)

        main_layout.addStretch()

    def set_products(self, products: list, consignment_id: str):
        self.products = products
        self.consignment_id = consignment_id

    def handle_calculate(self):
        from services.get_item import get_item
        from ui.core.revenue_generation import RevenueGeneration

        q2 = Decimal("0.01")
        total_vendor = Decimal("0.00")
        total_super_x = Decimal("0.00")

        consignment = get_item("Consignments", "consignment", self.consignment_id)
        if not consignment:
            log.error("Failed to fetch consignment for payout calculation")
            return

        fresh_products = consignment.get('products', [])

        for fresh in fresh_products:
            price = float(fresh.get('price', 0))
            sold = int(fresh.get('sold', 0))
            rate = fresh.get('rate', 45)

            result = RevenueGeneration.calculate_revenues(price, sold, "100%", rate)
            if result == -1:
                log.error(f"Failed to calculate payout for product {fresh.get('product_id')}")
                continue

            total_vendor += result['vendor']
            total_super_x += result['super_x']

        self.vendor_input.setText(f"${float(total_vendor.quantize(q2, rounding=ROUND_HALF_UP)):.2f}")
        self.super_x_input.setText(f"${float(total_super_x.quantize(q2, rounding=ROUND_HALF_UP)):.2f}")

        payout_data = {
            'vendor': float(total_vendor.quantize(q2, rounding=ROUND_HALF_UP)),
            'super_x': float(total_super_x.quantize(q2, rounding=ROUND_HALF_UP)),
            'user': ', '.join([current_user.get_username(), current_user.get_user_full_name()])
        }

        result = update_property("Consignments", "consignment", self.consignment_id, "revenue.payout", [payout_data])
        if result != 0:
            log.error("Failed to save payout to database")
        else:
            log.info(f"Payout saved for consignment {self.consignment_id}")

    def get_payout_data(self) -> dict:
        """
        :purpose: retrieves current payout display values
        :return: dict with sold, vendor, super_x
        :author(s): Joe Lee
        """
        return {
            'vendor': float(self.vendor_input.text().replace('$', '') or 0),
            'super_x': float(self.super_x_input.text().replace('$', '') or 0)
        }

    def clear(self):
        """
        :purpose: resets payout fields to zero
        :author(s): Joe Lee
        """
        self.products = []
        self.sold_input.setText("0")
        self.vendor_input.setText("$0.00")
        self.super_x_input.setText("$0.00")