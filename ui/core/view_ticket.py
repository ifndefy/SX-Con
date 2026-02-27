from PyQt6.QtWidgets import QHBoxLayout
from PyQt6.QtWidgets import QLabel
from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtWidgets import QComboBox
from PyQt6.QtWidgets import QPushButton

from services.get_item import get_item
from services.update_property import update_property
from ui.core.revenue_generation import RevenueGeneration
import utils.logger.logger as log

class ViewTicket:
    @staticmethod
    def view_ticket_details(ticket_section, ticket_details):
        details_container = ticket_section['details_container']
        details_container.setObjectName("view_bg")

        product_layout = ticket_section['product_details_layout']

        while product_layout.count():
            child = product_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        ticket_data = ticket_details['ticket_data']
        ticket_id = ticket_data.get('id', '')
        products = ticket_data.get('price_data', {}).get('products', [])
        revenue_sharing = ticket_data.get('revenue_sharing', [])

        # Products section
        valid_products = [p for p in products if p.get('product_id') and p.get('product_id') != 'NULL']

        for index, product in enumerate(valid_products):
            product_id = product.get('product_id')

            # Line 1: Product ID and Product Name
            line1_layout = QHBoxLayout()

            # Product ID
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
            product_name = product.get('product_type', 'Unknown Product')
            if product_id and product_id != 'NULL':
                product_entity = get_item('Entities', 'product', product_id)
                if product_entity:
                    product_name = product_entity.get('product_name', product_name)
            product_name_input = QLineEdit(product_name)
            product_name_input.setObjectName("READ_ONLY")
            product_name_input.setReadOnly(True)
            line1_layout.addWidget(product_name_input)

            line1_layout.addStretch()

            line1_layout.addWidget(QLabel("Sold:"))
            sold_input = QLineEdit(str(product.get('sold', 0)))
            sold_input.setFixedWidth(100)
            line1_layout.addWidget(sold_input)

            update_btn = QPushButton("Update")
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
            price = (product.get('price', 0)) if product.get('price') else 0
            price = fix_price(price)
            price_input = QLineEdit(price)
            price_input.setFixedWidth(100)
            price_input.setObjectName("READ_ONLY")
            price_input.setReadOnly(True)
            line2_layout.addWidget(price_input)

            # Quantity
            line2_layout.addWidget(QLabel("Qty:"))
            quantity_input = QLineEdit(str(product.get('quantity', 0)))
            quantity_input.setFixedWidth(100)
            quantity_input.setObjectName("READ_ONLY")
            quantity_input.setReadOnly(True)
            line2_layout.addWidget(quantity_input)

            line2_layout.addStretch()

            product_layout.addLayout(line2_layout)

        def make_update_handler(product_index, sold_widget):
            def handler():
                sold_value = sold_widget.text()
                try:
                    sold_int = int(sold_value)
                    result = update_property("Consignments", "consignment", "100000",
                                             f"price_data.products[{product_index}].sold", sold_int)
                    if result == 0:
                        log.info(f"Successfully updated sold quantity to {sold_int}")
                    else:
                        log.error(f"Failed to update sold quantity")
                except ValueError:
                    log.error(f"Invalid sold value: {sold_value}. Please enter a valid number.")

            return handler

            # todo: sxc-266
            update_btn.clicked.connect(make_update_handler(index, sold_input))

        # Revenue Sharing section
        if revenue_sharing:
            revenue_container_layout = QHBoxLayout()
            revenue_container_layout.setObjectName("view_bg")
            revenue_container_layout.addStretch(1)
            revenue_widget = RevenueGeneration()
            revenue_widget.set_revenue_data(revenue_sharing)
            revenue_container_layout.addWidget(revenue_widget)
            product_layout.addLayout(revenue_container_layout)

def fix_price(price_val):
    """
    :Purpose: inserts dollar sign in front of price should it not have it (this is due to how older records did not insert $"
    :Parameter: price
    :Return: $ + price if not startswith("$")
    :Author(s): Joe Lee
    """
    price_str = str(price_val)
    if not price_str.startswith('$'):
        price_str = '$' + price_str
    return price_str
