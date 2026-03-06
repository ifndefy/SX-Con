from PyQt6.QtWidgets import QWidget
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtWidgets import QHBoxLayout
from PyQt6.QtWidgets import QLabel
from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtCore import Qt

from decimal import Decimal
from decimal import ROUND_HALF_UP

from src.core.generate_agg_data import convert_price
from ui.core.revenue_generation import RevenueGeneration
import utils.logger.logger as log


class RevenueByProdType(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.revenue_records = []
        self.totals = {}
        self.setup_ui()

    def setup_ui(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        content_container = QVBoxLayout()
        revenue_layout = QVBoxLayout()

        header_layout = QHBoxLayout()
        type_header = QLabel("Type")
        type_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        type_header.setFixedWidth(100)
        header_layout.addWidget(type_header)

        total_header = QLabel("Total")
        total_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        total_header.setFixedWidth(120)
        header_layout.addWidget(total_header)
        revenue_layout.addLayout(header_layout)

        product_types = ["Hot Food", "General", "Produce", "Total"]
        for prod_type in product_types:
            row_layout = QHBoxLayout()
            row_layout.setSpacing(5)

            type_label = QLabel(prod_type)
            type_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            type_label.setFixedWidth(100)
            row_layout.addWidget(type_label)

            total_edit = QLineEdit()
            total_edit.setText("$0.00")
            total_edit.setObjectName("READ_ONLY")
            total_edit.setReadOnly(True)
            total_edit.setAlignment(Qt.AlignmentFlag.AlignRight)
            total_edit.setFixedWidth(120)
            row_layout.addWidget(total_edit)

            revenue_layout.addLayout(row_layout)

            self.revenue_records.append({
                'type_label': type_label,
                'total_edit': total_edit,
                'product_type': prod_type
            })

        content_container.addLayout(revenue_layout)
        main_layout.addLayout(content_container)
        main_layout.addStretch()
        revenue_layout.addStretch()

    def generate_revenue_data(self, product_sections):
        """
        :Purpose: generates the grouped revenues by product type, uses RevenueGeneration's calculation
        :Param: product_sections container
        :Author(s): Joe Lee
        """
        product_types = ["Hot Food", "General", "Produce"]
        totals = {}
        grand_total = Decimal("0.00")

        for prod_type in product_types:
            type_total = Decimal("0.00")
            for section in product_sections:
                if section['product_type'].currentText() != prod_type:
                    continue
                price_text = section['price'].text().strip()
                qty_text = section['quantity'].text().strip()
                rate_text = section['rate'].text().strip()
                if not price_text or not qty_text or not rate_text:
                    continue
                price = convert_price(price_text)
                if price is None:
                    continue
                try:
                    qty = int(qty_text)
                    rate = int(rate_text)
                except ValueError:
                    continue
                result = RevenueGeneration.calculate_revenues(price, qty, "100%", rate)
                if result == -1:
                    continue
                type_total += result['vendor']
            totals[prod_type] = type_total.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            grand_total += totals[prod_type]

        totals['Total'] = float(Decimal(str(grand_total)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))
        return totals

    def update_display_values(self, totals):
        """
        :Purpose: updates text fields of widget
        :Author(s): Joe Lee
        """
        self.totals = totals
        for rec in self.revenue_records:
            prod_type = rec['product_type']
            rec['total_edit'].setText(f"${totals.get(prod_type, 0.0):.2f}")

    def handle_updating(self, product_sections):
        """
        :Purpose: handles updating of widget display field
        :Author(s): Joe Lee
        """
        totals = self.generate_revenue_data(product_sections)
        self.update_display_values(totals)

    def get_revenue_data(self):
        """
        :Return: revenue data -> list
        :Author(s): Joe Lee
        """
        rev_data = []
        for prod_type, total in self.totals.items():
            rev_data.append({'product_type': prod_type, 'total': total})
        return rev_data