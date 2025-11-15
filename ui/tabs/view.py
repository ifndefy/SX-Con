from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtWidgets import QHBoxLayout
from PyQt6.QtWidgets import QLabel
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtWidgets import QScrollArea
from PyQt6.QtWidgets import QWidget

from ui.tabs.base import BaseTab

class ViewTab(BaseTab):
    def __init__(self, api_handler, db_connection):
        self.ticket_counter = None
        self.tickets_layout = None
        self.tickets_section = []
        self.db_connection = db_connection

        super().__init__(api_handler, "view")

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
        title = QLabel("Open Tickets")
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
        self.update_btn = QPushButton("Update")
        vendor_section_row_3.addWidget(self.update_btn)
        layout.addLayout(vendor_section_row_3)

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
        status_input.setPlaceholderText("OPEN")
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

    def fetch_on_clicked(self):
        """
        :purpose: calls fetch method and adds ticket sections
        :return: None
        :author(s): Joe Lee
        """
        self.remove_ticket_section()
        tickets = self.fetch("OPEN")
        if not tickets:
            self.status_label.setText(f"No tickets found for Status: OPEN")
        else:
            for ticket in tickets:
                self.add_ticket_section()

    def fetch(self, status_value):
        """
        :purpose: fetches all tickets with status from Consignments container
        :return: list of tickets
        :author(s): Joe Lee
        """
        try:
            container = self.db_connection.connect("Consignments")

            query = """
            SELECT c.ticket_number, c.datetime, c.vendor_id
            FROM c
            WHERE c.type = 'consignment'
            ORDER BY c.ticket_number ASC
            """

            results = list(container.query_items(
                query=query,
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
        self.update_btn.clicked.connect(self.fetch_on_clicked)
        # self.view_btn.clicked.connect()
        # self.excel_btn.clicked.connect()
        # self.pdf_btn.clicked.connect()
        # self.print_btn.clicked.connect()