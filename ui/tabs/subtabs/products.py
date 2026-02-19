from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QVBoxLayout, QTabWidget
from PyQt6.QtWidgets import QHBoxLayout
from PyQt6.QtWidgets import QLabel
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtWidgets import QScrollArea
from PyQt6.QtWidgets import QWidget

from services.connect_database import db_connection
from ui.tabs.base import BaseTab
import utils.logger.logger as log
from services.message_bus import status_bar_instance

class ProductsTab(BaseTab):
    def __init__(self, api_handler, db_connection):
        self.tickets_section = []
        self.db_connection = db_connection
        super().__init__(api_handler, "products")

    def setup_ui(self):
        """
        :purpose: initializes the "Create New Record" tab
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

        # Ticket Header
        title = QLabel("View Products")
        title.setObjectName("post_title")
        header_section.addWidget(title)

        # Push to the left
        header_section.addStretch()

        # Ends creation and adds header_section to window
        layout.addLayout(header_section)

        # HR Line between Vendor and Tickets sections
        hr1 = QLabel()
        hr1.setObjectName("hr")
        layout.addWidget(hr1)

        # Ticket Line 1: Tickets sections container
        self.tickets_layout = QVBoxLayout()

        layout.addLayout(self.tickets_layout)

        tickets_section = QHBoxLayout()

        layout.addLayout(tickets_section)
        layout.addStretch()

        vendor_section_row_3 = QHBoxLayout()
        self.create_btn = QPushButton("Create New Product")
        vendor_section_row_3.addWidget(self.create_btn)

        vendor_section_row_3.addStretch()

        self.update_btn = QPushButton("Update")
        vendor_section_row_3.addWidget(self.update_btn)
        layout.addLayout(vendor_section_row_3)

        # HR Line to separate buttons at the bottom
        hr3 = QLabel()
        hr3.setObjectName("hr")
        layout.addWidget(hr3)

        # Set up the scroll area
        scroll.setWidget(scroll_content)
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(scroll)

        self.setup_button_connections()

    def add_user_section(self):
        """
        :purpose: adds ticket lines
        :return: None
        :author(s): Joe Lee
        """
        tickets_section = {}

        # Ticket section container
        section_widget = QWidget()
        section_layout = QVBoxLayout(section_widget)
        section_layout.setContentsMargins(0, 0, 0, 0)

        # Line 1: ticket_num + datetime + status + buttons
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
        self.tickets_layout.addWidget(section_widget)
        self.tickets_section.append(tickets_section)

    def remove_ticket_section(self):
        """
        :purpose: removes and clears all ticket sections
        :return: None
        :author(s): Joe Lee
        """
        # Remove all widgets from the layout
        for i in reversed(range(self.tickets_layout.count())):
            widget = self.tickets_layout.itemAt(i).widget()
            if widget:
                self.tickets_layout.removeWidget(widget)
                widget.deleteLater()

        # Clear the tickets_section list
        self.tickets_section.clear()

        # Update status
        status_bar_instance.send_message("All tickets cleared")

    def fetch_on_clicked(self):
        """
        :purpose: calls fetch method and adds ticket sections
        :return: None
        :author(s): Joe Lee
        """
        self.remove_ticket_section()
        products = self.fetch()
        if not products:
            log.error("No products found")
        else:
            for product in products:
                self.add_user_section()

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

    def setup_button_connections(self):
        """
        :purpose: links buttons with methods
        :return: None
        :author(s): Joe Lee
        """
        self.update_btn.clicked.connect(self.fetch_on_clicked)