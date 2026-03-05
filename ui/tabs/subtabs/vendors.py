from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QIntValidator
from PyQt6.QtWidgets import QVBoxLayout, QDialog, QFrame
from PyQt6.QtWidgets import QHBoxLayout
from PyQt6.QtWidgets import QLabel
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtWidgets import QScrollArea
from PyQt6.QtWidgets import QWidget

from ui.tabs.base import BaseTab

from ui.core import format_phone
from ui.core import format_state
from services.insert_item import insert_item
import utils.logger.logger as log
from services.message_bus import status_bar_instance

class VendorsTab(BaseTab):
    def __init__(self, api_handler, db_connection):
        self.new_vendor_data = None
        self.vendors_section = []
        self.db_connection = db_connection
        super().__init__(api_handler, "vendors")

        self.search_timer = QTimer()
        self.search_timer.setSingleShot(True)
        self.search_timer.timeout.connect(self.build_and_search)

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

        self.create_btn = QPushButton("Create New Vendor")
        self.create_btn.setFixedWidth(200)
        header_section.addWidget(self.create_btn)

        layout.addLayout(header_section) # Ends creation and adds header_section to window

        hr1 = QFrame()
        hr1.setFrameShape(QFrame.Shape.HLine)
        hr1.setFrameShadow(QFrame.Shadow.Sunken)
        hr1.setObjectName("hr")
        layout.addWidget(hr1)

        search_section_row_1 = QHBoxLayout()

        search_section_row_1.addWidget(QLabel("VendorID:"))
        self.vendor_id_input = QLineEdit()
        self.vendor_id_input.setPlaceholderText("V ID")
        self.vendor_id_input.setMaxLength(4)
        self.vendor_id_input.setFixedWidth(80)
        self.vendor_id_input.setValidator(QIntValidator(0, 9999, self))
        self.vendor_id_input.textChanged.connect(self.on_search_input_changed)
        search_section_row_1.addWidget(self.vendor_id_input)

        search_section_row_1.addWidget(QLabel("Phone Number:"))
        self.phone_number_input = format_phone.PhoneNumField()
        self.phone_number_input.setMaxLength(12)
        self.phone_number_input.setFixedWidth(150)
        self.phone_number_input.textChanged.connect(self.on_search_input_changed)
        search_section_row_1.addWidget(self.phone_number_input)

        search_section_row_1.addStretch()
        layout.addLayout(search_section_row_1)

        search_section_row_2 = QHBoxLayout()

        search_section_row_2.addWidget(QLabel("First Name:"))
        self.first_name_input = QLineEdit()
        self.first_name_input.setPlaceholderText("First Name")
        self.first_name_input.setMaxLength(30)
        self.first_name_input.setFixedWidth(263)
        self.first_name_input.textChanged.connect(self.on_search_input_changed)
        search_section_row_2.addWidget(self.first_name_input)

        search_section_row_2.addWidget(QLabel("Middle Name:"))
        self.middle_name_input = QLineEdit()
        self.middle_name_input.setPlaceholderText("M. Name")
        self.middle_name_input.setMaxLength(10)
        self.middle_name_input.setFixedWidth(103)
        self.middle_name_input.textChanged.connect(self.on_search_input_changed)
        search_section_row_2.addWidget(self.middle_name_input)

        search_section_row_2.addWidget(QLabel("Last Name:"))
        self.last_name_input = QLineEdit()
        self.last_name_input.setPlaceholderText("Last Name")
        self.last_name_input.setMaxLength(30)
        self.last_name_input.setFixedWidth(263)
        self.last_name_input.textChanged.connect(self.on_search_input_changed)
        search_section_row_2.addWidget(self.last_name_input)

        search_section_row_2.addStretch()
        layout.addLayout(search_section_row_2)

        search_section_row_3 = QHBoxLayout()

        search_section_row_3.addWidget(QLabel("Address:"))
        self.address_input = QLineEdit()
        self.address_input.setPlaceholderText("Address")
        self.address_input.setMaxLength(255)
        self.address_input.textChanged.connect(self.on_search_input_changed)
        search_section_row_3.addWidget(self.address_input)

        search_section_row_3.addWidget(QLabel("City:"))
        self.city_input = QLineEdit()
        self.city_input.setPlaceholderText("City")
        self.city_input.setMaxLength(30)
        self.city_input.textChanged.connect(self.on_search_input_changed)
        search_section_row_3.addWidget(self.city_input)

        search_section_row_3.addWidget(QLabel("State:"))
        self.state_input = format_state.FormatState()
        self.state_input.setFixedWidth(50)
        self.state_input.textChanged.connect(self.on_search_input_changed)
        search_section_row_3.addWidget(self.state_input)

        search_section_row_3.addWidget(QLabel("Zip:"))
        self.zip_input = QLineEdit()
        self.zip_input.setPlaceholderText("Zip")
        self.zip_input.setMaxLength(5)
        self.zip_input.setFixedWidth(70)
        self.zip_input.textChanged.connect(self.on_search_input_changed)
        search_section_row_3.addWidget(self.zip_input)

        search_section_row_3.addStretch()
        layout.addLayout(search_section_row_3)

        search_section_row_4 = QHBoxLayout()
        self.clear_btn = QPushButton("Clear")
        self.clear_btn.setFixedWidth(200)
        search_section_row_4.addWidget(self.clear_btn)

        search_section_row_4.addStretch()
        self.search_btn = QPushButton("Search")
        self.search_btn.setFixedWidth(200)
        search_section_row_4.addWidget(self.search_btn)
        layout.addLayout(search_section_row_4)

        hr2 = QFrame()
        hr2.setFrameShape(QFrame.Shape.HLine)
        hr2.setFrameShadow(QFrame.Shadow.Sunken)
        hr2.setObjectName("hr")
        layout.addWidget(hr2)

        self.vendors_layout = QVBoxLayout() # Vendors container
        layout.addLayout(self.vendors_layout)

        vendors_section = QHBoxLayout()
        layout.addLayout(vendors_section)
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
        self.remove_vendor_section()
        fields = [
            self.vendor_id_input,
            self.phone_number_input,
            self.first_name_input,
            self.middle_name_input,
            self.last_name_input,
        ]
        for field in fields:
            field.blockSignals(True)
            field.clear()
            field.setReadOnly(False)
            field.setObjectName("DEFAULT")
            field.blockSignals(False)
            field.style().unpolish(field)
            field.style().polish(field)

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
        self.remove_vendor_section()

        conditions = ["c.type = 'vendor'"]
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

        vendor_id = self.vendor_id_input.text().strip()
        if vendor_id:
            try:
                vendor_id_int = int(vendor_id)
                add_property("vendor_id", vendor_id_int, "=")
            except ValueError:
                pass

        phone = self.phone_number_input.text().strip()
        if phone:
            add_property("phone", phone, "CONTAINS")

        first_name = self.first_name_input.text().strip()
        if first_name:
            add_property("first_name", first_name, "CONTAINS")

        middle_name = self.middle_name_input.text().strip()
        if middle_name:
            add_property("middle_name", middle_name, "CONTAINS")

        last_name = self.last_name_input.text().strip()
        if last_name:
            add_property("last_name", last_name, "CONTAINS")

        address = self.address_input.text().strip()
        if address:
            add_property("address", address, "CONTAINS")

        city = self.city_input.text().strip()
        if city:
            add_property("city", city, "CONTAINS")

        state = self.state_input.text().strip()
        if state:
            add_property("state", state, "CONTAINS")

        zip = self.zip_input.text().strip()
        if zip:
            add_property("zip", zip, "CONTAINS")

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
        self.remove_vendor_section()
        try:
            container = self.db_connection.connect("Entities")
            results = list(container.query_items(
                query=query,
                parameters=properties if properties else [],
                enable_cross_partition_query=True
            ))

            vendors = []
            for item in results:
                vendors.append({
                    'vendor_id': item.get('vendor_id'),
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

            for vendor in vendors:
                self.add_vendor_section(vendor)

            if not vendors:
                status_bar_instance.send_message("No vendors found")
            else:
                status_bar_instance.send_message(f"Found {len(vendors)} vendors(s)")

        except Exception as e:
            log.error(f"Error executing query: {e}")
            status_bar_instance.send_message("Query failed")

    def fetch(self):
        """
        :purpose: fetches all users from Entities container
        :return: list of users
        :author(s): Joe Lee
        """
        get_all_query = "SELECT * FROM c WHERE c.type = 'vendor'"
        self.query_db(get_all_query)

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
        hr = QFrame()
        hr.setFrameShape(QFrame.Shape.HLine)
        hr.setFrameShadow(QFrame.Shadow.Sunken)
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

    def setup_button_connections(self):
        """
        :purpose: links buttons with methods
        :return: None
        :author(s): Joe Lee
        """
        self.clear_btn.clicked.connect(self.clear)
        self.search_btn.clicked.connect(self.build_and_search)
        self.create_btn.clicked.connect(self.create_new_vendor_prompt)

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