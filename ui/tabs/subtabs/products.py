from PyQt6.QtCore import QTimer
from PyQt6.QtCore import QRegularExpression
from PyQt6.QtGui import QRegularExpressionValidator
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtWidgets import QFrame
from PyQt6.QtWidgets import QComboBox
from PyQt6.QtWidgets import QHBoxLayout
from PyQt6.QtWidgets import QLabel
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtWidgets import QScrollArea
from PyQt6.QtWidgets import QWidget
from PyQt6.QtWidgets import QDialog

from services.message_bus import status_bar_instance
from ui.tabs.base import BaseTab

from datetime import datetime

from src.core import get_average_price as avg
from src.core import get_latest_price as latest
from services.insert_item import insert_item
from services.update_property import update_property

import utils.logger.logger as log

class ProductsTab(BaseTab):
    def __init__(self, api_handler, db_connection):
        self.list_prod_types = ['Hot Food', 'General', 'Produce']
        self.products_section = []
        self.db_connection = db_connection
        super().__init__(api_handler, "products")

        self.search_timer = QTimer()
        self.search_timer.setSingleShot(True)
        self.search_timer.timeout.connect(self.build_and_search)

    def setup_ui(self):
        """
        :purpose: initializes the "Create New Product" tab
        :return: None
        :author(s): Joe Lee
        """
        background = QVBoxLayout(self)

        main_layout_widget = QWidget()
        main_layout = QVBoxLayout(main_layout_widget)

        header_section = QHBoxLayout()
        title = QLabel("View Products")
        title.setObjectName("post_title")
        header_section.addWidget(title)
        header_section.addStretch() # push to the left

        self.create_btn = QPushButton("Create New Product")
        self.create_btn.setFixedWidth(200)
        header_section.addWidget(self.create_btn)

        # Ends creation and adds header_section to window
        main_layout.addLayout(header_section)

        hr1 = QFrame()
        hr1.setFrameShape(QFrame.Shape.HLine)
        hr1.setFrameShadow(QFrame.Shadow.Sunken)
        hr1.setObjectName("hr")
        main_layout.addWidget(hr1)

        product_section_row_1 = QHBoxLayout()

        product_section_row_1.addWidget(QLabel("ProductID:"))
        self.product_id_input = QLineEdit()
        self.product_id_input.setPlaceholderText("P ID")
        self.product_id_input.setMaxLength(10)
        self.product_id_input.setFixedWidth(102)
        product_id_validator = QRegularExpressionValidator(QRegularExpression("[0-9]{0,10}"))
        self.product_id_input.setValidator(product_id_validator)
        self.product_id_input.textChanged.connect(self.on_search_input_changed)
        product_section_row_1.addWidget(self.product_id_input)

        product_section_row_1.addWidget(QLabel("Product Name:"))
        self.product_name_input = QLineEdit()
        self.product_name_input.setPlaceholderText("Produce Name")
        self.product_name_input.setMaxLength(30)
        self.product_name_input.setFixedWidth(265)
        alpha_validator = QRegularExpressionValidator(QRegularExpression("[A-Za-z ]+"))
        self.product_name_input.setValidator(alpha_validator)
        self.product_name_input.textChanged.connect(self.on_search_input_changed)
        product_section_row_1.addWidget(self.product_name_input)

        product_section_row_1.addStretch()

        product_section_row_1.addWidget(QLabel("Last Consignment:"))
        self.last_consignment_input = QLineEdit()
        self.last_consignment_input.setPlaceholderText("Last Consignment")
        self.last_consignment_input.setMaxLength(30)
        self.last_consignment_input.setFixedWidth(265)
        self.last_consignment_input.textChanged.connect(self.on_search_input_changed)
        product_section_row_1.addWidget(self.last_consignment_input)

        main_layout.addLayout(product_section_row_1)

        product_section_row_2 = QHBoxLayout()

        product_section_row_2.addWidget(QLabel("Product Type:"))
        self.product_type_input = QComboBox()
        self.product_type_input.addItems(self.list_prod_types)
        self.product_type_input.setPlaceholderText("Produce Type")
        self.product_type_input.setCurrentIndex(-1)
        self.product_type_input.currentIndexChanged.connect(self.on_search_input_changed)
        product_section_row_2.addWidget(self.product_type_input)

        product_section_row_2.addStretch()
        main_layout.addLayout(product_section_row_2)

        search_section_1 = QHBoxLayout()
        self.clear_btn = QPushButton("Clear")
        self.clear_btn.setFixedWidth(200)
        search_section_1.addWidget(self.clear_btn)

        search_section_1.addStretch()
        self.search_btn = QPushButton("Search")
        self.search_btn.setFixedWidth(200)
        search_section_1.addWidget(self.search_btn)
        main_layout.addLayout(search_section_1)

        hr2 = QFrame()
        hr2.setFrameShape(QFrame.Shape.HLine)
        hr2.setFrameShadow(QFrame.Shadow.Sunken)
        hr2.setObjectName("hr")
        main_layout.addWidget(hr2)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)

        # Products sections container
        self.products_layout = QVBoxLayout()
        scroll_layout.addLayout(self.products_layout)
        scroll_layout.addStretch()

        scroll.setWidget(scroll_content)
        main_layout.addWidget(scroll)
        background.addWidget(main_layout_widget)
        self.setup_button_connections()

    def clear(self):
        """
        :purpose: clears all input fields and fetched items
        :author(s): Joe Lee, Colin Henderson
        """
        self.search_timer.stop()
        self.remove_product_section()
        fields = [
            self.product_id_input,
            self.product_name_input,
        ]

        for field in fields:
            field.blockSignals(True)
            field.clear()
            field.setReadOnly(False)
            field.setObjectName("DEFAULT")
            field.blockSignals(False)
            field.style().unpolish(field)
            field.style().polish(field)

        self.product_type_input.blockSignals(True)
        self.product_type_input.setCurrentIndex(-1)
        self.product_type_input.blockSignals(False)
        self.product_type_input.style().unpolish(self.product_type_input)
        self.product_type_input.style().polish(self.product_type_input)

        status_bar_instance.send_message("Query and Results cleared")

    def on_search_input_changed(self):
        """
        :Purpose: forces a wait
        :Author(s): Joe Lee
        """
        self.search_timer.start(300)

    def build_and_search(self):
        """
        :Purpose: Gathers properties to build a query then calls query_db
        :Author(s): Joe Lee
        """
        self.remove_product_section()

        conditions = ["c.type = 'product'"]
        properties = []

        def add_property(props, value, operator="="):
            """
            :Purpose: appends query conditions
            :Author(s): Joe Lee
            """
            if value:
                prop_name = props
                if operator == "CONTAINS":
                    conditions.append(f"CONTAINS(LOWER(c.{props}), LOWER(@{prop_name}))")
                else:
                    conditions.append(f"c.{props} {operator} @{prop_name}")
                properties.append({"name": f"@{prop_name}", "value": value})

        product_id = self.product_id_input.text().strip()
        if product_id:
            try:
                product_id_int = int(product_id)
                add_property("product_id", product_id_int, "=")
            except ValueError:
                pass

        product_name = self.product_name_input.text().strip()
        if product_name:
            add_property("product_name", product_name, "CONTAINS")

        last_consignment = self.last_consignment_input.text().strip()
        last_consignment = self.last_consignment_input.text().strip()
        if last_consignment:
            try:
                consignment_container = self.db_connection.connect("Consignments")
                consignment_query = f"""
                    SELECT DISTINCT p.product_id
                    FROM c
                    JOIN p IN c.products
                    WHERE c.type = 'consignment'
                    AND CONTAINS(c.datetime, '{last_consignment}')
                """
                results = list(consignment_container.query_items(
                    query=consignment_query,
                    enable_cross_partition_query=True
                ))

                matching_product_ids = []
                for r in results:
                    if r.get('product_id'):
                        matching_product_ids.append(int(r['product_id']))

                if not matching_product_ids:
                    self.remove_product_section()
                    status_bar_instance.send_message("No products found")
                    return

                id_parts = []
                for prod_id in matching_product_ids:
                    id_parts.append(str(prod_id))
                id_list = ", ".join(id_parts)

                conditions.append(f"c.product_id IN ({id_list})")
            except Exception as e:
                log.error(f"Error querying consignments: {e}")
                return

        product_type = self.product_type_input.currentText().strip()
        if product_type:
            add_property("product_type", product_type, "=")

        if len(conditions) == 1:
            self.fetch()
            return

        where_clause = " AND ".join(conditions)
        search_query = f"SELECT * FROM c WHERE {where_clause}"
        self.query_db(search_query, properties)

    def query_db(self, query: str, properties: list = None):
        """
        :Purpose: Queries against the database
        :Author(s): Joe Lee
        """
        self.remove_product_section()
        try:
            container = self.db_connection.connect("Entities")
            results = list(container.query_items(
                query=query,
                parameters=properties if properties else [],
                enable_cross_partition_query=True
            ))

            products = []
            for item in results:
                products.append({
                    'product_id': item.get('product_id'),
                    'product_name': item.get('product_name', ''),
                    'product_type': item.get('product_type', ''),
                    'rate': item.get('rate', 'NA'),
                })

            products.sort(key=lambda product: int(product['product_id']))

            last_consignments = {}
            try:
                product_ids = []
                for product in products:
                    product_ids.append(product['product_id'])

                consignment_container = self.db_connection.connect("Consignments")

                product_id_parts = []
                for product_id in product_ids:
                    product_id_parts.append(str(product_id))
                product_id_list = ", ".join(product_id_parts)

                last_cons_query = f"""
                    SELECT c.products, c.datetime
                    FROM c
                    WHERE c.type = 'consignment'
                    AND EXISTS(SELECT VALUE p FROM p IN c.products WHERE p.product_id IN ({product_id_list}))
                """
                last_cons = list(consignment_container.query_items(
                    query=last_cons_query,
                    enable_cross_partition_query=True
                ))
                for lc in last_cons:
                    last_con = lc.get('datetime', '')
                    if not last_con:
                        continue
                    try:
                        split_date = datetime.strptime(last_con, "%m/%d/%y -- %H:%M")
                        for product in lc.get('products', []):
                            product_id = int(product.get('product_id'))
                            if ((product_id not in last_consignments) or
                                    (split_date > last_consignments[product_id]['date'])):
                                last_consignments[product_id] = {
                                    'date': split_date,
                                    'full': last_con
                                }
                    except ValueError:
                        continue

                last_consignments = {product_id: value['full'] for product_id, value in last_consignments.items()}

            except Exception as e:
                log.error(f"Error fetching last consignments: {e}")

            for product in products:
                product['last_consignment'] = last_consignments.get(int(product['product_id'])) or ''
                self.add_product_section(product)

            if not products:
                status_bar_instance.send_message("No products found")
            else:
                status_bar_instance.send_message(f"Found {len(products)} products(s)")

        except Exception as e:
            log.error(f"Error executing query: {e}")
            status_bar_instance.send_message("Query failed")

    def fetch(self):
        """
        :purpose: fetches all products from Entities container
        :return: list of products
        :author(s): Joe Lee
        """
        get_all_query = "SELECT * FROM c WHERE c.type = 'product'"
        self.query_db(get_all_query)

    def add_product_section(self, prod_data):
        """
        :purpose: adds product lines
        :return: None
        :author(s): Joe Lee, Tim Liu
        """
        # product section container
        section_widget = QWidget()
        section_layout = QVBoxLayout(section_widget)
        section_layout.setContentsMargins(0, 0, 0, 0)

        # Line 1: product_num + datetime + status + buttons
        line1_layout = QHBoxLayout()

        # user id
        line1_layout.addWidget(QLabel("ProductID:"))
        product_id = QLineEdit()
        product_id.setText(str(prod_data['product_id']))
        product_id.setProperty('pk', 'product_id')
        product_id.setObjectName("LOCKED")
        product_id.setReadOnly(True)
        product_id.setMaxLength(30)
        product_id.setFixedWidth(120)
        line1_layout.addWidget(product_id)

        # product_name
        line1_layout.addWidget(QLabel("Product Name:"))
        product_name = QLineEdit()
        product_name.setText(str(prod_data['product_name']))
        product_name.setProperty('edit_field', 'product_name')
        product_name.setObjectName("READ_ONLY")
        product_name.setReadOnly(True)
        product_name.setMaxLength(30)
        product_name.setMinimumWidth(130)
        line1_layout.addWidget(product_name)

        line1_layout.addWidget(QLabel("Last Consignment:"))
        last_consignment_input = QLineEdit()
        last_consignment_input.setText(prod_data.get('last_consignment') or '')
        last_consignment_input.setObjectName("LOCKED")
        last_consignment_input.setReadOnly(True)
        last_consignment_input.setMaxLength(30)
        last_consignment_input.setFixedWidth(265)
        line1_layout.addWidget(last_consignment_input)

        section_layout.addLayout(line1_layout)

        line2_layout = QHBoxLayout()
        line2_layout.addWidget(QLabel("Product Type:"))
        product_type_input = QComboBox()
        product_type_input.addItems(self.list_prod_types)
        product_type_input.setPlaceholderText("Produce Type")
        product_type_input.setProperty('edit_field', 'product_type')
        index = product_type_input.findText(prod_data['product_type'])
        product_type_input.setCurrentIndex(index)
        product_type_input.setObjectName("READ_ONLY")
        product_type_input.setEnabled(False)
        line2_layout.addWidget(product_type_input)

        line2_layout.addStretch()

        line2_layout.addWidget(QLabel("Rate:"))
        rate_input = QLineEdit()
        rate_input.setText(str(prod_data['rate']))
        rate_input.setProperty('edit_field', 'rate')
        rate_input.setObjectName("READ_ONLY")
        rate_input.setReadOnly(True)
        rate_input.setMaxLength(30)
        rate_input.setFixedWidth(100)
        line2_layout.addWidget(rate_input)

        line2_layout.addStretch()

        line2_layout.addWidget(QLabel("last Price:"))
        last_price = QLineEdit()
        latest_price_val = latest.get_latest_price(prod_data['product_id'])
        last_price.setText(f"${latest_price_val:,.2f}")
        last_price.setObjectName("LOCKED")
        last_price.setReadOnly(True)
        last_price.setMaxLength(30)
        last_price.setFixedWidth(100)
        line2_layout.addWidget(last_price)

        line2_layout.addStretch()

        line2_layout.addWidget(QLabel("Average Price:"))
        avg_price = QLineEdit()
        avg_price_value = avg.get_average_price(prod_data['product_id'])
        avg_price.setText(f"${avg_price_value:,.2f}")
        avg_price.setObjectName("LOCKED")
        avg_price.setReadOnly(True)
        avg_price.setMaxLength(30)
        avg_price.setFixedWidth(100)
        line2_layout.addWidget(avg_price)

        section_layout.addLayout(line2_layout)

        line3_layout = QHBoxLayout()
        # btns
        edit_btn = QPushButton("Edit")
        edit_btn.setObjectName("red_btn")
        line3_layout.addWidget(edit_btn)
        edit_btn.clicked.connect(self.on_edit_clicked)

        section_layout.addLayout(line3_layout)

        hr = QFrame()
        hr.setFrameShape(QFrame.Shape.HLine)
        hr.setFrameShadow(QFrame.Shadow.Sunken)
        hr.setObjectName("hr")
        section_layout.addWidget(hr)

        # Add to container
        self.products_layout.addWidget(section_widget)

    def remove_product_section(self):
        """
        :purpose: removes and clears all product sections
        :return: None
        :author(s): Joe Lee
        """
        # Remove all widgets from the layout
        for i in reversed(range(self.products_layout.count())):
            widget = self.products_layout.itemAt(i).widget()
            if widget:
                self.products_layout.removeWidget(widget)
                widget.deleteLater()

        # Clear the products_section list
        self.products_section.clear()

        # Update status
        status_bar_instance.send_message("All products cleared")

    def fetch_on_clicked(self):
        """
        :purpose: calls fetch method and adds product sections
        :return: None
        :author(s): Joe Lee
        """
        self.remove_product_section()
        products = self.fetch()
        if not products:
            log.error("No products found")
        else:
            for product in products:
                self.add_product_section(product)

    def create_new_product_prompt(self):
        '''
        :purpose: Sets up the UI and uses helper methods to create a product and insert it into the db
        :author(s): Tim Liu
        '''
        dialog = QDialog(self)
        dialog.setWindowTitle("Create New Product")

        layout = QVBoxLayout(dialog)

        # Fields
        layout.addWidget(QLabel("Product ID:"))
        product_id_input = QLineEdit()
        product_id_input.setObjectName("product_id_input")
        layout.addWidget(product_id_input)

        layout.addWidget(QLabel("Product Name:"))
        product_name_input = QLineEdit()
        product_name_input.setObjectName("product_name_input")
        layout.addWidget(product_name_input)

        prompt_label = QLabel("Product Type:")
        layout.addWidget(prompt_label)
        product_type_input= QComboBox()
        product_type_input.addItems(self.list_prod_types)
        product_type_input.setObjectName("product_type_input")
        product_type_input.setCurrentIndex(-1)
        layout.addWidget(product_type_input)

        layout.addWidget(QLabel("rate:"))
        rate_input = QLineEdit()
        rate_input.setObjectName("rate_input")
        layout.addWidget(rate_input)

        layout.addStretch()

        # Buttons
        btn_layout = QHBoxLayout()
        create_btn = QPushButton("Create")
        cancel_btn = QPushButton("Cancel")

        btn_layout.addWidget(create_btn)
        btn_layout.addWidget(cancel_btn)
        layout.addLayout(btn_layout)

        # Connects
        create_btn.clicked.connect(self.on_create_clicked(dialog))
        cancel_btn.clicked.connect(dialog.reject)

        # Execute dialog
        result = dialog.exec()
        if result == QDialog.DialogCode.Accepted:
            self.handle_dialog_accepted(dialog)

    def setup_button_connections(self):
        """
        :purpose: links buttons with methods
        :return: None
        :author(s): Joe Lee
        """
        self.clear_btn.clicked.connect(self.clear)
        self.search_btn.clicked.connect(self.build_and_search)
        self.create_btn.clicked.connect(self.create_new_product_prompt)

    def on_create_clicked(self, dialog):
        """
        :Purpose: handles button initialization
        :Author(s): Tim Liu
        """
        def handler():
            if self.validate_product_data(dialog):
                dialog.accept()
        return handler

    def handle_dialog_accepted(self, dialog):
        """
        :Purpose: executes a sequence of events
        :Author(s): Joe Lee
        """
        self.new_product_data = self.gather_new_product_data(dialog)
        insert_item("Entities", "product", self.new_product_data)

    def gather_new_product_data(self, dialog):
        """
        :Purpose: gathers user data from dialog's input fields
        :Method: passes in dialog then parses dialog for data
        :Author(s): Colin Heinselman, Joe Lee
        """
        raw_product_data = {
            "product_id": int(dialog.findChild(QLineEdit, "product_id_input").text()),
            "product_name": dialog.findChild(QLineEdit, "product_name_input").text(),
            "product_type": dialog.findChild(QComboBox, "product_type_input").currentText(),
            "rate": dialog.findChild(QLineEdit, "rate_input").text(),
            "type": "product"
        }
        return raw_product_data

    def validate_product_data(self, dialog):
        return True

    def on_edit_clicked(self):
        btn = self.sender()
        section_widget = btn.parent()

        for widget in section_widget.findChildren(QLineEdit):
            if widget.objectName() == "READ_ONLY":
                widget.setReadOnly(False)
                widget.setObjectName("DEFAULT")
                widget.style().unpolish(widget)
                widget.style().polish(widget)

        for widget in section_widget.findChildren(QComboBox):
            if widget.objectName() == "READ_ONLY":
                widget.setEnabled(True)
                widget.setObjectName("DEFAULT")
                widget.style().unpolish(widget)
                widget.style().polish(widget)

        btn.setObjectName("DEFAULT")
        btn.style().unpolish(btn)
        btn.style().polish(btn)
        btn.setText("Save")
        btn.clicked.disconnect(self.on_edit_clicked)
        btn.clicked.connect(self.on_save_clicked)

    def on_save_clicked(self):
        btn = self.sender()
        section_widget = btn.parent()

        product_id = None
        for widget in section_widget.findChildren(QLineEdit):
            if widget.property("pk") == "product_id":
                product_id = widget.text()
                break

        btn.setText("Edit")
        btn.setObjectName("red_btn")
        btn.style().unpolish(btn)
        btn.style().polish(btn)
        btn.clicked.disconnect(self.on_save_clicked)
        btn.clicked.connect(self.on_edit_clicked)

        for widget in section_widget.findChildren(QLineEdit):
            if widget.objectName() == "DEFAULT":
                update_property("Entities", "product", product_id, widget.property("edit_field"), widget.text().strip())
                widget.setReadOnly(True)
                widget.setObjectName("READ_ONLY")
                widget.style().unpolish(widget)
                widget.style().polish(widget)

        for widget in section_widget.findChildren(QComboBox):
            if widget.objectName() == "DEFAULT":
                value = widget.currentText()
                update_property("Entities", "product", product_id, widget.property("edit_field"), value)
                widget.setEnabled(False)
                widget.setObjectName("READ_ONLY")
                widget.style().unpolish(widget)
                widget.style().polish(widget)