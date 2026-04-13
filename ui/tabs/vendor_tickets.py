from PyQt6.QtCore import QTimer, QRegularExpression
from PyQt6.QtGui import QIntValidator, QRegularExpressionValidator
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtWidgets import QFrame
from PyQt6.QtWidgets import QMessageBox
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
from ui.core import format_phone
from ui.core import format_state
from ui.core import excel_button
from ui.core.view_ticket import ViewTicket
from utils.core import generate_excel as xls_gen

from utils.message_bus import status_bar_instance
import utils.logger.logger as log


class VendorTicketsTab(BaseTab):
    def __init__(self, api_handler, db_connection):
        self.ticket_counter = None
        self.tickets_layout = None
        self.tickets_section = []
        self.db_connection = db_connection
        self.current_ticket_index = 0

        super().__init__(api_handler, "vendor_tickets")

        self.search_timer = QTimer()
        self.search_timer.setSingleShot(True)
        self.search_timer.timeout.connect(self.build_and_search)

    def setup_ui(self):
        background = QVBoxLayout(self)

        main_layout_widget = QWidget()
        main_layout = QVBoxLayout(main_layout_widget)

        vendor_section_row_0 = QHBoxLayout()
        vendor_title = QLabel("View Vendor Tickets")
        vendor_title.setObjectName("post_title")
        vendor_section_row_0.addWidget(vendor_title)
        vendor_section_row_0.addStretch()
        main_layout.addLayout(vendor_section_row_0)

        hr1 = QFrame()
        hr1.setFrameShape(QFrame.Shape.HLine)
        hr1.setFrameShadow(QFrame.Shadow.Sunken)
        hr1.setObjectName("hr")
        main_layout.addWidget(hr1)

        vendor_section_row_1 = QHBoxLayout()

        vendor_section_row_1.addWidget(QLabel("Vendor ID:"))
        self.vendor_id_input = QLineEdit()
        self.vendor_id_input.setPlaceholderText("V ID")
        self.vendor_id_input.setMaxLength(4)
        self.vendor_id_input.setFixedWidth(80)
        self.vendor_id_input.setValidator(QIntValidator(0, 9999, self))
        self.vendor_id_input.textChanged.connect(self.on_search_input_changed)
        vendor_section_row_1.addWidget(self.vendor_id_input)

        vendor_section_row_1.addWidget(QLabel("Phone Number:"))
        self.phone_number_input = format_phone.PhoneNumField()
        self.phone_number_input.setMaxLength(12)
        self.phone_number_input.setFixedWidth(150)
        self.phone_number_input.textChanged.connect(self.on_search_input_changed)
        vendor_section_row_1.addWidget(self.phone_number_input)

        vendor_section_row_1.addStretch()
        main_layout.addLayout(vendor_section_row_1)

        vendor_section_row_2 = QHBoxLayout()

        vendor_section_row_2.addWidget(QLabel("First Name:"))
        self.first_name_input = QLineEdit()
        self.first_name_input.setPlaceholderText("First Name")
        self.first_name_input.setMaxLength(30)
        self.first_name_input.setFixedWidth(263)
        alpha_validator = QRegularExpressionValidator(QRegularExpression("[A-Za-z ]+"))
        self.first_name_input.setValidator(alpha_validator)
        self.first_name_input.textChanged.connect(self.on_search_input_changed)
        vendor_section_row_2.addWidget(self.first_name_input)

        vendor_section_row_2.addWidget(QLabel("Middle Name:"))
        self.middle_name_input = QLineEdit()
        self.middle_name_input.setPlaceholderText("M. Name")
        self.middle_name_input.setMaxLength(10)
        self.middle_name_input.setFixedWidth(103)
        self.middle_name_input.setValidator(alpha_validator)
        self.middle_name_input.textChanged.connect(self.on_search_input_changed)
        vendor_section_row_2.addWidget(self.middle_name_input)

        vendor_section_row_2.addWidget(QLabel("Last Name:"))
        self.last_name_input = QLineEdit()
        self.last_name_input.setPlaceholderText("Last Name")
        self.last_name_input.setMaxLength(30)
        self.last_name_input.setFixedWidth(263)
        self.last_name_input.setValidator(alpha_validator)
        self.last_name_input.textChanged.connect(self.on_search_input_changed)
        vendor_section_row_2.addWidget(self.last_name_input)

        vendor_section_row_2.addStretch()
        main_layout.addLayout(vendor_section_row_2)

        vendor_section_row_3 = QHBoxLayout()

        vendor_section_row_3.addWidget(QLabel("Address:"))
        self.address_input = QLineEdit()
        self.address_input.setPlaceholderText("Address")
        self.address_input.setMaxLength(255)
        address_validator = QRegularExpressionValidator(QRegularExpression("[A-Za-z0-9 ]+"))
        self.address_input.setValidator(address_validator)
        self.address_input.textChanged.connect(self.on_search_input_changed)
        vendor_section_row_3.addWidget(self.address_input)

        vendor_section_row_3.addWidget(QLabel("City:"))
        self.city_input = QLineEdit()
        self.city_input.setPlaceholderText("City")
        self.city_input.setMaxLength(30)
        self.city_input.setValidator(alpha_validator)
        self.city_input.textChanged.connect(self.on_search_input_changed)
        vendor_section_row_3.addWidget(self.city_input)

        vendor_section_row_3.addWidget(QLabel("State:"))
        self.state_input = format_state.FormatState()
        self.state_input.setFixedWidth(50)
        self.state_input.setValidator(alpha_validator)
        self.state_input.textChanged.connect(self.on_search_input_changed)
        vendor_section_row_3.addWidget(self.state_input)

        vendor_section_row_3.addWidget(QLabel("Zip:"))
        self.zip_input = QLineEdit()
        self.zip_input.setPlaceholderText("Zip")
        self.zip_input.setMaxLength(5)
        self.zip_input.setFixedWidth(70)
        zip_validator = QIntValidator(0, 99999, self)
        self.zip_input.setValidator(zip_validator)
        self.zip_input.textChanged.connect(self.on_search_input_changed)
        vendor_section_row_3.addWidget(self.zip_input)

        vendor_section_row_3.addStretch()
        main_layout.addLayout(vendor_section_row_3)

        action_section = QHBoxLayout()

        self.clear_btn = QPushButton("Clear")
        self.clear_btn.setFixedWidth(200)
        action_section.addWidget(self.clear_btn)

        action_section.addStretch()

        self.search_btn = QPushButton("Search")
        self.search_btn.setFixedWidth(200)
        action_section.addWidget(self.search_btn)

        main_layout.addLayout(action_section)

        hr2 = QFrame()
        hr2.setFrameShape(QFrame.Shape.HLine)
        hr2.setFrameShadow(QFrame.Shadow.Sunken)
        hr2.setObjectName("hr")
        main_layout.addWidget(hr2)

        ticket_section_row_0 = QHBoxLayout()
        ticket_title = QLabel("Tickets")
        ticket_title.setObjectName("post_title")
        ticket_section_row_0.addWidget(ticket_title)
        main_layout.addLayout(ticket_section_row_0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)

        self.tickets_layout = QVBoxLayout()
        scroll_layout.addLayout(self.tickets_layout)

        scroll_layout.addStretch(1)

        hr2 = QFrame()
        hr2.setFrameShape(QFrame.Shape.HLine)
        hr2.setFrameShadow(QFrame.Shadow.Sunken)
        hr2.setObjectName("hr")
        main_layout.addWidget(hr2)

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
            self.vendor_id_input,
            self.phone_number_input,
            self.first_name_input,
            self.middle_name_input,
            self.last_name_input,
            self.address_input,
            self.city_input,
            self.state_input,
            self.zip_input,
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
        :Purpose: forces a wait before triggering search
        :Author(s): Joe Lee
        """
        self.search_timer.start(300)

    def build_and_search(self):
        """
        :Purpose: Builds a vendor query from input fields, then fetches matching tickets
        :Author(s): Joe Lee
        """
        self.remove_ticket_section()

        conditions = ["c.entity_type = 'vendor'"]
        properties = []

        def add_property(prop, value, operator="="):
            if value:
                if operator == "CONTAINS":
                    conditions.append(f"CONTAINS(LOWER(c.{prop}), LOWER(@{prop}))")
                else:
                    conditions.append(f"c.{prop} {operator} @{prop}")
                properties.append({"name": f"@{prop}", "value": value})

        vendor_id = self.vendor_id_input.text().strip()
        if vendor_id:
            try:
                add_property("vendor_id", int(vendor_id), "=")
            except ValueError:
                pass

        phone = self.phone_number_input.text().strip().replace('-', '')
        if phone:
            conditions.append("CONTAINS(REPLACE(c.phone, '-', ''), @phone)")
            properties.append({"name": "@phone", "value": phone})

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

        zip_code = self.zip_input.text().strip()
        if zip_code:
            conditions.append("CONTAINS(ToString(c.zip), @zip)")
            properties.append({"name": "@zip", "value": zip_code})

        if len(conditions) == 1:
            self.fetch()
            return

        where_clause = " AND ".join(conditions)
        vendor_query = f"SELECT c.vendor_id FROM c WHERE {where_clause}"
        self.query_db(vendor_query, properties)

    def query_db(self, vendor_query: str, properties: list = None):
        """
        :purpose: gets vendor id based on input values, then gets consignments from vendor id
        :Author(s): Joe Lee
        """
        self.remove_ticket_section()
        try:
            # find vendor_id that could match field inputs
            entity_container = self.db_connection.connect("Entities")
            vendor_results = list(entity_container.query_items(
                query=vendor_query,
                parameters=properties if properties else [],
                enable_cross_partition_query=True
            ))

            vendor_ids = []
            for item in vendor_results:
                if 'vendor_id' in item:
                    vendor_ids.append(int(item['vendor_id']))
            if not vendor_ids:
                status_bar_instance.send_message("No vendors found matching criteria")
                return

            # find tickets with vendor_id
            consignment_container = self.db_connection.connect("Consignments")
            tickets = []

            for vendor_id in vendor_ids:
                results = list(consignment_container.query_items(
                    query="""
                        SELECT * FROM c
                        WHERE c.entity_type = 'consignment'
                        AND c.vendor_id = @vendor_id
                    """,
                    parameters=[{"name": "@vendor_id", "value": vendor_id}],
                    enable_cross_partition_query=True
                ))
                for item in results:
                    tickets.append({
                        'ticket_number': item.get('consignment_id'),
                        'vendor_id': item.get('vendor_id', ''),
                        'product_ids': item.get('product_ids', ''),
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
                status_bar_instance.send_message("No tickets found for matching vendors")
            else:
                status_bar_instance.send_message(f"Found {len(tickets)} ticket(s)")

        except Exception as e:
            log.error(f"Error executing query: {e}")
            status_bar_instance.send_message("Query failed")

    def fetch(self):
        """
        :purpose: fetches all consignment tickets (no filter)
        :author(s): Joe Lee
        """
        try:
            container = self.db_connection.connect("Consignments")
            results = list(container.query_items(
                query="SELECT * FROM c WHERE c.entity_type = 'consignment'",
                enable_cross_partition_query=True
            ))

            tickets = []
            for item in results:
                tickets.append({
                    'ticket_number': item.get('consignment_id'),
                    'vendor_id': item.get('vendor_id', ''),
                    'product_ids': item.get('product_ids', ''),
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
            log.error(f"Error fetching all tickets: {e}")
            status_bar_instance.send_message("Fetch failed")

    def add_ticket_section(self):
        tickets_section = {}

        section_widget = QWidget()
        section_layout = QVBoxLayout(section_widget)
        section_layout.setContentsMargins(0, 0, 0, 0)

        line1_layout = QHBoxLayout()

        line1_layout.addWidget(QLabel("Ticket Number:"))
        ticket_number_input = QLineEdit()
        ticket_number_input.setObjectName("READ_ONLY")
        ticket_number_input.setReadOnly(True)
        ticket_number_input.setFixedWidth(100)
        line1_layout.addWidget(ticket_number_input)
        tickets_section['ticket_num'] = ticket_number_input

        line1_layout.addWidget(QLabel("Datetime:"))
        datetime_input = QLineEdit()
        datetime_input.setObjectName("READ_ONLY")
        datetime_input.setReadOnly(True)
        datetime_input.setFixedWidth(195)
        line1_layout.addWidget(datetime_input)
        tickets_section['datetime'] = datetime_input

        line1_layout.addWidget(QLabel("Status:"))
        status_input = QLineEdit()
        status_input.setObjectName("READ_ONLY")
        status_input.setPlaceholderText("Status")
        status_input.setReadOnly(True)
        status_input.setFixedWidth(70)
        line1_layout.addWidget(status_input)
        tickets_section['status'] = status_input

        line1_layout.addStretch()

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
        tickets_section['product_details_widget'] = details_container

        hr = QFrame()
        hr.setFrameShape(QFrame.Shape.HLine)
        hr.setFrameShadow(QFrame.Shadow.Sunken)
        hr.setObjectName("hr")
        section_layout.addWidget(hr)

        self.tickets_layout.addWidget(section_widget)

        ticket_index = len(self.tickets_section)
        tickets_section['index'] = ticket_index

        view_btn.clicked.connect(self.make_view_handler(ticket_index))
        pdf_btn.clicked.connect(self.make_pdf_handler(ticket_index))
        excel_btn.link_gather_function(self.make_form_handler(ticket_index))
        print_btn.clicked.connect(self.make_print_handler(ticket_index))
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
            :Purpose: Handles open and close button via a sequence of events
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

    def make_print_handler(self, ticket_index):
        """
        :Purpose: Instance Handler
        :Author(s): Joe Lee
        """
        def handler():
            """
            :Purpose: Handles print button via a sequence of events
            :Author(s): Joe Lee
            """
            ticket_section = self.tickets_section[ticket_index]
            ticket_number = ticket_section['ticket_num'].text().strip()
            try:
                handler_db_pdf(int(ticket_number))
            except Exception as e:
                log.error(f"Could not generate PDF for ticket {ticket_number}: {e}")
                return

            try:
                handler_print(ticket_number)
                log.info(f"Print requested for ticket {ticket_number}")
                QMessageBox.information(self, "PDF Generation Succeeded",
                                        f"Ticket {ticket_number} successfully requested to print")
            except Exception as e:
                QMessageBox.critical(self, "Print Failed", f"Failed to print ticket {ticket_number}:\n\n{e}")
        return handler

    def make_pdf_handler(self, ticket_index):
        """
        :Purpose: Instance Handler
        :Author(s): Joe Lee
        """
        def handler():
            """
            :Purpose: Handles pdf generation
            :Author(s): Joe Lee
            """
            ticket_section = self.tickets_section[ticket_index]
            ticket_number = ticket_section['ticket_num'].text().strip()
            if ticket_number:
                self.handle_pdf_btn_clicked(ticket_number)
            else:
                log.warning("No ticket number available for PDF generation")
        return handler

    def handle_pdf_btn_clicked(self, ticket_number):
        """
        :Purpose: handles interaction between pdf generation files
        :Param: ticket_number - typecasted value found in GUI ticket field
        :Author(s): Joe Lee
        """
        try:
            handler_db_pdf(int(ticket_number))
            log.info(f"PDF generated for ticket {ticket_number}")
            QMessageBox.information(self, "PDF Generation Succeeded", f"Ticket {ticket_number} successfully generated a PDF")
        except Exception as e:
            log.error(f"ERROR generating PDF for ticket {ticket_number}: {e}")
            QMessageBox.information(self, "PDF Generation Failed", f"Ticket {ticket_number} failed to generate a PDF")

    def make_form_handler(self, ticket_index):
        """
        :Purpose: Instance Handler
        :Author(s): Maksym Komarov
        """
        def gather_ticket():
            """
            :Purpose: Gathers consignment data
            :Author(s): Maksym Komarov
            """
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

    def make_view_handler(self, ticket_index):
        """
        :Purpose: Instance Handler
        :Author(s): Joe Lee
        """
        def handler():
            """
            :Purpose: Handles view button via a sequence of events
            :Author(s): Joe Lee
            """
            self.on_view_clicked(ticket_index)
        return handler

    def remove_ticket_section(self):
        """
        :Purpose: Removes ticket section when cleared
        :Author(s): Joe Lee
        """
        for i in reversed(range(self.tickets_layout.count())):
            widget = self.tickets_layout.itemAt(i).widget()
            if widget:
                self.tickets_layout.removeWidget(widget)
                widget.deleteLater()

        self.tickets_section.clear()
        log.info("All tickets cleared")

    def setup_button_connections(self):
        self.clear_btn.clicked.connect(self.clear)
        self.search_btn.clicked.connect(self.build_and_search)

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