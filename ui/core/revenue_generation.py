from PyQt6.QtWidgets import QWidget
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtWidgets import QHBoxLayout
from PyQt6.QtWidgets import QLabel
from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtCore import Qt
from decimal import Decimal
from decimal import ROUND_HALF_UP
from decimal import InvalidOperation

import utils.logger.logger as log

class RevenueGeneration(QWidget):
    def __init__(self):
        super().__init__()
        self.revenue_records = []
        self.setup_ui()

    def setup_ui(self):
        """
        :author(s): Joe Lee
        :purpose: initializes the revenue section to be placed into a window
        :return: None
        """
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        content_container = QVBoxLayout()

        # Create the 3column layout
        revenue_layout = QVBoxLayout()

        # Header row
        header_layout = QHBoxLayout()

        # Vendor header
        vendor_header = QLabel("Vendor")
        vendor_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        vendor_header.setFixedWidth(120)
        header_layout.addWidget(vendor_header)

        # Percentage header
        percentage_header = QLabel("Amount Sold")
        percentage_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        percentage_header.setFixedWidth(100)
        header_layout.addWidget(percentage_header)

        # Super X header
        super_x_header = QLabel("Super X")
        super_x_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        super_x_header.setFixedWidth(120)
        header_layout.addWidget(super_x_header)

        revenue_layout.addLayout(header_layout)

        # Create 4 rows
        self.revenue_records = []
        for i in range(4):
            record_layout = QHBoxLayout()
            record_layout.setSpacing(5)

            # Vendor rows
            vendor_input = QLineEdit()
            vendor_input.setText("$0.00")
            vendor_input.setObjectName("READ_ONLY")
            vendor_input.setReadOnly(True)
            vendor_input.setFixedWidth(130)
            record_layout.addWidget(vendor_input)

            # Percentage rows
            percentage_label = QLabel(["25%", "50%", "75%", "100%"][i])
            percentage_label.setObjectName("percentage_label")
            percentage_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            percentage_label.setFixedWidth(80)
            record_layout.addWidget(percentage_label)

            # Super X rows
            super_x_input = QLineEdit()
            super_x_input.setText("$0.00")
            super_x_input.setObjectName("READ_ONLY")
            super_x_input.setReadOnly(True)
            super_x_input.setFixedWidth(130)
            record_layout.addWidget(super_x_input)

            revenue_layout.addLayout(record_layout)

            # Store references to the inputs
            self.revenue_records.append({
                'vendor': vendor_input,
                'percentage': percentage_label,
                'super_x': super_x_input
            })

        content_container.addLayout(revenue_layout)
        main_layout.addLayout(content_container)

        # Add stretch to push content to the left half
        main_layout.addStretch()

        # Add stretch to keep section "in place"
        revenue_layout.addStretch()

    def get_revenue_data(self):
        """
        :author(s): Joe Lee
        :purpose: retrieves the revenue data
        :return: Revenue data
        """
        revenue_data = []
        for record in self.revenue_records:
            revenue_data.append({
                'vendor': float(record['vendor'].text().replace('$', '')),
                'percentage': record['percentage'].text(),
                'super_x': float(record['super_x'].text().replace('$', ''))
            })
        return revenue_data

    def clear_revenue_data(self):
        """
        :author(s): Joe Lee
        :purpose: clears the revenue data fields
        :return: None
        """
        for record in self.revenue_records:
            record['vendor'].clear()
            record['super_x'].clear()

        self.set_revenue_data()

    def set_revenue_data(self, revenue_data=None):
        """
        :author(s): Joe Lee
        :purpose: sets the revenue data values
        :return: None
        """
        if revenue_data is None:
            revenue_data = [
                {'vendor': 0.0, 'super_x': 0.0},
                {'vendor': 0.0, 'super_x': 0.0},
                {'vendor': 0.0, 'super_x': 0.0},
                {'vendor': 0.0, 'super_x': 0.0}
            ]

        for i, record in enumerate(revenue_data):
            if i < len(self.revenue_records):
                self.revenue_records[i]['vendor'].setText(f"${record.get('vendor', 0):.2f}")
                self.revenue_records[i]['super_x'].setText(f"${record.get('super_x', 0):.2f}")

    @staticmethod
    def calculate_revenues(price, quantity, percentile, rate=25):
        """
        gross = (price * quantity) * percentile
        super_x = gross * rate
        vendor  = gross * (1 - rate)
        where `rate` is a fraction (0..1). If passed as an integer, treated as percent.
        """
        q2 = Decimal("0.01")

        try:
            d_price = Decimal(str(price))
            d_qty = Decimal(str(quantity))
            if d_price.is_nan() or d_qty.is_nan() or d_price < 0 or d_qty < 0:
                return -1

            # percentile parsing (your existing logic)
            if isinstance(percentile, str):
                p_str = percentile.strip()
                if p_str.endswith("%"):
                    p = Decimal(p_str[:-1].strip()) / Decimal(100)
                else:
                    p = Decimal(p_str)
            else:
                p = Decimal(str(percentile))

            if p > 1:
                p = p / Decimal(100)
            if p < 0 or p > 1:
                return -1

            # rate parsing (NEW)
            r = Decimal(str(rate).strip())
            if r > 1:
                r = r / Decimal(100)
            if r < 0 or r > 1:
                return -1

            gross = d_price * d_qty * p
            super_x = gross * r
            vendor = gross * (Decimal("1") - r)

            gross = gross.quantize(q2, rounding=ROUND_HALF_UP)
            vendor = vendor.quantize(q2, rounding=ROUND_HALF_UP)
            super_x = super_x.quantize(q2, rounding=ROUND_HALF_UP)

            diff = gross - (vendor + super_x)
            if diff != 0:
                vendor = (vendor + diff).quantize(q2, rounding=ROUND_HALF_UP)

            return {"gross": gross, 
                    "vendor": vendor, 
                    "super_x": super_x}

        except (InvalidOperation, ValueError, TypeError):
            return -1

    @staticmethod
    def calculate_total(price, quantity, rate):
        """
        :Purpose: calculates the fee-applied total of a product
        :Author(s): Joe Lee
        """
        try:
            rate = Decimal(int(rate))
        except (InvalidOperation, ValueError, TypeError):
            log.error("Invalid rate")
        d_rate = rate / 100
        d_return_rate = 1 - d_rate
        try:
            d_price = Decimal(str(price))
            d_qty = int(quantity)
            if d_price is None or d_price < 0:
                log.error("Invalid price")
            if d_qty is None or d_qty < 0:
                log.error("Invalid quantity")

            total = (d_price * d_qty * d_return_rate).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            return total
        except (InvalidOperation, ValueError, TypeError):
            return -1