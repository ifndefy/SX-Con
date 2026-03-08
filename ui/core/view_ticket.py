from PyQt6.QtCore import QObject
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHBoxLayout
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtWidgets import QLabel
from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtWidgets import QComboBox
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtWidgets import QFrame

from src.core.update_quantities import update_quantities
from services.get_item import get_item
from ui.core.revenue_by_product_type import RevenueByProdType
from ui.core.revenue_generation import RevenueGeneration
from ui.core.revenue_payout import RevenuePayout

import utils.logger.logger as log

class ViewTicket(QObject):
    def __init__(self, ticket_id):
        super().__init__()
        self.ticket_id = ticket_id
        self.product_widgets = {}
        self.revenue_widget = None
        self.rev_by_type = None
        self.payout_widget = None
        self.ticket_status = None

    def setup_ui(self, ticket_section, ticket_details):
        details_container = ticket_section['details_container']
        details_container.setObjectName("view_bg")

        product_layout = ticket_section['product_details_layout']

        while product_layout.count():
            child = product_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        ticket_data = ticket_details['ticket_data']
        self.ticket_status = ticket_data.get('status', '')
        products = ticket_data.get('products', [])
        revenue_sharing = ticket_data.get('revenue', []).get('shared', [])
        revenue_grouped = ticket_data.get('revenue', []).get('grouped', [])

        # Products section
        valid_products = []
        for prod in products:
            if prod.get('product_id') and prod.get('product_id') != 'NULL':
                valid_products.append(prod)

        for product in valid_products:
            product_id = product.get('product_id')

            line1_layout = QHBoxLayout()

            line1_layout.addWidget(QLabel("ID:"))
            product_id_input = QLineEdit(str(product_id))
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
            if self.ticket_status == "CLOSED":
                sold_edit.setReadOnly(True)
                sold_edit.setObjectName("LOCKED")

            update_btn = QPushButton("Update")
            update_btn.product_id = product_id
            if self.ticket_status == "CLOSED":
                update_btn.setEnabled(True)
                update_btn.setObjectName("LOCKED")
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
                'sold_display': sold_display,
                'update_btn' : update_btn,
            }

        # Revenue section
        if revenue_sharing:
            revenue_container_layout = QHBoxLayout()
            revenue_container_layout.setObjectName("view_bg")

            shared_layout = QVBoxLayout()
            shared_label = QLabel("Signed")
            shared_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            shared_layout.addWidget(shared_label)
            hr2 = QFrame()
            hr2.setFrameShape(QFrame.Shape.HLine)
            hr2.setFrameShadow(QFrame.Shadow.Sunken)
            hr2.setObjectName("hr")
            shared_layout.addWidget(hr2)
            self.revenue_widget = RevenueGeneration()
            self.revenue_widget.setObjectName("view_bg")
            self.revenue_widget.set_revenue_data(revenue_sharing)
            shared_layout.addWidget(self.revenue_widget)
            revenue_container_layout.addLayout(shared_layout)

            vr1 = QFrame()
            vr1.setFrameShape(QFrame.Shape.VLine)
            vr1.setFrameShadow(QFrame.Shadow.Sunken)
            vr1.setObjectName("hr")
            revenue_container_layout.addWidget(vr1)

            grouped_layout = QVBoxLayout()
            grouped_label = QLabel("Grouped")
            grouped_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            grouped_layout.addWidget(grouped_label)
            hr1 = QFrame()
            hr1.setFrameShape(QFrame.Shape.HLine)
            hr1.setFrameShadow(QFrame.Shadow.Sunken)
            hr1.setObjectName("hr")
            grouped_layout.addWidget(hr1)
            self.rev_by_type = RevenueByProdType()
            self.rev_by_type.setObjectName("view_bg")
            self.rev_by_type.load_from_db_document(ticket_data)
            grouped_layout.addWidget(self.rev_by_type)
            revenue_container_layout.addLayout(grouped_layout)

            vr2 = QFrame()
            vr2.setFrameShape(QFrame.Shape.VLine)
            vr2.setFrameShadow(QFrame.Shadow.Sunken)
            vr2.setObjectName("hr")
            revenue_container_layout.addWidget(vr2)

            payout_layout = QVBoxLayout()
            payout_label = QLabel("Payout")
            payout_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            payout_layout.addWidget(payout_label)
            hr3 = QFrame()
            hr3.setFrameShape(QFrame.Shape.HLine)
            hr3.setFrameShadow(QFrame.Shadow.Sunken)
            hr3.setObjectName("hr")
            payout_layout.addWidget(hr3)
            self.payout_widget = RevenuePayout()
            self.payout_widget.setObjectName("view_bg")
            self.payout_widget.on_calculated = self.rev_by_type.update_display_values
            self.payout_widget.set_products(valid_products, self.ticket_id)
            payout_layout.addWidget(self.payout_widget)
            revenue_container_layout.addLayout(payout_layout)

            product_layout.addLayout(revenue_container_layout)

    def handle_update_clicked(self):
        product_id, widgets = self.get_product_and_widgets()
        if not product_id or not widgets:
            return

        new_sold, quantity = self.val_quantities(widgets)
        if new_sold is None or quantity is None:
            return
        if new_sold > quantity:
            QMessageBox.warning(self.sender(), "Invalid Input", f"Sold quantity ({new_sold}) exceeds Signed quantity ({quantity})")
            log.error(f"Update failed: Sold quantity exceeds signed quantity")
            return
        if new_sold < 0:
            QMessageBox.warning(self.sender(), "Invalid Input", f"Sold quantity ({new_sold}) must be positive")
            log.error(f"Update failed: Sold quantity must be positive")
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

        if not sold_input.text().strip():
            log.error("Sold field is empty")
            return None, None

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