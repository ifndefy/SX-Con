from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtWidgets import QFrame
from PyQt6.QtWidgets import QHBoxLayout
from PyQt6.QtWidgets import QLabel
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtWidgets import QScrollArea
from PyQt6.QtWidgets import QWidget

from ui.tabs.base import BaseTab

from handlers.handler_open_close import handler_open_close_btns
from handlers.handler_print import handler_print
from handlers.handler_pdf import handler_db_pdf
from services.get_item import get_item
from services.get_property import get_property
from ui.core import excel_button
from ui.core.view_ticket import ViewTicket
from utils.core import generate_excel as xls_gen

import utils.logger.logger as log
from utils.message_bus import status_bar_instance

class OpenTicketsTab(BaseTab):
    def __init__(self, api_handler, db_connection):
        self.ticket_counter = None
        self.tickets_layout = None
        self.ticket_status = None
        self.tickets_section = []
        self.db_connection = db_connection

        super().__init__(api_handler, "open_tickets")

    def setup_ui(self):
        """
        :purpose: initializes the "Create New Record" tab
        :return: None
        :author(s): Joe Lee
        """
        background = QVBoxLayout(self)

        main_layout_widget = QWidget()
        main_layout_widget.setObjectName("main_layout")
        main_layout = QVBoxLayout(main_layout_widget)


        # Line 0 Creation
        header_section = QHBoxLayout()

        # Ticket Header
        title = QLabel("Open Tickets")
        title.setObjectName("post_title")
        header_section.addWidget(title)

        # Push to the left
        header_section.addStretch()

        # Ends creation and adds header_section to window
        main_layout.addLayout(header_section)

        # HR Line between Vendor and Tickets sections
        hr1 = QFrame()
        hr1.setFrameShape(QFrame.Shape.HLine)
        hr1.setFrameShadow(QFrame.Shadow.Sunken)
        hr1.setObjectName("hr")
        main_layout.addWidget(hr1)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)

        # Ticket Line 1: Tickets sections container
        self.tickets_layout = QVBoxLayout()
        scroll_layout.addLayout(self.tickets_layout)

        scroll_layout.addStretch()
        scroll.setWidget(scroll_content)
        main_layout.addWidget(scroll)

        # HR Line to separate buttons at the bottom
        hr2 = QFrame()
        hr2.setFrameShape(QFrame.Shape.HLine)
        hr2.setFrameShadow(QFrame.Shadow.Sunken)
        hr2.setObjectName("hr")
        main_layout.addWidget(hr2)

        # Set up update button separate from the scrollable area
        self.update_btn = QPushButton("Update")
        main_layout.addWidget(self.update_btn)
        background.addWidget(main_layout_widget)
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
        line1_layout.addWidget(ticket_number_input)
        tickets_section['ticket_num'] = ticket_number_input

        # datetime
        line1_layout.addWidget(QLabel("Date and Time:"))
        datetime_input = QLineEdit()
        datetime_input.setObjectName("READ_ONLY")
        datetime_input.setReadOnly(True)
        datetime_input.setFixedWidth(175)
        line1_layout.addWidget(datetime_input)
        tickets_section['datetime'] = datetime_input

        # status
        line1_layout.addWidget(QLabel("Status:"))
        status_input = QLineEdit()
        status_input.setObjectName("READ_ONLY")
        status_input.setPlaceholderText("OPEN")
        status_input.setReadOnly(True)
        status_input.setFixedWidth(70)
        line1_layout.addWidget(status_input)
        tickets_section['status'] = status_input

        line1_layout.addStretch()

        # btns
        view_btn = QPushButton("View")
        line1_layout.addWidget(view_btn)
        tickets_section['view_btn'] = view_btn

        #Create excel button without gather function link once index is assigned
        excel_btn = excel_button.ExcelButton(None, xls_gen.generate_excel, "Excel")
        line1_layout.addWidget(excel_btn)
        tickets_section['excel_btn'] = excel_btn

        pdf_btn = QPushButton("PDF")
        line1_layout.addWidget(pdf_btn)
        tickets_section['pdf_btn'] = pdf_btn

        print_btn = QPushButton("Print")
        line1_layout.addWidget(print_btn)
        tickets_section['print_btn'] = print_btn

        close_btn = QPushButton("Close")
        close_btn.setObjectName("red_btn")
        close_btn.setFixedWidth(68)
        line1_layout.addWidget(close_btn)
        tickets_section['close_btn'] = close_btn

        open_btn = QPushButton("Open")
        open_btn.setObjectName("green_btn")
        open_btn.setFixedWidth(68)
        line1_layout.addWidget(open_btn)
        tickets_section['open_btn'] = open_btn

        section_layout.addLayout(line1_layout)

        # Create details container (initially hidden)
        details_container = QWidget()
        details_container.setObjectName("view_bg")
        details_container.setVisible(False)
        details_layout = QVBoxLayout(details_container)
        details_layout.setContentsMargins(10, 10, 10, 10)

        product_details_layout = QVBoxLayout()
        tickets_section['product_details_layout'] = product_details_layout
        details_layout.addLayout(product_details_layout)
        section_layout.addWidget(details_container)
        tickets_section['details_container'] = details_container

        hr = QFrame()
        hr.setFrameShape(QFrame.Shape.HLine)
        hr.setFrameShadow(QFrame.Shadow.Sunken)
        hr.setObjectName("hr")
        section_layout.addWidget(hr)

        # Add to container
        self.tickets_layout.addWidget(section_widget)

        # Store the index
        ticket_index = len(self.tickets_section)
        tickets_section['index'] = ticket_index

        # Connect the view button
        view_btn.clicked.connect(self.make_view_handler(ticket_index))
        pdf_btn.clicked.connect(self.make_pdf_handler(ticket_number_input))
        excel_btn.link_gather_function(self.make_form_handler(ticket_index))
        print_btn.clicked.connect(self.make_print_handler(ticket_number_input))
        close_btn.clicked.connect(self.handle_open_close_btns(ticket_index, "closed"))
        open_btn.clicked.connect(self.handle_open_close_btns(ticket_index, "open"))

        self.tickets_section.append(tickets_section)

    def handle_open_close_btns(self, ticket_index, action):
        def handler():
            try:
                ticket_number = self.tickets_section[ticket_index]['ticket_num'].text().strip()
                if action == "open":
                    handler_open_close_btns(ticket_number, action.upper())
                    log.info(f"OPENED ticket {ticket_number}")
                    self.tickets_section[ticket_index]['status'].setText("OPEN")
                    self.tickets_section[ticket_index]['open_btn'].hide()
                    self.tickets_section[ticket_index]['close_btn'].show()
                    view_ticket = self.tickets_section[ticket_index].get('view_ticket')
                    if view_ticket:
                        view_ticket.payout_widget.calc_btn.setEnabled(True)
                        view_ticket.payout_widget.calc_btn.setObjectName('DEFAULT')
                        view_ticket.payout_widget.calc_btn.setText("Calculate Payout")
                        view_ticket.payout_widget.calc_btn.style().unpolish(view_ticket.payout_widget.calc_btn)
                        view_ticket.payout_widget.calc_btn.style().polish(view_ticket.payout_widget.calc_btn)
                        for widgets in view_ticket.product_widgets.values():
                            widgets['sold_edit'].setReadOnly(False)
                            widgets['sold_edit'].setObjectName("DEFAULT")
                            widgets['sold_edit'].style().unpolish(widgets['sold_edit'])
                            widgets['sold_edit'].style().polish(widgets['sold_edit'])
                            widgets['update_btn'].setEnabled(False)
                            widgets['update_btn'].setObjectName("DEFAULT")
                            widgets['update_btn'].style().unpolish(widgets['update_btn'])
                            widgets['update_btn'].style().polish(widgets['update_btn'])
                    QMessageBox.information(self, "Ticket Opened", f"Ticket {ticket_number} has been opened")
                elif action == "closed":
                    handler_open_close_btns(ticket_number, action.upper())
                    log.info(f"CLOSED ticket {ticket_number}")
                    self.tickets_section[ticket_index]['status'].setText("CLOSED")
                    self.tickets_section[ticket_index]['close_btn'].hide()
                    self.tickets_section[ticket_index]['open_btn'].show()
                    view_ticket = self.tickets_section[ticket_index].get('view_ticket')
                    if view_ticket:
                        view_ticket.payout_widget.calc_btn.setEnabled(False)
                        view_ticket.payout_widget.calc_btn.setObjectName('LOCKED')
                        view_ticket.payout_widget.calc_btn.setText("TICKET CLOSED")
                        view_ticket.payout_widget.calc_btn.style().unpolish(view_ticket.payout_widget.calc_btn)
                        view_ticket.payout_widget.calc_btn.style().polish(view_ticket.payout_widget.calc_btn)
                        for widgets in view_ticket.product_widgets.values():
                            widgets['sold_edit'].setReadOnly(True)
                            widgets['sold_edit'].setObjectName("LOCKED")
                            widgets['sold_edit'].style().unpolish(widgets['sold_edit'])
                            widgets['sold_edit'].style().polish(widgets['sold_edit'])
                            widgets['update_btn'].setEnabled(False)
                            widgets['update_btn'].setObjectName("LOCKED")
                            widgets['update_btn'].style().unpolish(widgets['update_btn'])
                            widgets['update_btn'].style().polish(widgets['update_btn'])
                    QMessageBox.information(self, "Ticket Closed", f"Ticket {ticket_number} has been closed")
                self.tickets_section[ticket_index]['status'].setText(
                    get_property("Consignments", "status", "consignment", ticket_number)
                )
                self.parent().setFocus()
            except Exception as e:
                log.error(f"Could not {action} ticket {ticket_number}: {e}")

        return handler

    def make_print_handler(self, ticket_number_input):
        def handler():
            ticket_number = ticket_number_input.text().strip()
            try:
                handler_db_pdf(int(ticket_number))
                QMessageBox.information(self, "PDF Generation Succeeded",
                                        f"Ticket {ticket_number} successfully requested to print")
            except Exception as e:
                log.error(f"Could not generate PDF for ticket {ticket_number}: {e}")
                return

            try:
                handler_print(ticket_number)
                log.info(f"Print requested for ticket {ticket_number}")
            except Exception as e:
                QMessageBox.critical(self, "Print Failed", f"Failed to print ticket {ticket_number}:\n\n{e}")
        return handler

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
                'product_data': unpacked_ticket['products'],
                'revenue_shared': unpacked_ticket['revenue']['shared'],
                'revenue_grouped': unpacked_ticket['revenue']['grouped'],
                'revenue_payout': unpacked_ticket['revenue']['payout'],
            }

        return gather_ticket

    def make_pdf_handler(self, ticket_number_input):
        def handler():
            ticket_number = int(ticket_number_input.text().strip())
            self.handle_pdf_btn_clicked(ticket_number)
        return handler

    def handle_pdf_btn_clicked(self, ticket_number):
        try:
            handler_db_pdf(ticket_number)
            log.info(f"PDF generated for ticket {ticket_number}")
            QMessageBox.information(self, "PDF Generation Succeeded", f"Ticket {ticket_number} successfully generated a PDF")
        except Exception as e:
            log.error(f"ERROR generating PDF for ticket {ticket_number}: {e}")
            QMessageBox.information(self, "PDF Generation Failed", f"Ticket {ticket_number} failed to generate a PDF")

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
        self.update_btn.clicked.connect(self.on_fetch_clicked)

    def on_fetch_clicked(self):
        """
        :purpose: calls fetch method and adds ticket sections
        :return: None
        :author(s): Joe Lee
        """
        self.remove_ticket_section()
        tickets = self.fetch("OPEN")
        if not tickets:
            log.warning(f"No tickets found with Status: OPEN")
        else:
            for ticket in tickets:
                self.add_ticket_section()  # Pass ticket data to populate fields
                last_section = self.tickets_section[-1]
                last_section['ticket_num'].setText(str(ticket['ticket_number']))
                last_section['datetime'].setText(str(ticket['datetime']))
                last_section['status'].setText(ticket['status'])
                if last_section['status'].text().strip() == "CLOSED":
                    self.ticket_status = "CLOSED"
                    last_section['close_btn'].hide()
                if last_section['status'].text().strip() == "OPEN":
                    self.ticket_status = "OPEN"
                    last_section['open_btn'].hide()

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
                log.warning("No ticket number available")
                return

            details_container = ticket_section['details_container']
            is_visible = details_container.isVisible()

            if not is_visible:
                ticket_details = self.view(ticket_number)
                if ticket_details:
                    ticket_data = ticket_details['ticket_data']
                    ticket_num_val = ticket_data.get('id', '')
                    if ticket_num_val and '_' in ticket_num_val:
                        numeric_id = ticket_num_val.split('_', 1)[-1]
                    else:
                        numeric_id = ticket_num_val

                    view_ticket = ViewTicket(numeric_id)
                    view_ticket.setup_ui(ticket_section, ticket_details)

                    ticket_section['view_ticket'] = view_ticket

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
        """
        :Purpose: pulls a consignment's data from the db and maps it for display
        :Param: ticket_number - the ticket number
        :Returns: ticket data
        :Author(s): Joe Lee
        """
        try:
            consignment_data = get_item("Consignments", "consignment", ticket_number)
            if consignment_data is None:
                log.error(f"Consignment with ticket number {ticket_number} not found.")
                return None

            product_ids = consignment_data.get('product_ids', [])
            products = []
            for product_id in product_ids:
                product_data = get_item("Entities", "product", product_id)
                if product_data:
                    products.append({
                        'product_id': product_id,
                        'product_name': product_data.get('product_name', 'N/A'),
                        'description': product_data.get('description', ''),
                        'price': product_data.get('price', 0),
                        'quantity': product_data.get('quantity', 0)
                    })
                else:
                    log.warning(f"Product {product_id} not found in Entities.")

            return {
                'ticket_data': consignment_data,
                'products': products
            }

        except Exception as e:
            log.error(f"Error fetching ticket details: {e}")
            return None