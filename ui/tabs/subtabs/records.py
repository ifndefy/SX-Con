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

class RecordsTab(BaseTab):
    def __init__(self, api_handler, db_connection):
        self.records_section = []
        self.db_connection = db_connection
        super().__init__(api_handler, "records")

    def setup_ui(self):
        """
        :purpose: initializes the "Record" subtab
        :author(s): Joe Lee
        """
        # Enable scrolling for when the content exceeds the height of the window
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        layout = QVBoxLayout(scroll_content)

        # Line 0 Creation
        header_section = QHBoxLayout()

        # Record Header
        title = QLabel("View Records")
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
        self.records_layout = QVBoxLayout()

        layout.addLayout(self.records_layout)

        records_section = QHBoxLayout()

        layout.addLayout(records_section)
        layout.addStretch()

        record_section_row_3 = QHBoxLayout()
        self.update_btn = QPushButton("Update")
        record_section_row_3.addWidget(self.update_btn)
        layout.addLayout(record_section_row_3)

        # HR Line to separate buttons at the bottom
        hr3 = QLabel()
        hr3.setObjectName("hr")
        layout.addWidget(hr3)

        # Set up the scroll area
        scroll.setWidget(scroll_content)
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(scroll)

        self.setup_button_connections()

    def add_ticket_section(self, rec_data):
        """
        :purpose: adds record lines
        :return: None
        :author(s): Joe Lee
        """
        rec_section = {}

        # Record section container
        section_widget = QWidget()
        section_layout = QVBoxLayout(section_widget)
        section_layout.setContentsMargins(0, 0, 0, 0)

        # Line 1: ticket_num + datetime + status + buttons
        line1_layout = QHBoxLayout()

        # ticket_num
        line1_layout.addWidget(QLabel("Ticket Number:"))
        ticket_num_input = QLineEdit()
        ticket_num_input.setText(str(rec_data['ticket_number']))
        ticket_num_input.setObjectName("READ_ONLY")
        ticket_num_input.setReadOnly(True)
        ticket_num_input.setMaxLength(6)
        ticket_num_input.setFixedWidth(80)
        line1_layout.addWidget(ticket_num_input)

        # datetime
        line1_layout.addWidget(QLabel("DateTime:"))
        datetime_input = QLineEdit()
        datetime_input.setText(str(rec_data['datetime']))
        datetime_input.setObjectName("READ_ONLY")
        datetime_input.setReadOnly(True)
        datetime_input.setFixedWidth(165)
        line1_layout.addWidget(datetime_input)

        # status
        line1_layout.addWidget(QLabel("Status:"))
        status_input = QLineEdit()
        status_input.setText(str(rec_data['status']))
        status_input.setObjectName("READ_ONLY")
        status_input.setReadOnly(True)
        status_input.setFixedWidth(55)
        line1_layout.addWidget(status_input)

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
        self.edit_btn = QPushButton("Edit")
        self.edit_btn.setObjectName("red_btn")
        line1_layout.addWidget(self.edit_btn)
        self.close_btn = QPushButton("Close")
        self.close_btn.setObjectName("red_btn")
        line1_layout.addWidget(self.close_btn)

        section_layout.addLayout(line1_layout)

        # Add to container
        self.records_layout.addWidget(section_widget)
        self.records_section.append(rec_section)

    def remove_record_section(self):
        """
        :purpose: removes and clears all ticket sections
        :return: None
        :author(s): Joe Lee
        """
        # Remove all widgets from the layout
        for i in reversed(range(self.records_layout.count())):
            widget = self.records_layout.itemAt(i).widget()
            if widget:
                self.records_layout.removeWidget(widget)
                widget.deleteLater()

        # Clear the tickets_section list
        self.records_section.clear()

        # Update status
        status_bar_instance.send_message("All tickets cleared")

    def fetch_on_clicked(self):
        """
        :purpose: calls fetch method and adds ticket sections
        :return: None
        :author(s): Joe Lee
        """
        self.remove_record_section()
        records = self.fetch()
        if not records:
            log.error("No records found")
        else:
            for record in records:
                self.add_ticket_section(record)

    def fetch(self):
        """
        :purpose: fetches all consignments from Consignments container
        :return: list of tickets
        :author(s): Joe Lee
        """
        try:
            container = self.db_connection.connect("Consignments")

            query = """
            SELECT *
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
                    'ticket_number': item.get('ticket_number', ''),
                    'datetime': item.get("datetime", ""),
                    'status': item.get("status", ""),
                    'vendor_id': item.get("vendor_id", ""),
                })
            return tickets

        except Exception as e:
            log.error(f"Error fetching tickets: {e}")
            return []

    def setup_button_connections(self):
        """
        :purpose: links buttons with methods
        :return: None
        :author(s): Joe Lee
        """
        self.update_btn.clicked.connect(self.fetch_on_clicked)