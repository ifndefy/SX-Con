from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QIntValidator
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtWidgets import QFrame
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtWidgets import QHBoxLayout
from PyQt6.QtWidgets import QLabel
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtWidgets import QScrollArea
from PyQt6.QtWidgets import QWidget

from handlers.handler_open_close import handler_open_close_btns
from handlers.handler_pdf import handler_db_pdf
from handlers.handler_print import handler_print
from services.get_item import get_item
from services.get_property import get_property
from ui.core.view_ticket import ViewTicket
from ui.tabs.base import BaseTab

from ui.core import excel
from utils.core import generate_excel as xls_gen

import utils.logger.logger as log
from services.message_bus import status_bar_instance

class RecordsTab(BaseTab):
    def __init__(self, api_handler, db_connection):
        self.records_section = []
        self.db_connection = db_connection
        super().__init__(api_handler, "records")

        self.search_timer = QTimer()
        self.search_timer.setSingleShot(True)
        self.search_timer.timeout.connect(self.build_and_search)

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
        header_section.addStretch()

        # Ends creation and adds header_section to window
        layout.addLayout(header_section)

        # HR Line between Vendor and Tickets sections
        hr1 = QFrame()
        hr1.setFrameShape(QFrame.Shape.HLine)
        hr1.setFrameShadow(QFrame.Shadow.Sunken)
        hr1.setObjectName("hr")
        layout.addWidget(hr1)


        search_section_row_1 = QHBoxLayout()

        search_section_row_1.addWidget(QLabel("Ticket Number:"))
        self.ticket_number_input = QLineEdit()
        self.ticket_number_input.setPlaceholderText("T Num")
        self.ticket_number_input.setFixedWidth(73)
        self.ticket_number_input.setValidator(QIntValidator(0, 999999, self))
        self.ticket_number_input.textChanged.connect(self.on_search_input_changed)
        search_section_row_1.addWidget(self.ticket_number_input)


        search_section_row_1.addWidget(QLabel("Datetime:"))
        self.datetime_input = QLineEdit()
        self.datetime_input.setPlaceholderText("Datetime")
        self.datetime_input.setMaxLength(30)
        self.datetime_input.setFixedWidth(160)
        self.datetime_input.textChanged.connect(self.on_search_input_changed)
        search_section_row_1.addWidget(self.datetime_input)

        search_section_row_1.addWidget(QLabel("Status:"))
        self.status_input = QLineEdit()
        self.status_input.setPlaceholderText("Stat")
        self.status_input.setMaxLength(10)
        self.status_input.setFixedWidth(69)
        self.status_input.textChanged.connect(self.on_search_input_changed)
        search_section_row_1.addWidget(self.status_input)

        search_section_row_1.addStretch()
        layout.addLayout(search_section_row_1)

        search_section_row_2 = QHBoxLayout()

        search_section_row_2.addWidget(QLabel("Vendor ID:"))
        self.vendor_id_input = QLineEdit()
        self.vendor_id_input.setPlaceholderText("V ID")
        self.vendor_id_input.setFixedWidth(80)
        self.vendor_id_input.setValidator(QIntValidator(0, 9999, self))
        self.vendor_id_input.textChanged.connect(self.on_search_input_changed)
        search_section_row_2.addWidget(self.vendor_id_input)

        search_section_row_2.addWidget(QLabel("Product ID:"))
        self.product_id_input = QLineEdit()
        self.product_id_input.setPlaceholderText("P ID")
        self.product_id_input.setFixedWidth(80)
        self.product_id_input.setValidator(QIntValidator(0, 9999, self))
        self.product_id_input.textChanged.connect(self.on_search_input_changed)
        search_section_row_2.addWidget(self.product_id_input)

        search_section_row_2.addStretch()
        layout.addLayout(search_section_row_2)

        search_section_row_3 = QHBoxLayout()
        self.clear_btn = QPushButton("Clear")
        self.clear_btn.setFixedWidth(200)
        search_section_row_3.addWidget(self.clear_btn)

        search_section_row_3.addStretch()
        self.search_btn = QPushButton("Search")
        self.search_btn.setFixedWidth(200)
        search_section_row_3.addWidget(self.search_btn)
        layout.addLayout(search_section_row_3)

        hr2 = QFrame()
        hr2.setFrameShape(QFrame.Shape.HLine)
        hr2.setFrameShadow(QFrame.Shadow.Sunken)
        hr2.setObjectName("hr")
        layout.addWidget(hr2)

        # Ticket Line 1: Tickets sections container
        self.records_layout = QVBoxLayout()
        layout.addLayout(self.records_layout)

        records_section = QHBoxLayout()
        layout.addLayout(records_section)
        layout.addStretch()

        # Set up the scroll area
        scroll.setWidget(scroll_content)
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(scroll)

        self.setup_button_connections()

    def clear(self):
        """
        :purpose: clears all input fields and fetched items
        :author(s): Joe Lee
        """
        self.search_timer.stop()
        self.remove_record_section()
        fields = [
            self.ticket_number_input,
            self.vendor_id_input,
            self.product_id_input,
            self.datetime_input,
            self.status_input,
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
        self.remove_record_section()

        conditions = ["c.type = 'consignment'"]
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
            try:
                ticket_number_int = int(ticket_number)
                add_property("ticket_number", ticket_number_int, "=")
            except ValueError:
                pass

        vendor_id = self.vendor_id_input.text().strip()
        if vendor_id:
            try:
                vendor_id_int = int(vendor_id)
                add_property("vendor_id", vendor_id_int, "=")
            except ValueError:
                pass

        product_id = self.product_id_input.text().strip()
        if product_id: # this needs to iterate through a list todo:
            try:
                product_id_int = int(product_id)
                conditions.append("ARRAY_CONTAINS(c.product_ids, @product_id_int)")
                properties.append({"name": "@product_id_int", "value": product_id_int})
            except ValueError:
                pass

        datetime = self.datetime_input.text().strip()
        if datetime:
            add_property("datetime", datetime, "CONTAINS")

        status = self.status_input.text().strip()
        if status:
            add_property("status", status, "CONTAINS")

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
        self.remove_record_section()
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
                    'ticket_number': item.get('ticket_number'),
                    'vendor_id': item.get('vendor_id', ''),
                    'product_ids': item.get('product_ids', ''),
                    'datetime': item.get('datetime', ''),
                    'status': item.get('status', ''),
                })

            tickets.sort(key=lambda t: int(t['ticket_number']), reverse=True)

            for ticket in tickets:
                self.add_record_section()
                last_section = self.records_section[-1]
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
        get_all_query = "SELECT * FROM c WHERE c.type = 'consignment'"
        self.query_db(get_all_query)

    def add_record_section(self):
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
        ticket_num_input.setObjectName("READ_ONLY")
        ticket_num_input.setReadOnly(True)
        ticket_num_input.setMaxLength(6)
        ticket_num_input.setFixedWidth(73)
        line1_layout.addWidget(ticket_num_input)
        rec_section['ticket_num'] = ticket_num_input

        # datetime
        line1_layout.addWidget(QLabel("DateTime:"))
        datetime_input = QLineEdit()
        datetime_input.setObjectName("READ_ONLY")
        datetime_input.setReadOnly(True)
        datetime_input.setFixedWidth(160)
        line1_layout.addWidget(datetime_input)
        rec_section['datetime'] = datetime_input

        # status
        line1_layout.addWidget(QLabel("Status:"))
        status_input = QLineEdit()
        status_input.setObjectName("READ_ONLY")
        status_input.setReadOnly(True)
        status_input.setFixedWidth(69)
        line1_layout.addWidget(status_input)
        rec_section['status'] = status_input

        line1_layout.addStretch()

        # btns
        view_btn = QPushButton("View")
        line1_layout.addWidget(view_btn)
        rec_section['view_btn'] = view_btn

        #Create excel button without gather function link once index is assigned
        excel_btn = excel.ExcelButton(None, xls_gen.generate_excel, "Excel")
        line1_layout.addWidget(excel_btn)
        rec_section['excel_btn'] = excel_btn

        pdf_btn = QPushButton("PDF")
        line1_layout.addWidget(pdf_btn)
        rec_section['pdf_btn'] = pdf_btn

        print_btn = QPushButton("Print")
        line1_layout.addWidget(print_btn)
        rec_section['print_btn'] = print_btn

        edit_btn = QPushButton("Edit")
        line1_layout.addWidget(edit_btn)
        rec_section['edit_btn'] = edit_btn

        close_btn = QPushButton("Close")
        close_btn.setObjectName('red_btn')
        close_btn.setFixedWidth(68)
        line1_layout.addWidget(close_btn)
        rec_section['close_btn'] = close_btn

        open_btn = QPushButton("Open")
        open_btn.setObjectName('green_btn')
        open_btn.setFixedWidth(68)
        line1_layout.addWidget(open_btn)
        rec_section['open_btn'] = open_btn

        section_layout.addLayout(line1_layout)

        details_container = QWidget()
        details_container.setObjectName("view_bg")
        details_container.setVisible(False)
        details_layout = QVBoxLayout(details_container)
        details_layout.setContentsMargins(10, 10, 10, 10)

        product_details_layout = QVBoxLayout()
        rec_section['product_details_layout'] = product_details_layout
        details_layout.addLayout(product_details_layout)

        section_layout.addWidget(details_container)
        rec_section['details_container'] = details_container

        # Add to container
        self.records_layout.addWidget(section_widget)
        ticket_index = len(self.records_section)
        rec_section['index'] = ticket_index

        view_btn.clicked.connect(self.make_view_handler(ticket_index))
        pdf_btn.clicked.connect(self.make_pdf_handler(ticket_index))
        excel_btn.link_gather_function(self.make_form_handler(ticket_index))
        print_btn.clicked.connect(self.make_print_handler(ticket_index))
        close_btn.clicked.connect(self.handle_open_close_btns(ticket_index, "closed"))
        open_btn.clicked.connect(self.handle_open_close_btns(ticket_index, "open"))

        self.records_section.append(rec_section)

    def handle_open_close_btns(self, ticket_index, action):
        def handler():
            try:
                ticket_number = self.records_section[ticket_index]['ticket_num'].text().strip()
                self.parent().setFocus()
                if action == "open":
                    handler_open_close_btns(ticket_number, action.upper())
                    log.info(f"OPENED ticket {ticket_number}")
                    self.records_section[ticket_index]['status'].setText("OPEN")
                    self.records_section[ticket_index]['open_btn'].hide()
                    self.records_section[ticket_index]['close_btn'].show()
                elif action == "closed":
                    handler_open_close_btns(ticket_number, action.upper())
                    log.info(f"CLOSED ticket {ticket_number}")
                    self.records_section[ticket_index]['status'].setText("CLOSED")
                    self.records_section[ticket_index]['close_btn'].hide()
                    self.records_section[ticket_index]['open_btn'].show()
                self.records_section[ticket_index]['status'].setText(
                    get_property("Consignments", "status", "consignment", ticket_number)
                )
            except Exception as e:
                log.error(f"Could not {action} ticket {ticket_number}: {e}")
        return handler

    def make_print_handler(self, ticket_index):
        def handler():
            ticket_number = self.records_section[ticket_index]['ticket_num'].text().strip()
            try:
                handler_db_pdf(int(ticket_number))
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
            ticket = self.records_section[ticket_index]
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
                'revenue_shared': unpacked_ticket['revenue']['shared'],
                'revenue_grouped': unpacked_ticket['revenue']['grouped']
            }

        return gather_ticket

    def make_pdf_handler(self, ticket_index):
        def handler():
            self.handle_pdf_btn_clicked(ticket_index)
        return handler

    def handle_pdf_btn_clicked(self, ticket_index):
        ticket_number = self.records_section[ticket_index]['ticket_num'].text().strip()
        try:
            handler_db_pdf(int(ticket_number))
            log.info(f"PDF generated for ticket {ticket_number}")
        except Exception as e:
            log.error(f"ERROR generating PDF for ticket {ticket_number}: {e}")

    def make_view_handler(self, ticket_index):
        def handler():
            self.on_view_clicked(ticket_index)
            pass
        return handler

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

    def on_view_clicked(self, ticket_index):
        try:
            records_section = self.records_section[ticket_index]
            ticket_number = records_section['ticket_num'].text().strip()

            if not ticket_number:
                log.warning("No ticket number available")
                return

            details_container = records_section['details_container']
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
                    view_ticket.setup_ui(records_section, ticket_details)

                    records_section['view_ticket'] = view_ticket

                    details_container.setVisible(True)
                    records_section['view_btn'].setText("Hide")
                    log.info(f"Displaying details for ticket {ticket_number}")
                else:
                    log.error(f"No details found for ticket {ticket_number}")
            else:
                details_container.setVisible(False)
                records_section['view_btn'].setText("View")
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
