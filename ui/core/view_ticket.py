from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout, QLabel, QWidget, QLineEdit, QComboBox, QPushButton
from services.get_item import get_item
from ui.core.revenue_generation import RevenueGeneration


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
        products = ticket_data.get('price_data', {}).get('products', [])
        revenue_sharing = ticket_data.get('revenue_sharing', [])

        # Products section
        valid_products = [p for p in products if p.get('product_id') and p.get('product_id') != 'NULL']

        for product in valid_products:
            # Line 1: Product ID and Product Name
            line1_layout = QHBoxLayout()

            # Product ID
            line1_layout.addWidget(QLabel("ID:"))
            product_id_input = QLineEdit(product.get('product_id', ''))
            product_id_input.setFixedWidth(120)
            product_id_input.setObjectName("READ_ONLY")
            product_id_input.setReadOnly(True)
            line1_layout.addWidget(product_id_input)

            # Product Type
            line1_layout.addWidget(QLabel("Type:"))
            product_type_input = QComboBox()
            product_types = ["SELECT", "Hot Food", "General Item", "Produce"]
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
            product_id = product.get('product_id')
            if product_id and product_id != 'NULL':
                product_entity = get_item('Entities', 'product', product_id)
                if product_entity:
                    product_name = product_entity.get('product_name', product_name)
            product_name_input = QLineEdit(product_name)
            product_name_input.setObjectName("READ_ONLY")
            product_name_input.setReadOnly(True)
            line1_layout.addWidget(product_name_input)

            line1_layout.addStretch()

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
            price = float(product.get('price', 0)) if product.get('price') else 0
            price_input = QLineEdit(f"${price:.2f}")
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

        # Revenue Sharing section
        if revenue_sharing:
            revenue_container_layout = QHBoxLayout()
            revenue_container_layout.addStretch(1)
            revenue_widget = RevenueGeneration()
            revenue_widget.set_revenue_data(revenue_sharing)
            revenue_container_layout.addWidget(revenue_widget)
            product_layout.addLayout(revenue_container_layout)