from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QIntValidator
from PyQt6.QtWidgets import QVBoxLayout, QFrame
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

from services.insert_item import insert_item
import utils.logger.logger as log

class ProductsTab(BaseTab):
    def __init__(self, api_handler, db_connection):
        self.list_prod_types = ['Hot_Food', 'General', 'Produce']
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
        # Enable scrolling for when the content exceeds the height of the window
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        layout = QVBoxLayout(scroll_content)

        # Line 0 Creation
        header_section = QHBoxLayout()

        # Product Header
        title = QLabel("View Products")
        title.setObjectName("post_title")
        header_section.addWidget(title)
        header_section.addStretch() # push to the left

        self.create_btn = QPushButton("Create New Product")
        header_section.addWidget(self.create_btn)

        # Ends creation and adds header_section to window
        layout.addLayout(header_section)

        hr1 = QFrame()
        hr1.setFrameShape(QFrame.Shape.HLine)
        hr1.setFrameShadow(QFrame.Shadow.Sunken)
        hr1.setObjectName("hr")
        layout.addWidget(hr1)

        product_section_row_1 = QHBoxLayout()

        product_section_row_1.addWidget(QLabel("ProductID:"))
        self.product_id_input = QLineEdit()
        self.product_id_input.setPlaceholderText("P ID")
        self.product_id_input.setMaxLength(30)
        self.product_id_input.setFixedWidth(102)
        self.product_id_input.setValidator(QIntValidator(0, 9999, self))
        self.product_id_input.textChanged.connect(self.on_search_input_changed)
        product_section_row_1.addWidget(self.product_id_input)

        product_section_row_1.addWidget(QLabel("Product Name:"))
        self.product_name_input = QLineEdit()
        self.product_name_input.setPlaceholderText("Produce Name")
        self.product_name_input.setMaxLength(30)
        self.product_name_input.setFixedWidth(265)
        self.product_name_input.textChanged.connect(self.on_search_input_changed)
        product_section_row_1.addWidget(self.product_name_input)

        product_section_row_1.addWidget(QLabel("Product Type:"))
        self.product_type_input = QComboBox()
        self.product_type_input.addItems(self.list_prod_types)
        self.product_type_input.setPlaceholderText("Produce Type")
        self.product_type_input.setCurrentIndex(-1)
        self.product_type_input.currentIndexChanged.connect(self.on_search_input_changed)
        product_section_row_1.addWidget(self.product_type_input)

        product_section_row_1.addStretch()
        layout.addLayout(product_section_row_1)

        product_section_row_last_consignment = QHBoxLayout()

        product_section_row_last_consignment.addWidget(QLabel("Last Consignment:"))
        self.last_consignment_input = QLineEdit()
        self.last_consignment_input.setPlaceholderText("Last Consignment")
        self.last_consignment_input.setMaxLength(30)
        self.last_consignment_input.setFixedWidth(265)
        self.last_consignment_input.textChanged.connect(self.on_search_input_changed)
        product_section_row_last_consignment.addWidget(self.last_consignment_input)

        product_section_row_last_consignment.addStretch()
        layout.addLayout(product_section_row_last_consignment)

        search_section_1 = QHBoxLayout()
        self.clear_btn = QPushButton("Clear")
        self.clear_btn.setFixedWidth(200)
        search_section_1.addWidget(self.clear_btn)

        search_section_1.addStretch()
        self.search_btn = QPushButton("Search")
        self.search_btn.setFixedWidth(200)
        search_section_1.addWidget(self.search_btn)
        layout.addLayout(search_section_1)

        hr2 = QFrame()
        hr2.setFrameShape(QFrame.Shape.HLine)
        hr2.setFrameShadow(QFrame.Shadow.Sunken)
        hr2.setObjectName("hr")
        layout.addWidget(hr2)

        # Products sections container
        self.products_layout = QVBoxLayout()
        layout.addLayout(self.products_layout)
        products_section = QHBoxLayout()
        layout.addLayout(products_section)
        layout.addStretch()

        # Set up the scroll area
        scroll.setWidget(scroll_content)
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(scroll)

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

            products.sort(key=lambda v: int(v['product_id']))

            for prod in products:
                self.add_product_section(prod)

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
        product_id.setObjectName("READ_ONLY")
        product_id.setReadOnly(True)
        product_id.setMaxLength(30)
        product_id.setFixedWidth(120)
        line1_layout.addWidget(product_id)

        # username
        line1_layout.addWidget(QLabel("Product Name:"))
        product_name = QLineEdit()
        product_name.setText(str(prod_data['product_name']))
        product_name.setObjectName("READ_ONLY")
        product_name.setReadOnly(True)
        product_name.setMaxLength(30)
        product_name.setFixedWidth(265)
        line1_layout.addWidget(product_name)

        line1_layout.addStretch()

        section_layout.addLayout(line1_layout)

        line2_layout = QHBoxLayout()
        line2_layout.addWidget(QLabel("Average Price:"))
        avg_price = QLineEdit()
        avg_price.setText("TBD") # todo:
        avg_price.setObjectName("READ_ONLY")
        avg_price.setReadOnly(True)
        avg_price.setMaxLength(30)
        avg_price.setFixedWidth(190)
        line2_layout.addWidget(avg_price)

        line2_layout.addStretch()

        line2_layout.addWidget(QLabel("last Price:"))
        last_price = QLineEdit()
        last_price.setText("TBD")
        last_price.setObjectName("READ_ONLY")
        last_price.setReadOnly(True)
        last_price.setMaxLength(30)
        last_price.setFixedWidth(190)
        line2_layout.addWidget(last_price)

        line2_layout.addStretch()

        line2_layout.addWidget(QLabel("Rate:"))
        rate_input = QLineEdit()
        rate_input.setText(str(prod_data['rate']))
        rate_input.setObjectName("READ_ONLY")
        rate_input.setReadOnly(True)
        rate_input.setMaxLength(30)
        rate_input.setFixedWidth(190)
        line2_layout.addWidget(rate_input)

        section_layout.addLayout(line2_layout)

        line3_layout = QHBoxLayout()
        # btns
        self.view_btn = QPushButton("View")
        line3_layout.addWidget(self.view_btn)
        self.edit_btn = QPushButton("Edit")
        self.edit_btn.setObjectName("red_btn")
        line3_layout.addWidget(self.edit_btn)
        self.del_btn = QPushButton("Delete")
        self.del_btn.setObjectName("red_btn")
        line3_layout.addWidget(self.del_btn)

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
            "product_id": dialog.findChild(QLineEdit, "product_id_input").text(),
            "product_name": dialog.findChild(QLineEdit, "product_name_input").text(),
            "product_type": dialog.findChild(QComboBox, "product_type_input").currentText(),
            "rate": dialog.findChild(QLineEdit, "rate_input").text(),
            "type": "product"
        }
        return raw_product_data

    def validate_product_data(self, dialog):
        return True
