from PyQt6.QtGui import QIntValidator
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtWidgets import QHBoxLayout
from PyQt6.QtWidgets import QLabel
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtWidgets import QScrollArea
from PyQt6.QtWidgets import QWidget

from ui.tabs.base import BaseTab

from handlers.handler_print import handler_print
from handlers.handler_pdf import handler_db_pdf
from services.get_item import get_item
from services.get_item_by_property import get_item_by_property
from ui.core import format_phone
from ui.core import excel
from ui.core.view_ticket import ViewTicket
from utils.core import generate_excel as xls_gen

from services.message_bus import status_bar_instance
import utils.logger.logger as log

class VendorTicketsTab(BaseTab):
    def __init__(self, api_handler, db_connection):
        self.ticket_counter = None
        self.tickets_layout = None
        self.tickets_section = []
        self.db_connection = db_connection
        self.current_ticket_index = 0

        super().__init__(api_handler, "vendor_tickets")

    def setup_ui(self):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        layout = QVBoxLayout(scroll_content)

        vendor_section_row_0 = QHBoxLayout()

        vendor_title = QLabel("Vendor Information")
        vendor_title.setObjectName("post_title")
        vendor_section_row_0.addWidget(vendor_title)

        vendor_section_row_0.addStretch()

        layout.addLayout(vendor_section_row_0)

        vendor_section_row_1 = QHBoxLayout()

        vendor_section_row_1.addWidget(QLabel("Vendor ID:"))
        self.vendor_id_input = QLineEdit()
        self.vendor_id_input.setPlaceholderText("4 INTS")
        self.vendor_id_input.setFixedWidth(80)
        self.vendor_id_input.setValidator(QIntValidator(0, 9999, self))
        self.vendor_id_input.textEdited.connect(self.auto_pop_vend)
        vendor_section_row_1.addWidget(self.vendor_id_input)

        vendor_section_row_1.addWidget(QLabel("Phone Number:"))
        self.phone_input = format_phone.PhoneNumField()
        self.phone_input.setFixedWidth(150)
        self.phone_input.setValidator(QIntValidator(0, 2147483647, self))
        self.phone_input.textEdited.connect(self.auto_pop_vend_by_phone)
        vendor_section_row_1.addWidget(self.phone_input)

        vendor_section_row_1.addStretch()
        layout.addLayout(vendor_section_row_1)

        vendor_section_row_2 = QHBoxLayout()

        vendor_section_row_2.addWidget(QLabel("First Name:"))
        self.first_name_input = QLineEdit()
        self.first_name_input.setObjectName("READ_ONLY")
        self.first_name_input.setPlaceholderText("READ_ONLY_FROM_DB")
        self.first_name_input.setReadOnly(True)
        self.first_name_input.setMaxLength(30)
        self.first_name_input.setMinimumWidth(263)
        vendor_section_row_2.addWidget(self.first_name_input)

        vendor_section_row_2.addWidget(QLabel("Middle Name:"))
        self.middle_name_input = QLineEdit()
        self.middle_name_input.setObjectName("READ_ONLY")
        self.middle_name_input.setPlaceholderText("READ_ONLY_FROM_DB")
        self.middle_name_input.setReadOnly(True)
        self.middle_name_input.setMaxLength(10)
        self.middle_name_input.setMinimumWidth(103)
        vendor_section_row_2.addWidget(self.middle_name_input)

        vendor_section_row_2.addWidget(QLabel("Last Name:"))
        self.last_name_input = QLineEdit()
        self.last_name_input.setObjectName("READ_ONLY")
        self.last_name_input.setPlaceholderText("READ_ONLY_FROM_DB")
        self.last_name_input.setReadOnly(True)
        self.last_name_input.setMaxLength(30)
        self.last_name_input.setMinimumWidth(263)
        vendor_section_row_2.addWidget(self.last_name_input)

        layout.addLayout(vendor_section_row_2)

        vendor_section_row_3 = QHBoxLayout()

        vendor_section_row_3.addWidget(QLabel("Address:"))
        self.address_input = QLineEdit()
        self.address_input.setObjectName("READ_ONLY")
        self.address_input.setPlaceholderText("READ_ONLY_FROM_DB")
        self.address_input.setReadOnly(True)
        self.address_input.setMaxLength(255)
        vendor_section_row_3.addWidget(self.address_input)

        vendor_section_row_3.addWidget(QLabel("City:"))
        self.city_input = QLineEdit()
        self.city_input.setObjectName("READ_ONLY")
        self.city_input.setPlaceholderText("READ_ONLY_FROM_DB")
        self.city_input.setReadOnly(True)
        self.city_input.setMaxLength(30)
        vendor_section_row_3.addWidget(self.city_input)

        vendor_section_row_3.addWidget(QLabel("State:"))
        self.state_input = QLineEdit()
        self.state_input.setObjectName("READ_ONLY")
        self.state_input.setPlaceholderText("XX")
        self.state_input.setReadOnly(True)
        self.state_input.setMaxLength(2)
        self.state_input.setFixedWidth(50)
        vendor_section_row_3.addWidget(self.state_input)

        vendor_section_row_3.addWidget(QLabel("Zip Code:"))
        self.zip_input = QLineEdit()
        self.zip_input.setObjectName("READ_ONLY")
        self.zip_input.setPlaceholderText("XXXXX")
        self.zip_input.setReadOnly(True)
        self.zip_input.setMaxLength(5)
        self.zip_input.setFixedWidth(70)
        vendor_section_row_3.addWidget(self.zip_input)

        layout.addLayout(vendor_section_row_3)

        hr1 = QLabel()
        hr1.setObjectName("hr")
        layout.addWidget(hr1)

        ticket_section_row_0 = QHBoxLayout()

        ticket_title = QLabel("Tickets")
        ticket_title.setObjectName("post_title")
        ticket_section_row_0.addWidget(ticket_title)

        layout.addLayout(ticket_section_row_0)

        self.tickets_layout = QVBoxLayout()

        layout.addLayout(self.tickets_layout)

        ticket_section_row_1 = QHBoxLayout()

        layout.addLayout(ticket_section_row_1)
        layout.addStretch(1)

        hr3 = QLabel()
        hr3.setObjectName("hr")
        layout.addWidget(hr3)

        scroll.setWidget(scroll_content)
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(scroll)

        vendor_section_row_3 = QHBoxLayout()
        # vendor_section_row_3.addStretch()
        self.fetch_btn = QPushButton("Fetch")
        # self.fetch_btn.setFixedWidth(200)
        vendor_section_row_3.addWidget(self.fetch_btn)
        main_layout.addLayout(vendor_section_row_3)

        self.setup_button_connections()

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
        ticket_number_input.setFixedWidth(80)
        line1_layout.addWidget(ticket_number_input)
        tickets_section['ticket_num'] = ticket_number_input

        line1_layout.addWidget(QLabel("Date and Time:"))
        datetime_input = QLineEdit()
        datetime_input.setObjectName("READ_ONLY")
        datetime_input.setReadOnly(True)
        datetime_input.setFixedWidth(175)
        line1_layout.addWidget(datetime_input)
        tickets_section['datetime'] = datetime_input

        line1_layout.addWidget(QLabel("Status:"))
        status_input = QLineEdit()
        status_input.setObjectName("READ_ONLY")
        status_input.setPlaceholderText("CLOSED")
        status_input.setReadOnly(True)
        status_input.setFixedWidth(70)
        line1_layout.addWidget(status_input)
        tickets_section['status'] = status_input

        line1_layout.addStretch()

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

        close_btn = QPushButton("Close")
        close_btn.setObjectName("red_btn")
        line1_layout.addWidget(close_btn)
        tickets_section['close_btn'] = close_btn

        section_layout.addLayout(line1_layout)

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

        tickets_section['product_details_widget'] = details_container

        self.tickets_layout.addWidget(section_widget)

        ticket_index = len(self.tickets_section)
        tickets_section['index'] = ticket_index

        view_btn.clicked.connect(self.make_view_handler(ticket_index))
        pdf_btn.clicked.connect(self.make_pdf_handler(ticket_index))
        excel_btn.link_gather_function(self.make_form_handler(ticket_index))
        print_btn.clicked.connect(self.make_print_handler(ticket_index))

        self.tickets_section.append(tickets_section)

    def make_print_handler(self, ticket_index):
        def handler():
            ticket_section = self.tickets_section[ticket_index]
            ticket_number = ticket_section['ticket_num'].text().strip()
            try:
                handler_db_pdf(int(ticket_number))
            except Exception as e:
                log.error(f"Could not generate PDF for ticket {ticket_number}: {e}")
                return

            handler_print(ticket_number)
            log.info(f"Print requested for ticket {ticket_number}")
        return handler

    def make_pdf_handler(self, ticket_index):
        """
        :Purpose: handles GUI interactions with the pdf_btn
        :Param: ticket_index - GUI objects for the ticket field
        :Author(s): Joe Lee
        """
        def handler():
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
        except Exception as e:
            log.error(f"ERROR generating PDF for ticket {ticket_number}: {e}")

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
                'revenue_shared': unpacked_ticket['revenue']['shared'],
                'revenue_grouped': unpacked_ticket['revenue']['grouped']
            }
        
        return gather_ticket 

    def make_view_handler(self, ticket_index):
        def handler():
            self.on_view_clicked(ticket_index)

        return handler

    def remove_ticket_section(self):
        for i in reversed(range(self.tickets_layout.count())):
            widget = self.tickets_layout.itemAt(i).widget()
            if widget:
                self.tickets_layout.removeWidget(widget)
                widget.deleteLater()

        self.tickets_section.clear()

        log.info("All tickets cleared")

    def setup_button_connections(self):
        self.fetch_btn.clicked.connect(self.on_fetch_clicked)

    def on_fetch_clicked(self):
        self.remove_ticket_section()
        vendor_id = self.vendor_id_input.text().strip()
        if vendor_id:
            tickets = self.fetch(vendor_id)
            if not tickets:
                log.warning(f"No tickets found for Vendor ID: {vendor_id}")
            else:
                for ticket in tickets:
                    self.add_ticket_section()
                    last_section = self.tickets_section[-1]
                    last_section['ticket_num'].setText(str(ticket['ticket_number']))
                    last_section['datetime'].setText(str(ticket['datetime']))
                    last_section['status'].setText(ticket['status'])
        else:
            status_bar_instance.send_message("Please enter a Vendor ID")

    def fetch(self, vendor_id_input):
        try:
            container = self.db_connection.connect("Consignments")

            query = """
                    SELECT c.ticket_number, c.datetime, c.status
                    FROM c
                    WHERE c.vendor_id = @vendor_id
                    ORDER BY c.ticket_number DESC
                    """

            parameters = [
                {"name": "@vendor_id", "value": int(vendor_id_input)}
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
                    'status': item['status']
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

    def auto_pop_vend(self):
        try:
            field_mapping = {
                'phone': self.phone_input,
                'first_name': self.first_name_input,
                'middle_name': self.middle_name_input,
                'last_name': self.last_name_input,
                'address': self.address_input,
                'city': self.city_input,
                'state': self.state_input,
                'zip': self.zip_input
            }
            vend_id = self.vendor_id_input.text().strip()

            if vend_id:
                item = get_item("Entities", "vendor", vend_id)
                if item is not None:
                    for field_name, input_field in field_mapping.items():
                        if field_name in item:
                            input_field.setText(item[field_name])
                            input_field.setObjectName("READ_ONLY")
                            input_field.setReadOnly(True)
                else:
                    for input_field in field_mapping.values():
                        input_field.setText("")
                        input_field.setObjectName("")
                        input_field.setReadOnly(False)
            else:
                for input_field in field_mapping.values():
                    input_field.setText("")
                    input_field.setObjectName("")
                    input_field.setReadOnly(False)

            for input_field in field_mapping.values():
                input_field.style().unpolish(input_field)
                input_field.style().polish(input_field)

        except Exception as e:
            log.error(f"Failed to fetch vendor: {e}")

    def auto_pop_vend_by_phone(self):
        try:
            field_mapping = {
                'vendor_id': self.vendor_id_input,
                'first_name': self.first_name_input,
                'middle_name': self.middle_name_input,
                'last_name': self.last_name_input,
                'address': self.address_input,
                'city': self.city_input,
                'state': self.state_input,
                'zip': self.zip_input
            }
            phone = self.phone_input.text().strip()

            if phone:
                item = get_item_by_property("Entities", "vendor", "phone", phone)
                if item is not None:
                    for field_name, input_field in field_mapping.items():
                        if field_name in item:
                            input_field.setText(str(item[field_name]))
                            input_field.setObjectName("READ_ONLY")
                            input_field.setReadOnly(True)
                else:
                    for input_field in field_mapping.values():
                        input_field.setText("")
                        input_field.setObjectName("")
                        input_field.setReadOnly(False)
            else:
                for input_field in field_mapping.values():
                    input_field.setText("")
                    input_field.setObjectName("")
                    input_field.setReadOnly(False)

            for input_field in field_mapping.values():
                input_field.style().unpolish(input_field)
                input_field.style().polish(input_field)

        except Exception as e:
            log.error(f"Failed to fetch vendor by phone: {e}")