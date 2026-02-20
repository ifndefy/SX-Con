from PyQt6.QtGui import QIntValidator
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtWidgets import QHBoxLayout
from PyQt6.QtWidgets import QLabel
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtWidgets import QScrollArea
from PyQt6.QtWidgets import QWidget

from services.get_item import get_item
from services.get_item_by_property import get_item_by_property
from ui.core import format_phone
from ui.core import excel
from utils.core import generate_excel as xls_gen
from ui.core.view_ticket import ViewTicket
from ui.tabs.base import BaseTab
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

        vendor_section_row_3 = QHBoxLayout()
        vendor_section_row_3.addStretch()
        self.fetch_btn = QPushButton("Fetch")
        self.fetch_btn.setFixedWidth(200)
        vendor_section_row_3.addWidget(self.fetch_btn)
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

        # self.status_label.setText("All tickets cleared")

    def setup_button_connections(self):
        self.fetch_btn.clicked.connect(self.on_fetch_clicked)

    def on_fetch_clicked(self):
        self.remove_ticket_section()
        vendor_id = self.vendor_id_input.text().strip()
        if vendor_id:
            tickets = self.fetch(vendor_id)
            if not tickets:
                self.status_label.setText(f"No tickets found for Vendor ID: {vendor_id}")
            else:
                for ticket in tickets:
                    self.add_ticket_section()
                    last_section = self.tickets_section[-1]
                    last_section['ticket_num'].setText(str(ticket['ticket_number']))
                    last_section['datetime'].setText(str(ticket['datetime']))
                    last_section['status'].setText(ticket['status'])
        else:
            self.status_label.setText("Please enter a Vendor ID")

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
                self.status_label.setText("No ticket number available")
                return

            details_container = ticket_section['details_container']
            is_visible = details_container.isVisible()

            if not is_visible:
                ticket_details = self.view(ticket_number)
                if ticket_details:
                    self.view_ticket_details(ticket_section, ticket_details)
                    details_container.setVisible(True)
                    ticket_section['view_btn'].setText("Hide")
                    # self.status_label.setText(f"Displaying details for ticket {ticket_number}")
                else:
                    # self.status_label.setText(f"No details found for ticket {ticket_number}")
                    print("err") # delete when fixed
            else:
                details_container.setVisible(False)
                ticket_section['view_btn'].setText("View")
                self.status_label.setText(f"Hidden details for ticket {ticket_number}")

        except Exception as e:
            log.error(f"Error in on_view_clicked: {e}")
            self.status_label.setText("Error loading ticket details")

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