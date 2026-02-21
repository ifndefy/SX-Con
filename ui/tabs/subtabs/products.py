from PyQt6.QtWidgets import QVBoxLayout
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
        self.product_type = ['Hot_Food', 'General', 'Produce']
        self.products_section = []
        self.db_connection = db_connection
        super().__init__(api_handler, "products")

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

        # Push to the left
        header_section.addStretch()

        # Ends creation and adds header_section to window
        layout.addLayout(header_section)

        # HR Line between Vendor and Products sections
        hr1 = QLabel()
        hr1.setObjectName("hr")
        layout.addWidget(hr1)

        # Product Line 1: Products sections container
        self.products_layout = QVBoxLayout()

        layout.addLayout(self.products_layout)

        products_section = QHBoxLayout()

        layout.addLayout(products_section)
        layout.addStretch()

        product_section_row_3 = QHBoxLayout()
        self.create_btn = QPushButton("Create New Product")
        product_section_row_3.addWidget(self.create_btn)

        product_section_row_3.addStretch()

        self.update_btn = QPushButton("Update")
        product_section_row_3.addWidget(self.update_btn)
        layout.addLayout(product_section_row_3)

        # HR Line to separate buttons at the bottom
        hr3 = QLabel()
        hr3.setObjectName("hr")
        layout.addWidget(hr3)

        # Set up the scroll area
        scroll.setWidget(scroll_content)
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(scroll)

        self.setup_button_connections()

    def add_product_section(self):
        """
        :purpose: adds product lines
        :return: None
        :author(s): Joe Lee
        """
        prods_section = {}

        # product section container
        section_widget = QWidget()
        section_layout = QVBoxLayout(section_widget)
        section_layout.setContentsMargins(0, 0, 0, 0)

        # Line 1: product_num + datetime + status + buttons
        line1_layout = QHBoxLayout()

        # user id
        line1_layout.addWidget(QLabel("ProductID:"))
        product_id = QLineEdit()
        product_id.setPlaceholderText("10 DIGITS")
        product_id.setObjectName("READ_ONLY")
        product_id.setReadOnly(True)
        product_id.setMaxLength(30)
        product_id.setFixedWidth(120)
        line1_layout.addWidget(product_id)

        # username
        line1_layout.addWidget(QLabel("Product Name:"))
        product_name = QLineEdit()
        product_name.setPlaceholderText("30 CHAR")
        product_name.setObjectName("READ_ONLY")
        product_name.setReadOnly(True)
        product_name.setMaxLength(30)
        product_name.setFixedWidth(265)
        line1_layout.addWidget(product_name)

        line1_layout.addStretch()

        # last consignment
        line1_layout.addWidget(QLabel("Last Consignment:"))
        last_con = QLineEdit()
        last_con.setObjectName("READ_ONLY")
        last_con.setPlaceholderText("datetime")
        last_con.setReadOnly(True)
        last_con.setMaxLength(30)
        last_con.setFixedWidth(190)
        line1_layout.addWidget(last_con)

        section_layout.addLayout(line1_layout)

        line2_layout = QHBoxLayout()
        line2_layout.addWidget(QLabel("Average Price:"))
        avg_price = QLineEdit()
        avg_price.setObjectName("READ_ONLY")
        avg_price.setPlaceholderText("$")
        avg_price.setReadOnly(True)
        avg_price.setMaxLength(30)
        avg_price.setFixedWidth(190)
        line2_layout.addWidget(avg_price)

        line2_layout.addStretch()

        line2_layout.addWidget(QLabel("last Price:"))
        last_price = QLineEdit()
        last_price.setObjectName("READ_ONLY")
        last_price.setPlaceholderText("$")
        last_price.setReadOnly(True)
        last_price.setMaxLength(30)
        last_price.setFixedWidth(190)
        line2_layout.addWidget(last_price)

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

        # HR Line between Vendor and Product sections
        hr = QLabel()
        hr.setObjectName("hr")
        section_layout.addWidget(hr)

        # Add to container
        self.products_layout.addWidget(section_widget)
        self.products_section.append(prods_section)

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
                self.add_product_section()

    def fetch(self):
        """
        :purpose: fetches all products from Entities container
        :return: list of products
        :author(s): Joe Lee
        """
        try:
            container = self.db_connection.connect("Entities")

            query = """
            SELECT c.id, c.product_id, c.product_name, c.notes
            FROM c
            WHERE c.type = 'product'
            ORDER BY c.product_id ASC
            """

            results = list(container.query_items(
                query=query,
                enable_cross_partition_query=True
            ))

            products = []
            for item in results:
                products.append({
                    'product_id': item.get('product_id', ''),
                    'product_name': item.get('product_name', ''),
                })
            return products

        except Exception as e:
            log.error(f"Error fetching products: {e}")
            return []

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
        product_type_input.addItems(self.product_type)
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
            "rate": dialog.findChild(QLineEdit, "rate_input").text()
        }
        return raw_product_data

    def validate_product_data(self, dialog):
        return True

    def setup_button_connections(self):
        """
        :purpose: links buttons with methods
        :return: None
        :author(s): Joe Lee
        """
        self.update_btn.clicked.connect(self.fetch_on_clicked)
        self.create_btn.clicked.connect(self.create_new_product_prompt)