from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtWidgets import QHBoxLayout
from PyQt6.QtWidgets import QLabel
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtWidgets import QScrollArea
from PyQt6.QtWidgets import QWidget

from ui.tabs.base import BaseTab

class GetTab(BaseTab):
    def __init__(self, api_handler, db_connection):
        self.ticket_counter = None
        self.tickets_layout = None
        self.tickets_section = []
        self.db_connection = db_connection

        super().__init__(api_handler, "get")

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

        # Vendor Line 0 Creation: Vendor Information on left + Ticket Number on right
        vendor_section_row_0 = QHBoxLayout()

        # Vendor Information vendor_title
        vendor_title = QLabel("Vendor Information")
        vendor_title.setObjectName("post_title")
        vendor_section_row_0.addWidget(vendor_title)

        # Push to the left
        vendor_section_row_0.addStretch()

        # Ends creation and adds vendor_section_row_0 to window
        layout.addLayout(vendor_section_row_0)

        # Vendor Line 1 Creation: Vendor ID + Phone Number + Date and Time
        vendor_section_row_1 = QHBoxLayout()

        # Vendor ID
        vendor_section_row_1.addWidget(QLabel("Vendor ID:"))
        self.vendor_id_input = QLineEdit()
        self.vendor_id_input.setPlaceholderText("4 INTS")
        self.vendor_id_input.setMaxLength(4)
        self.vendor_id_input.setFixedWidth(80)
        vendor_section_row_1.addWidget(self.vendor_id_input)

        # Phone Number
        vendor_section_row_1.addWidget(QLabel("Phone Number:"))
        self.phone_input = QLineEdit()
        self.phone_input.setObjectName("READ_ONLY")
        self.phone_input.setPlaceholderText("READ_ONLY_FROM_DB")
        self.phone_input.setReadOnly(True)
        self.phone_input.setFixedWidth(150)
        vendor_section_row_1.addWidget(self.phone_input)

        vendor_section_row_1.addStretch()
        # Ends creation and adds vendor_section_row_1 to window
        layout.addLayout(vendor_section_row_1)

        # Vendor Line 2: First Name + Middle Name + Last Name
        vendor_section_row_2 = QHBoxLayout()

        # First Name
        vendor_section_row_2.addWidget(QLabel("First Name:"))
        self.first_name_input = QLineEdit()
        self.first_name_input.setObjectName("READ_ONLY")
        self.first_name_input.setPlaceholderText("READ_ONLY_FROM_DB")
        self.first_name_input.setReadOnly(True)
        self.first_name_input.setMaxLength(30)
        self.first_name_input.setMinimumWidth(263)
        vendor_section_row_2.addWidget(self.first_name_input)

        # Middle Name
        vendor_section_row_2.addWidget(QLabel("Middle Name:"))
        self.middle_name_input = QLineEdit()
        self.middle_name_input.setObjectName("READ_ONLY")
        self.middle_name_input.setPlaceholderText("READ_ONLY_FROM_DB")
        self.middle_name_input.setReadOnly(True)
        self.middle_name_input.setMaxLength(10)
        self.middle_name_input.setMinimumWidth(103)
        vendor_section_row_2.addWidget(self.middle_name_input)

        # Last Name
        vendor_section_row_2.addWidget(QLabel("Last Name:"))
        self.last_name_input = QLineEdit()
        self.last_name_input.setObjectName("READ_ONLY")
        self.last_name_input.setPlaceholderText("READ_ONLY_FROM_DB")
        self.last_name_input.setReadOnly(True)
        self.last_name_input.setMaxLength(30)
        self.last_name_input.setMinimumWidth(263)
        vendor_section_row_2.addWidget(self.last_name_input)

        # End creation and adds vendor_section_row_2 to the window
        layout.addLayout(vendor_section_row_2)

        # Vendor Line 3: Address + City + State
        vendor_section_row_3 = QHBoxLayout()

        # Address
        vendor_section_row_3.addWidget(QLabel("Address:"))
        self.address_input = QLineEdit()
        self.address_input.setObjectName("READ_ONLY")
        self.address_input.setPlaceholderText("READ_ONLY_FROM_DB")
        self.address_input.setReadOnly(True)
        self.address_input.setMaxLength(255)
        vendor_section_row_3.addWidget(self.address_input)

        # City
        vendor_section_row_3.addWidget(QLabel("City:"))
        self.city_input = QLineEdit()
        self.city_input.setObjectName("READ_ONLY")
        self.city_input.setPlaceholderText("READ_ONLY_FROM_DB")
        self.city_input.setReadOnly(True)
        self.city_input.setMaxLength(30)
        vendor_section_row_3.addWidget(self.city_input)

        # State
        vendor_section_row_3.addWidget(QLabel("State:"))
        self.state_input = QLineEdit()
        self.state_input.setObjectName("READ_ONLY")
        self.state_input.setPlaceholderText("XX")
        self.state_input.setReadOnly(True)
        self.state_input.setMaxLength(2)
        self.state_input.setFixedWidth(50)
        vendor_section_row_3.addWidget(self.state_input)

        # Zip Code
        vendor_section_row_3.addWidget(QLabel("Zip Code:"))
        self.zip_input = QLineEdit()
        self.zip_input.setObjectName("READ_ONLY")
        self.zip_input.setPlaceholderText("XXXXX")
        self.zip_input.setReadOnly(True)
        self.zip_input.setMaxLength(5)
        self.zip_input.setFixedWidth(70)
        vendor_section_row_3.addWidget(self.zip_input)

        # End creation and adds vendor_section_row_3 to the window
        layout.addLayout(vendor_section_row_3)

        vendor_section_row_3 = QHBoxLayout()
        vendor_section_row_3.addStretch()
        self.fetch_btn = QPushButton("Fetch")
        self.fetch_btn.setFixedWidth(200)
        vendor_section_row_3.addWidget(self.fetch_btn)
        layout.addLayout(vendor_section_row_3)

        # HR Line between Vendor and Tickets sections
        hr1 = QLabel()
        hr1.setObjectName("hr")
        layout.addWidget(hr1)

        # Tickets Line 0: title
        ticket_section_row_0 = QHBoxLayout()

        # Ticket Information title
        ticket_title = QLabel("Tickets")
        ticket_title.setObjectName("post_title")
        ticket_section_row_0.addWidget(ticket_title)

        # End creation and adds ticket_section_row_0 to the window
        layout.addLayout(ticket_section_row_0)

        # Ticket Line 1: Tickets sections container
        self.tickets_layout = QVBoxLayout()

        layout.addLayout(self.tickets_layout)

        ticket_section_row_1 = QHBoxLayout()

        layout.addLayout(ticket_section_row_1)
        layout.addStretch(1)

        # HR Line to separate buttons at the bottom
        hr3 = QLabel()
        hr3.setObjectName("hr")
        layout.addWidget(hr3)

        # Status Section
        status_container = QWidget()
        status_container.setObjectName("status_container")
        status_section = QHBoxLayout(status_container)

        # Align to center
        status_section.addStretch()
        self.status_label = QLabel("Ready to create record")
        status_section.addWidget(self.status_label, alignment=Qt.AlignmentFlag.AlignCenter)
        status_section.addStretch()

        layout.addWidget(status_container)

        # Set up the scroll area
        scroll.setWidget(scroll_content)
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(scroll)

        self.setup_button_connections()

    def add_ticket_section(self):
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

        # ticket_num
        line1_layout.addWidget(QLabel("Ticket Number:"))
        ticket_num_input = QLineEdit()
        ticket_num_input.setObjectName("READ_ONLY")
        ticket_num_input.setPlaceholderText("XXXX")
        ticket_num_input.setReadOnly(True)
        ticket_num_input.setMaxLength(4)
        ticket_num_input.setFixedWidth(60)
        line1_layout.addWidget(ticket_num_input)
        tickets_section['ticket_num'] = ticket_num_input

        # datetime
        line1_layout.addWidget(QLabel("Date and Time:"))
        datetime_input = QLineEdit()
        datetime_input.setObjectName("READ_ONLY")
        datetime_input.setPlaceholderText("10/29/2025--04:48:00")
        datetime_input.setReadOnly(True)
        datetime_input.setFixedWidth(250)
        line1_layout.addWidget(datetime_input)
        tickets_section['datetime'] = datetime_input

        # status
        line1_layout.addWidget(QLabel("Status:"))
        status_input = QLineEdit()
        status_input.setObjectName("READ_ONLY")
        status_input.setPlaceholderText("CLOSED")
        status_input.setReadOnly(True)
        status_input.setFixedWidth(80)
        line1_layout.addWidget(status_input)
        tickets_section['status'] = status_input

        line1_layout.addStretch()

        # btns
        self.view_btn = QPushButton("View")
        line1_layout.addWidget(self.view_btn)
        self.excel_btn = QPushButton("Excel")
        line1_layout.addWidget(self.excel_btn)
        self.pdf_btn = QPushButton("PDF")
        line1_layout.addWidget(self.pdf_btn)
        self.print_btn = QPushButton("Print")
        line1_layout.addWidget(self.print_btn)

        section_layout.addLayout(line1_layout)

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
        self.status_label.setText("All tickets cleared")

    def on_fetch_clicked(self):
        """
        :purpose: calls fetch method and adds ticket sections
        :return: None
        :author(s): Joe Lee
        """
        self.remove_ticket_section()
        vendor_id = self.vendor_id_input.text().strip()
        if vendor_id:
            tickets = self.fetch(vendor_id)
            if not tickets:
                self.status_label.setText(f"No tickets found for Vendor ID: {vendor_id}")
            else:
                for ticket in tickets:
                    self.add_ticket_section()
        else:
            self.status_label.setText("Please enter a Vendor ID")

    def fetch(self, vendor_id_input):
        """
        :purpose: fetches all tickets with vendor_id_input from Consignments container
        :return: list of tickets
        :author(s): Joe Lee
        """
        try:
            container = self.db_connection.connect("Consignments")

            query = """
                    SELECT c.ticket_number, c.datetime, c.vendor_id
                    FROM c
                    WHERE c.vendor_id = @vendor_id
                    ORDER BY c.ticket_number DESC
                    """

            parameters = [
                {"name": "@vendor_id", "value": int(vendor_id_input)}  # SEARCH AS INTEGER
            ]

            results = list(container.query_items(
                query=query,
                parameters=parameters,
                enable_cross_partition_query=True
            ))

            tickets = []
            for item in results:
                tickets.append({
                    'ticket_number': item['ticket_number'],
                    'datetime': item['datetime'],
                    'vendor_id': item['vendor_id']
                })
            return tickets

        except Exception as e:
            print(f"Error fetching tickets: {e}")
            return []

    def setup_button_connections(self):
        """
        :purpose: links buttons with methods
        :return: None
        :author(s): Joe Lee
        """
        self.fetch_btn.clicked.connect(self.on_fetch_clicked)
        # self.view_btn.clicked.connect()
        # self.excel_btn.clicked.connect()
        # self.pdf_btn.clicked.connect()
        # self.print_btn.clicked.connect()