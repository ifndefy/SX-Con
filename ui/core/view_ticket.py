from PyQt6.QtCore import QObject
from PyQt6.QtWidgets import QHBoxLayout
from PyQt6.QtWidgets import QLabel
from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtWidgets import QComboBox
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtWidgets import QFrame

from src.core.update_quantities import update_quantities
from services.get_item import get_item
from ui.core.revenue_generation import RevenueGeneration

import utils.logger.logger as log

class ViewTicket(QObject):
    def __init__(self, ticket_id):
        super().__init__()
        self.ticket_id = ticket_id
        self.product_widgets = {}

    def setup_ui(self, ticket_section, ticket_details):
        details_container = ticket_section['details_container']
        details_container.setObjectName("view_bg")

        product_layout = ticket_section['product_details_layout']

        while product_layout.count():
            child = product_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        ticket_data = ticket_details['ticket_data']
        products = ticket_data.get('price_data', {}).get('products', [])
        revenue_sharing = ticket_data.get('revenue_sharing', [])

        # Products section
        valid_products = []
        for prod in products:
            if prod.get('product_id') and prod.get('product_id') != 'NULL':
                valid_products.append(prod)

        for product in valid_products:
            product_id = product.get('product_id')

            line1_layout = QHBoxLayout()

            line1_layout.addWidget(QLabel("ID:"))
            product_id_input = QLineEdit(product_id)
            product_id_input.setFixedWidth(120)
            product_id_input.setObjectName("READ_ONLY")
            product_id_input.setReadOnly(True)
            line1_layout.addWidget(product_id_input)

            # Product Type
            line1_layout.addWidget(QLabel("Type:"))
            product_type_input = QComboBox()
            product_types = ["SELECT", "Hot Food", "General", "Produce"]
            product_type_input.addItems(product_types)
            product_type_from_db = product.get('product_type', '')
            if product_type_from_db in product_types:
                product_type_input.setCurrentText(product_type_from_db)
            else:
                product_type_input.setCurrentText("SELECT")
            product_type_input.setObjectName("READ_ONLY")
            product_type_input.setEnabled(False)
            line1_layout.addWidget(product_type_input)

            # Product Name
            line1_layout.addWidget(QLabel("Name:"))
            product_name = product.get('product_type', '')
            if product_id and product_id != 'NULL':
                product_entity = get_item('Entities', 'product', product_id)
                if product_entity:
                    product_name = product_entity.get('product_name', product_name)
            product_name_input = QLineEdit(product_name)
            product_name_input.setObjectName("READ_ONLY")
            product_name_input.setReadOnly(True)
            line1_layout.addWidget(product_name_input)

            line1_layout.addStretch()

            # Sold field
            line1_layout.addWidget(QLabel("Sold:"))
            sold_edit = QLineEdit(str(product.get('sold', 0)))
            sold_edit.setFixedWidth(100)
            line1_layout.addWidget(sold_edit)

            update_btn = QPushButton("Update")
            update_btn.product_id = product_id
            update_btn.clicked.connect(self.handle_update_clicked)
            line1_layout.addWidget(update_btn)

            product_layout.addLayout(line1_layout)

            # Line 2: Notes, Price, Quantity
            line2_layout = QHBoxLayout()

            # Notes
            line2_layout.addWidget(QLabel("Notes:"))
            notes_input = QLineEdit(product.get('notes', ''))
            notes_input.setObjectName("READ_ONLY")
            notes_input.setReadOnly(True)
            line2_layout.addWidget(notes_input)

            # Price
            line2_layout.addWidget(QLabel("Price:"))
            price = product.get('price', 0) if product.get('price') else 0
            price = self.fix_price(price)
            price_input = QLineEdit(price)
            price_input.setFixedWidth(100)
            price_input.setObjectName("READ_ONLY")
            price_input.setReadOnly(True)
            line2_layout.addWidget(price_input)

            # Quantity Signed
            line2_layout.addWidget(QLabel("Qty Signed:"))
            quantity_input = QLineEdit(str(product.get('quantity', 0)))
            quantity_input.setFixedWidth(100)
            quantity_input.setObjectName("READ_ONLY")
            quantity_input.setReadOnly(True)
            line2_layout.addWidget(quantity_input)

            # Quantity Remaining
            line2_layout.addWidget(QLabel("Qty Remaining:"))
            remaining_display = QLineEdit(str(product.get('remaining', 0)))
            remaining_display.setFixedWidth(100)
            remaining_display.setObjectName("READ_ONLY")
            remaining_display.setReadOnly(True)
            line2_layout.addWidget(remaining_display)

            # Quantity Sold
            line2_layout.addWidget(QLabel("Qty Sold:"))
            sold_display = QLineEdit(str(product.get('sold', 0)))
            sold_display.setFixedWidth(100)
            sold_display.setObjectName("READ_ONLY")
            sold_display.setReadOnly(True)
            line2_layout.addWidget(sold_display)

            line2_layout.addStretch()
            product_layout.addLayout(line2_layout)

            # HR Line to separate products
            line3_layout = QHBoxLayout()
            hr1 = QFrame()
            hr1.setFrameShape(QFrame.Shape.HLine)
            hr1.setFrameShadow(QFrame.Shadow.Sunken)
            hr1.setObjectName("hr")
            line3_layout.addWidget(hr1)

            product_layout.addLayout(line3_layout)

            self.product_widgets[product_id] = {
                'sold_edit': sold_edit,
                'remaining_display': remaining_display,
                'quantity_display': quantity_input,
                'sold_display': sold_display
            }

        # Revenue Sharing section
        if revenue_sharing:
            revenue_container_layout = QHBoxLayout()
            revenue_container_layout.setObjectName("view_bg")
            revenue_container_layout.addStretch(1)
            revenue_widget = RevenueGeneration()
            revenue_widget.set_revenue_data(revenue_sharing)
            revenue_container_layout.addWidget(revenue_widget)
            product_layout.addLayout(revenue_container_layout)

    def handle_update_clicked(self):
        product_id, widgets = self.get_product_and_widgets()
        if not product_id or not widgets:
            return

        new_sold, quantity = self.val_quantities(widgets)
        if new_sold is None or quantity is None:
            return

        success, new_remaining, error = update_quantities(
            self.ticket_id, product_id, new_sold
        )
        if success:
            widgets['sold_edit'].setText(str(new_sold))
            widgets['remaining_display'].setText(str(new_remaining))
            widgets['sold_display'].setText(str(new_sold))
        else:
            log.error(f"Update failed: {error}")

    def get_product_and_widgets(self):
        """
        :Purpose: get product and widget data for parsing
        :Author(s): Joe Lee
        """
        button = self.sender()
        if button is None:
            return None, None

        product_id = getattr(button, 'product_id', None)
        if product_id is None:
            log.error("Update button missing product data.")
            return None, None

        widgets = self.product_widgets.get(product_id)
        if not widgets:
            log.error(f"No widgets found for product {product_id}")
            return None, None

        return product_id, widgets

    def val_quantities(self, widgets):
        """
        :Purpose: Validate values from widgets
        :Returns: new_sold, quantity
        :Author(s): Joe Lee
        """
        sold_input = widgets['sold_edit']
        quantity_display = widgets['quantity_display']

        try:
            new_sold = int(sold_input.text())
        except ValueError:
            log.error(f"Invalid sold value: {sold_input.text()}")
            return None, None

        try:
            quantity = int(quantity_display.text())
        except ValueError:
            log.error(f"Invalid quantity value: {quantity_display.text()}")
            return None, None

        return new_sold, quantity

    @staticmethod
    def fix_price(price_val):
        price_str = str(price_val)
        if not price_str.startswith('$'):
            price_str = '$' + price_str
        return price_str