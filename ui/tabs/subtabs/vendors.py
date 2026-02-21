
from PyQt6.QtWidgets import QVBoxLayout, QDialog
from PyQt6.QtWidgets import QHBoxLayout
from PyQt6.QtWidgets import QLabel
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtWidgets import QScrollArea
from PyQt6.QtWidgets import QWidget

from ui.tabs.base import BaseTab

from services.insert_item import insert_item
import utils.logger.logger as log
from services.message_bus import status_bar_instance

class VendorsTab(BaseTab):
    def __init__(self, api_handler, db_connection):
        self.new_vendor_data = None
        self.vendors_section = []
        self.db_connection = db_connection
        super().__init__(api_handler, "vendors")

    def setup_ui(self):
        """
        :purpose: initializes the "vendors subtab" tab
        :author(s): Joe Lee
        """
        # Enable scrolling for when the content exceeds the height of the window
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        layout = QVBoxLayout(scroll_content)

        header_section = QHBoxLayout()
        title = QLabel("View Vendors") # Subtab header
        title.setObjectName("post_title")
        header_section.addWidget(title)
        header_section.addStretch() # Push to the left
        layout.addLayout(header_section) # Ends creation and adds header_section to window

        hr1 = QLabel()# HR Line
        hr1.setObjectName("hr")
        layout.addWidget(hr1)

        self.vendors_layout = QVBoxLayout() # Vendors container
        layout.addLayout(self.vendors_layout)

        vendors_section = QHBoxLayout()
        layout.addLayout(vendors_section)
        layout.addStretch()

        btn_section = QHBoxLayout()
        self.create_btn = QPushButton("Create New Vendor")
        btn_section.addWidget(self.create_btn)
        self.create_btn.clicked.connect(self.create_new_vendor_prompt)

        btn_section.addStretch()

        self.update_btn = QPushButton("Update")
        btn_section.addWidget(self.update_btn)
        layout.addLayout(btn_section)

        hr3 = QLabel()
        hr3.setObjectName("hr")
        layout.addWidget(hr3)

        # Set up the scroll area
        scroll.setWidget(scroll_content)
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(scroll)

        self.setup_button_connections()

    def add_vendor_section(self, vendor):
        """
        :purpose: adds vendor items
        :author(s): Joe Lee
        """
        # Vendors section container
        section_widget = QWidget()
        section_layout = QVBoxLayout(section_widget)
        section_layout.setContentsMargins(0, 0, 0, 0)

        vendor_section_row_1 = QHBoxLayout()
        vendor_section_row_1.addWidget(QLabel("Vendor ID:"))
        vendor_id_input = QLineEdit()
        vendor_id_input.setText(str(vendor['vendor_id']))
        vendor_id_input.setObjectName("READ_ONLY")
        vendor_id_input.setPlaceholderText("4 INTS")
        vendor_id_input.setReadOnly(True)
        vendor_id_input.setMaxLength(4)
        vendor_id_input.setFixedWidth(80)
        vendor_section_row_1.addWidget(vendor_id_input)

        # Phone Number
        vendor_section_row_1.addWidget(QLabel("Phone Number:"))
        phone_input = QLineEdit()
        phone_input.setText(str(vendor['phone']))
        phone_input.setObjectName("READ_ONLY")
        phone_input.setReadOnly(True)
        phone_input.setMaxLength(12)
        phone_input.setFixedWidth(150)
        vendor_section_row_1.addWidget(phone_input)

        # Ends creation and adds vendor_section_row_1 to window
        vendor_section_row_1.addStretch()
        section_layout.addLayout(vendor_section_row_1)

        # Vendor Line 2: First Name + Middle Name + Last Name
        vendor_section_row_2 = QHBoxLayout()

        # First Name
        vendor_section_row_2.addWidget(QLabel("First Name:"))
        first_name_input = QLineEdit()
        first_name_input.setText(vendor['first_name'])
        first_name_input.setObjectName("READ_ONLY")
        first_name_input.setReadOnly(True)
        first_name_input.setMaxLength(30)
        first_name_input.setMinimumWidth(263)
        vendor_section_row_2.addWidget(first_name_input)

        # Middle Name
        vendor_section_row_2.addWidget(QLabel("Middle Name:"))
        middle_name_input = QLineEdit()
        middle_name_input.setText(vendor['middle_name'])
        middle_name_input.setObjectName("READ_ONLY")
        middle_name_input.setReadOnly(True)
        middle_name_input.setMaxLength(10)
        middle_name_input.setMinimumWidth(103)
        vendor_section_row_2.addWidget(middle_name_input)

        # Last Name
        vendor_section_row_2.addWidget(QLabel("Last Name:"))
        last_name_input = QLineEdit()
        last_name_input.setText(vendor['last_name'])
        last_name_input.setObjectName("READ_ONLY")
        last_name_input.setReadOnly(True)
        last_name_input.setMaxLength(30)
        last_name_input.setMinimumWidth(263)
        vendor_section_row_2.addWidget(last_name_input)

        # End creation and adds vendor_section_row_2 to the window
        section_layout.addLayout(vendor_section_row_2)

        # Vendor Line 3: Address + City + State
        vendor_section_row_3 = QHBoxLayout()

        # Address
        vendor_section_row_3.addWidget(QLabel("Address:"))
        address_input = QLineEdit()
        address_input.setText(vendor['address'])
        address_input.setObjectName("READ_ONLY")
        address_input.setReadOnly(True)
        address_input.setMaxLength(255)
        vendor_section_row_3.addWidget(address_input)

        # City
        vendor_section_row_3.addWidget(QLabel("City:"))
        city_input = QLineEdit()
        city_input.setText(vendor['city'])
        city_input.setObjectName("READ_ONLY")
        city_input.setReadOnly(True)
        city_input.setMaxLength(30)
        vendor_section_row_3.addWidget(city_input)

        # State
        vendor_section_row_3.addWidget(QLabel("State:"))
        state_input = QLineEdit()
        state_input.setText(vendor['state'])
        state_input.setObjectName("READ_ONLY")
        state_input.setReadOnly(True)
        state_input.setMaxLength(2)
        state_input.setFixedWidth(50)
        vendor_section_row_3.addWidget(state_input)

        # Zip Code
        vendor_section_row_3.addWidget(QLabel("Zip Code:"))
        zip_input = QLineEdit()
        zip_input.setText(vendor['zip'])
        zip_input.setObjectName("READ_ONLY")
        zip_input.setReadOnly(True)
        zip_input.setMaxLength(5)
        zip_input.setFixedWidth(70)
        vendor_section_row_3.addWidget(zip_input)

        # End creation and adds vendor_section_row_3 to the window
        section_layout.addLayout(vendor_section_row_3)

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
        self.vendors_layout.addWidget(section_widget)

    def remove_vendor_section(self):
        """
        :purpose: clears subtab widget that holds vendor items
        :author(s): Joe Lee
        """
        # Remove all widgets from the layout
        for i in reversed(range(self.vendors_layout.count())):
            widget = self.vendors_layout.itemAt(i).widget()
            if widget:
                self.vendors_layout.removeWidget(widget)
                widget.deleteLater()

        self.vendors_section.clear()

        # Update status
        status_bar_instance.send_message("All products cleared")

    def fetch_on_clicked(self):
        """
        :purpose: calls fetch method and adds ticket sections
        :return: None
        :author(s): Joe Lee
        """
        vendors = self.fetch()
        if not vendors:
            log.error("No vendors found")
        else:
            for vendor in vendors:
                self.add_vendor_section(vendor)

    def fetch(self):
        """
        :purpose: fetches all vendors from Entities container
        :return: list of vendors
        :author(s): Joe Lee
        """
        self.remove_vendor_section()
        try:
            container = self.db_connection.connect("Entities")

            query = """
            SELECT *
            FROM c
            WHERE c.type = 'vendor'
            """

            results = list(container.query_items(
                query=query,
                enable_cross_partition_query=True
            ))

            vendors = []
            for item in results:
                vendors.append({
                    'vendor_id': item.get('vendor_id', ''),
                    'phone': item.get('phone', ''),
                    'first_name': item.get('first_name', ''),
                    'middle_name': item.get('middle_name', ''),
                    'last_name': item.get('last_name', ''),
                    'address': item.get('address', ''),
                    'city': item.get('city', ''),
                    'state': item.get('state', ''),
                    'zip': item.get('zip', '')
                })

            vendors.sort(key=lambda v: int(v['vendor_id']))

            return vendors

        except Exception as e:
            log.error(f"Error fetching vendors: {e}")
            return []

    def setup_button_connections(self):
        """
        :purpose: links buttons with methods
        :return: None
        :author(s): Joe Lee
        """
        self.update_btn.clicked.connect(self.fetch_on_clicked)

    def create_new_vendor_prompt(self):
        '''
        :purpose: Sets up the UI and uses helper methods to create a user and insert it into the db
        :author(s): Colin Heinselman
        '''
        dialog = QDialog(self)
        dialog.setWindowTitle("Create New Vendor")

        layout = QVBoxLayout(dialog)

        # Fields
        layout.addWidget(QLabel("VendorID:"))
        vendor_id_input = QLineEdit()
        vendor_id_input.setObjectName("vendor_id_input")
        layout.addWidget(vendor_id_input)

        layout.addWidget(QLabel("Phone Number:"))
        phone_number_input = QLineEdit()
        phone_number_input.setObjectName("phone_number_input")
        layout.addWidget(phone_number_input)

        layout.addWidget(QLabel("First Name:"))
        first_name_input = QLineEdit()
        first_name_input.setObjectName("first_name_input")
        layout.addWidget(first_name_input)

        layout.addWidget(QLabel("Middle Name:"))
        middle_name_input = QLineEdit()
        middle_name_input.setObjectName("middle_name_input")
        layout.addWidget(middle_name_input)

        layout.addWidget(QLabel("Last Name:"))
        last_name_input = QLineEdit()
        last_name_input.setObjectName("last_name_input")
        layout.addWidget(last_name_input)

        layout.addWidget(QLabel("Address:"))
        address_input = QLineEdit()
        address_input.setObjectName("address_input")
        layout.addWidget(address_input)

        layout.addWidget(QLabel("City:"))
        city_input = QLineEdit()
        city_input.setObjectName("city_input")
        layout.addWidget(city_input)

        layout.addWidget(QLabel("State:"))
        state_input = QLineEdit()
        state_input.setObjectName("state_input")
        layout.addWidget(state_input)

        layout.addWidget(QLabel("Zip Code:"))
        zip_code_input = QLineEdit()
        zip_code_input.setObjectName("zip_code_input")
        layout.addWidget(zip_code_input)

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
        :Author(s): Joe Lee
        """
        def handler():
            if self.validate_vendor_data(dialog):
                dialog.accept()
        return handler

    def handle_dialog_accepted(self, dialog):
        """
        :Purpose: executes a sequence of events
        :Author(s): Joe Lee
        """
        self.new_vendor_data = self.gather_vendor_data(dialog)
        insert_item("Entities", "vendor", self.new_vendor_data)

    def gather_vendor_data(self, dialog):
        """
        :Purpose: gathers user data from dialog's input fields
        :Method: passes in dialog then parses dialog for data
        :Author(s): Colin Heinselman, Joe Lee
        """
        vendor_doc = {
            "vendor_id": dialog.findChild(QLineEdit, "vendor_id_input").text(),
            "phone": dialog.findChild(QLineEdit, "phone_number_input").text(),
            "first_name": dialog.findChild(QLineEdit, "first_name_input").text(),
            "middle_name": dialog.findChild(QLineEdit, "middle_name_input").text(),
            "last_name": dialog.findChild(QLineEdit, "last_name_input").text(),
            "address": dialog.findChild(QLineEdit, "address_input").text(),
            "city": dialog.findChild(QLineEdit, "city_input").text(),
            "state": dialog.findChild(QLineEdit, "state_input").text(),
            "zip": dialog.findChild(QLineEdit, "zip_code_input").text(),
            "type": "vendor"
        }
        return vendor_doc

    def validate_vendor_data(self, dialog):
        # todo:
        return True