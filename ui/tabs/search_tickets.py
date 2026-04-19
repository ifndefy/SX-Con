from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QIntValidator
from PyQt6.QtWidgets import QVBoxLayout, QComboBox
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

class SearchTicketsTab(BaseTab):
    def __init__(self, api_handler, db_connection):
        self.tickets_section = []
        self.db_connection = db_connection
        super().__init__(api_handler, "search_tickets")

        self.search_timer = QTimer()
        self.search_timer.setSingleShot(True)
        self.search_timer.timeout.connect(self.build_and_search)

    def setup_ui(self):
        """
        :purpose: initializes the "Create New Record" tab
        :return: None
        :author(s): Joe Lee
        """
        background = QVBoxLayout(self)

        main_layout_widget = QWidget()
        main_layout = QVBoxLayout(main_layout_widget)
        # main_layout_widget.setObjectName("main_layout")

        header_section = QHBoxLayout()
        title = QLabel("Open Tickets")
        title.setObjectName("post_title")
        header_section.addWidget(title)
        header_section.addStretch()
        main_layout.addLayout(header_section)

        hr1 = QFrame()
        hr1.setFrameShape(QFrame.Shape.HLine)
        hr1.setFrameShadow(QFrame.Shadow.Sunken)
        hr1.setObjectName("hr")
        main_layout.addWidget(hr1)

        search_section_row_1 = QHBoxLayout()
        search_section_row_1.addWidget(QLabel("Ticket Number:"))
        self.ticket_number_input = QLineEdit()
        self.ticket_number_input.setPlaceholderText("T Num")
        self.ticket_number_input.setFixedWidth(100)
        self.ticket_number_input.setValidator(QIntValidator(0, 2147483647, self))
        self.ticket_number_input.textChanged.connect(self.on_search_input_changed)
        search_section_row_1.addWidget(self.ticket_number_input)

        search_section_row_1.addWidget(QLabel("Datetime:"))
        self.datetime_input = QLineEdit()
        self.datetime_input.setPlaceholderText("Datetime")
        self.datetime_input.setMaxLength(30)
        self.datetime_input.setFixedWidth(195)
        self.datetime_input.textChanged.connect(self.on_search_input_changed)
        search_section_row_1.addWidget(self.datetime_input)

        search_section_row_1.addWidget(QLabel("Status:"))
        self.status_input = QComboBox()
        self.status_input.addItems(['OPEN', 'CLOSED'])
        self.status_input.setCurrentIndex(-1)
        self.status_input.setFixedWidth(75)
        self.status_input.currentTextChanged.connect(self.on_search_input_changed)
        search_section_row_1.addWidget(self.status_input)

        search_section_row_1.addStretch()

        main_layout.addLayout(search_section_row_1)

        search_section_row_2 = QHBoxLayout()
        self.clear_btn = QPushButton("Clear")
        self.clear_btn.setFixedWidth(200)
        search_section_row_2.addWidget(self.clear_btn)

        search_section_row_2.addStretch()
        self.search_btn = QPushButton("Search")
        self.search_btn.setFixedWidth(200)
        search_section_row_2.addWidget(self.search_btn)
        main_layout.addLayout(search_section_row_2)

        hr2 = QFrame()
        hr2.setFrameShape(QFrame.Shape.HLine)
        hr2.setFrameShadow(QFrame.Shadow.Sunken)
        hr2.setObjectName("hr")
        main_layout.addWidget(hr2)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)

        self.tickets_layout = QVBoxLayout()
        scroll_layout.addLayout(self.tickets_layout)
        scroll_layout.addStretch()

        scroll.setWidget(scroll_content)
        main_layout.addWidget(scroll)
        background.addWidget(main_layout_widget)
        self.setup_button_connections()

    def clear(self):
        """
        :purpose: clears all input fields and fetched items
        :author(s): Joe Lee
        """
        self.search_timer.stop()
        self.remove_ticket_section()
        fields = [
            self.ticket_number_input,
            self.datetime_input,
        ]
        for field in fields:
            field.blockSignals(True)
            field.clear()
            field.setReadOnly(False)
            field.setObjectName("DEFAULT")
            field.blockSignals(False)
            field.style().unpolish(field)
            field.style().polish(field)

        self.status_input.blockSignals(True)
        self.status_input.setCurrentIndex(-1)
        self.status_input.blockSignals(False)

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
        self.remove_ticket_section()

        conditions = ["c.entity_type = 'consignment'"]
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

        ticket_number = self.ticket_number_input.text().strip()
        if ticket_number:
            ticket_number_int = int(ticket_number)
            add_property("consignment_id", ticket_number_int, "=")

        status = self.status_input.currentText().strip()
        if status:
            add_property("status", status, "CONTAINS")

        datetime = self.datetime_input.text().strip()
        if datetime:
            add_property("datetime", datetime, "CONTAINS")

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
        self.remove_ticket_section()
        try:
            container = self.db_connection.connect("Consignments")
            results = list(container.query_items(
                query=query,
                parameters=properties if properties else [],
                enable_cross_partition_query=True
            ))

            tickets = []
            for item in results:
                tickets.append({
                    'ticket_number': item.get('consignment_id'),
                    'vendor_id': item.get('vendor_id', ''),
                    'products': item.get('products', []),
                    'datetime': item.get('datetime', ''),
                    'status': item.get('status', ''),
                })

            tickets.sort(key=lambda t: int(t['ticket_number']), reverse=True)

            for ticket in tickets:
                self.add_ticket_section()
                last_section = self.tickets_section[-1]
                last_section['ticket_num'].setText(str(ticket['ticket_number']))
                last_section['datetime'].setText(str(ticket['datetime']))
                last_section['status'].setText(ticket['status'])
                if last_section['status'].text().strip() == "CLOSED":
                    last_section['close_btn'].hide()
                if last_section['status'].text().strip() == "OPEN":
                    last_section['open_btn'].hide()

            if not tickets:
                status_bar_instance.send_message("No tickets found")
            else:
                status_bar_instance.send_message(f"Found {len(tickets)} ticket(s)")

        except Exception as e:
            log.error(f"Error executing query: {e}")
            status_bar_instance.send_message("Query failed")

    def fetch(self):
        """
        :purpose: fetches all tickets from Consignments container
        :return: list of users
        :author(s): Joe Lee
        """
        get_all_query = "SELECT * FROM c WHERE c.entity_type = 'consignment'"
        self.query_db(get_all_query)

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
        ticket_number_input.setReadOnly(True)
        ticket_number_input.setFixedWidth(100)
        line1_layout.addWidget(ticket_number_input)
        tickets_section['ticket_num'] = ticket_number_input

        # datetime
        line1_layout.addWidget(QLabel("Datetime:"))
        datetime_input = QLineEdit()
        datetime_input.setObjectName("READ_ONLY")
        datetime_input.setReadOnly(True)
        datetime_input.setFixedWidth(195)
        line1_layout.addWidget(datetime_input)
        tickets_section['datetime'] = datetime_input

        # status
        line1_layout.addWidget(QLabel("Status:"))
        status_input = QLineEdit()
        status_input.setObjectName("READ_ONLY")
        status_input.setReadOnly(True)
        status_input.setFixedWidth(75)
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
        """
        :Purpose: Instance Handler
        :Author(s): Joe Lee
        """
        def handler():
            """
            :Purpose: Handles the open and close button via a sequence of events
            :Author(s): Joe Lee
            """
            try:
                ticket_number = self.tickets_section[ticket_index]['ticket_num'].text().strip()

                def restyle(widget, obj_name):
                    widget.setObjectName(obj_name)
                    widget.style().unpolish(widget)
                    widget.style().polish(widget)

                if action == "open":
                    handler_open_close_btns(ticket_number, action.upper())
                    log.info(f"OPENED ticket {ticket_number}")
                    self.tickets_section[ticket_index]['status'].setText("OPEN")
                    self.tickets_section[ticket_index]['open_btn'].hide()
                    self.tickets_section[ticket_index]['close_btn'].show()
                    view_ticket = self.tickets_section[ticket_index].get('view_ticket')
                    if view_ticket:
                        view_ticket.payout_widget.calc_btn.setEnabled(True)
                        view_ticket.payout_widget.calc_btn.setText("Calculate")
                        restyle(view_ticket.payout_widget.calc_btn, 'DEFAULT')
                        view_ticket.payout_widget.payout_btn.setEnabled(True)
                        view_ticket.payout_widget.payout_btn.setText("Payout")
                        restyle(view_ticket.payout_widget.payout_btn, 'DEFAULT')
                        for widgets in view_ticket.product_widgets.values():
                            widgets['sold_edit'].setReadOnly(False)
                            restyle(widgets['sold_edit'], "DEFAULT")
                            widgets['update_btn'].setEnabled(True)
                            restyle(widgets['update_btn'], "DEFAULT")
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
                        view_ticket.payout_widget.calc_btn.setText("TICKET CLOSED")
                        restyle(view_ticket.payout_widget.calc_btn, 'LOCKED')
                        view_ticket.payout_widget.payout_btn.setEnabled(False)
                        view_ticket.payout_widget.payout_btn.setText("TICKET CLOSED")
                        restyle(view_ticket.payout_widget.payout_btn, 'LOCKED')
                        for widgets in view_ticket.product_widgets.values():
                            widgets['sold_edit'].setReadOnly(True)
                            restyle(widgets['sold_edit'], "LOCKED")
                            widgets['update_btn'].setEnabled(False)
                            restyle(widgets['update_btn'], "LOCKED")
                    QMessageBox.information(self, "Ticket Closed", f"Ticket {ticket_number} has been closed")
                self.tickets_section[ticket_index]['status'].setText(
                    get_property("Consignments", "status", "consignment", ticket_number)
                )
                self.parent().setFocus()
            except Exception as e:
                log.error(f"Could not {action} ticket {ticket_number}: {e}")

        return handler

    def make_print_handler(self, ticket_number_input):
        """
        :Purpose: Instance Handler
        :Author(s): Joe Lee
        """
        def handler():
            """
            :Purpose: Handles the print sequence
            :Author(s): Joe Lee
            """
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
        ''' 
        :purpose: Defines function closure for the current ticket to gather data from the fields to fill an excel table
        
        :return: Function reference for the specific ticket.
        :author: Maksym Komarov
        '''
        def gather_ticket():
            ''' 
            :purpose: Gathers data to fill an excel table
            
            :return: Dictionary containing data to export to excel.
            :author: Maksym Komarov
            '''
            ticket = self.tickets_section[ticket_index]
            ticket_number = ticket['ticket_num'].text().strip()
            ticket_details = self.view(ticket_number)
            unpacked_ticket = ticket_details['ticket_data']

            ticket_header = {
                'ticket_number': unpacked_ticket['consignment_id'],
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
        """
        :Purpose: Instance Handler
        :Author(s): Joe Lee
        """
        def handler():
            """
            :Purpose: Handles the PDF generation
            :Author(s): Joe Lee
            """
            ticket_number = int(ticket_number_input.text().strip())
            self.handle_pdf_btn_clicked(ticket_number)
        return handler

    def handle_pdf_btn_clicked(self, ticket_number):
        """
        :Purpose: Handles the PDF generation
        :Author(s): Joe Lee
        """
        try:
            handler_db_pdf(ticket_number)
            log.info(f"PDF generated for ticket {ticket_number}")
            QMessageBox.information(self, "PDF Generation Succeeded", f"Ticket {ticket_number} successfully generated a PDF")
        except Exception as e:
            log.error(f"ERROR generating PDF for ticket {ticket_number}: {e}")
            QMessageBox.information(self, "PDF Generation Failed", f"Ticket {ticket_number} failed to generate a PDF")

    def make_view_handler(self, ticket_index):
        """
        :Purpose: Instance Handler
        :Author(s): Joe Lee
        """
        def handler():
            """
            :Purpose: Handles the view generation
            :Author(s): Joe Lee
            """
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

    def on_view_clicked(self, ticket_index):
        """
        :Purpose: Handles view button via a sequence of events
        :Author(s): Joe Lee
        """
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


    def setup_button_connections(self):
        """
        :purpose: links buttons with methods
        :return: None
        :author(s): Joe Lee
        """
        self.clear_btn.clicked.connect(self.clear)
        self.search_btn.clicked.connect(self.build_and_search)
