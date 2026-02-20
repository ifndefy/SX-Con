from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtWidgets import QHBoxLayout
from PyQt6.QtWidgets import QLabel
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtWidgets import QScrollArea
from PyQt6.QtWidgets import QWidget

from handlers.handler_pdf import handler_db_pdf
from ui.core.view_ticket import ViewTicket
from ui.tabs.base import BaseTab
import utils.logger.logger as log
from services.message_bus import status_bar_instance
from ui.core import excel
from utils.core import generate_excel as xls_gen

class OpenTicketsTab(BaseTab):
    def __init__(self, api_handler, db_connection):
        self.ticket_counter = None
        self.tickets_layout = None
        self.tickets_section = []
        self.db_connection = db_connection

        super().__init__(api_handler, "open_tickets")

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

        # Set up the scroll area
        scroll.setWidget(scroll_content)
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(scroll)

        self.setup_button_connections()

    def add_ticket_section(self, ticket_data=None):
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
        ticket_number_input = QLineEdit()
        ticket_number_input.setObjectName("READ_ONLY")
        ticket_number_input.setPlaceholderText("XXXX")
        ticket_number_input.setReadOnly(True)
        ticket_number_input.setFixedWidth(80)

        # Set ticket number if provided
        if ticket_data:
            ticket_number_input.setText(str(ticket_data.get('ticket_number', '')))

        line1_layout.addWidget(ticket_number_input)
        tickets_section['ticket_num'] = ticket_number_input

        # datetime
        line1_layout.addWidget(QLabel("Date and Time:"))
        datetime_input = QLineEdit()
        datetime_input.setObjectName("READ_ONLY")
        datetime_input.setReadOnly(True)
        datetime_input.setFixedWidth(175)

        # Set datetime if provided
        if ticket_data:
            datetime_input.setText(str(ticket_data.get('datetime', '')))

        line1_layout.addWidget(datetime_input)
        tickets_section['datetime'] = datetime_input

        # status
        line1_layout.addWidget(QLabel("Status:"))
        status_input = QLineEdit()
        status_input.setObjectName("READ_ONLY")
        status_input.setPlaceholderText("OPEN")
        status_input.setReadOnly(True)
        status_input.setFixedWidth(70)

        # Set status if provided
        if ticket_data:
            status_input.setText(str(ticket_data.get('status', '')))

        line1_layout.addWidget(status_input)
        tickets_section['status'] = status_input

        line1_layout.addStretch()

        # btns
        view_btn = QPushButton("View")
        line1_layout.addWidget(view_btn)
        tickets_section['view_btn'] = view_btn

        #Create excel button without gather function link once index is assigned
        excel_btn = excel.ExcelButton(None, xls_gen.generate_excel, "Excel")
        line1_layout.addWidget(excel_btn)
        tickets_section['excel_btn'] = excel_btn

        pdf_btn = QPushButton("PDF")
        line1_layout.addWidget(pdf_btn)
        tickets_section['pdf_btn'] = pdf_btn

        print_btn = QPushButton("Print")
        line1_layout.addWidget(print_btn)
        tickets_section['print_btn'] = print_btn

        section_layout.addLayout(line1_layout)

        # Create details container (initially hidden)
        details_container = QWidget()
        details_container.setObjectName("view_bg")
        details_container.setVisible(False)
        details_layout = QVBoxLayout(details_container)
        details_layout.setContentsMargins(20, 10, 10, 10)

        product_details_layout = QVBoxLayout()
        tickets_section['product_details_layout'] = product_details_layout
        details_layout.addLayout(product_details_layout)

        section_layout.addWidget(details_container)
        tickets_section['details_container'] = details_container

        # Add to container
        self.tickets_layout.addWidget(section_widget)

        # Store the index
        ticket_index = len(self.tickets_section)
        tickets_section['index'] = ticket_index

        # Connect the view button
        view_btn.clicked.connect(self.make_view_handler(ticket_index))
        pdf_btn.clicked.connect(self.make_pdf_handler(ticket_number_input.text()))
        excel_btn.link_gather_function(self.make_form_handler(ticket_index))

        self.tickets_section.append(tickets_section)

    def make_form_handler(self, ticket_index):
        def gather_ticket():
            ticket = self.tickets_section[ticket_index]
            ticket_number = ticket['ticket_num'].text().strip()
            ticket_details = self.view(ticket_number)
            unpacked_ticket = ticket_details['ticket_data']

            ticket_header = {
                'ticket_number': unpacked_ticket['ticket_number'],
                'vendor_id': unpacked_ticket['vendor_id'],
                'created': unpacked_ticket['datetime'],
                'status': unpacked_ticket['status'],
            }

            return {
                'ticket_info': ticket_header,
                'product_data': unpacked_ticket['price_data']['products'],
                'revenue_sharing': unpacked_ticket['revenue_sharing']
            }

        return gather_ticket

    def make_pdf_handler(self, ticket_number):
        def handler():
            self.handle_pdf_btn_clicked(int(ticket_number))
        return handler

    def handle_pdf_btn_clicked(self, ticket_number):
        try:
            handler_db_pdf(ticket_number)
            log.info(f"PDF generated for ticket {ticket_number}")
        except Exception as e:
            log.error(f"ERROR generating PDF for ticket {ticket_number}: {e}")

    def make_view_handler(self, ticket_index):
        def handler():
            self.on_view_clicked(ticket_index)
        return handler

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

    def setup_button_connections(self):
        """
        :purpose: links buttons with methods
        :return: None
        :author(s): Joe Lee
        """
        self.update_btn.clicked.connect(self.fetch_on_clicked)

    def fetch_on_clicked(self):
        """
        :purpose: calls fetch method and adds ticket sections
        :return: None
        :author(s): Joe Lee
        """
        self.remove_ticket_section()
        tickets = self.fetch("OPEN")
        if not tickets:
            log.warning(f"No tickets found for Status: OPEN")
        else:
            for ticket in tickets:
                self.add_ticket_section(ticket)  # Pass ticket data to populate fields

    def fetch(self, status):
        try:
            container = self.db_connection.connect("Consignments")

            query = """
                    SELECT c.ticket_number, c.datetime, c.status
                    FROM c
                    WHERE c.type = 'consignment'
                      AND c.status = @status
                    ORDER BY c.ticket_number DESC
                    """

            parameters = [{"name": "@status", "value": status}]

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
                    'status': item.get('status', 'UNKNOWN')
                })

            return tickets

        except Exception as e:
            log.error(f"Error fetching tickets: {e}")
            return []

    def on_view_clicked(self, ticket_index):
        try:
            ticket_section = self.tickets_section[ticket_index]
            ticket_number = ticket_section['ticket_num'].text().strip()

            if not ticket_number:
                log.error("No ticket number available")
                return

            details_container = ticket_section['details_container']
            is_visible = details_container.isVisible()

            if not is_visible:
                ticket_details = self.view(ticket_number)
                if ticket_details:
                    self.view_ticket_details(ticket_section, ticket_details)
                    details_container.setVisible(True)
                    ticket_section['view_btn'].setText("Hide")
                    log.info(f"Displaying details for ticket {ticket_number}")
                else:
                    log.error(f"No details found for ticket {ticket_number}")
            else:
                details_container.setVisible(False)
                ticket_section['view_btn'].setText("View")
                log.info(f"Hidden details for ticket {ticket_number}")

        except Exception as e:
            log.error(f"Error in on_view_clicked: {e}")

    def view(self, ticket_number):
        try:
            consignments_container = self.db_connection.connect("Consignments")

            query = "SELECT * FROM c WHERE c.ticket_number = @ticket_number"

            parameters = [
                {"name": "@ticket_number", "value": int(ticket_number)}
            ]

            ticket_results = list(consignments_container.query_items(
                query=query,
                parameters=parameters,
                enable_cross_partition_query=True
            ))

            if not ticket_results:
                return None

            ticket_data = ticket_results[0]

            product_ids = ticket_data.get('product_ids', [])
            products = []

            if product_ids:
                entities_container = self.db_connection.connect("Entities")

                for product_id in product_ids:
                    product_query = "SELECT * FROM c WHERE c.id = @product_id AND c.type = 'product'"

                    product_parameters = [
                        {"name": "@product_id", "value": product_id}
                    ]

                    product_results = list(entities_container.query_items(
                        query=product_query,
                        parameters=product_parameters,
                        enable_cross_partition_query=True
                    ))

                    if product_results:
                        product_data = product_results[0]
                        products.append({
                            'product_id': product_id,
                            'product_name': product_data.get('product_name', 'N/A'),
                            'description': product_data.get('description', ''),
                            'price': product_data.get('price', 0),
                            'quantity': product_data.get('quantity', 0)
                        })

            return {
                'ticket_data': ticket_data,
                'products': products
            }

        except Exception as e:
            log.error(f"Error fetching ticket details: {e}")
            return None

    def view_ticket_details(self, ticket_section, ticket_details):
        ViewTicket.view_ticket_details(ticket_section, ticket_details)