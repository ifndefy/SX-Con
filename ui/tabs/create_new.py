from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtWidgets import QApplication
from PyQt6.QtWidgets import QComboBox
from PyQt6.QtWidgets import QFrame
from PyQt6.QtWidgets import QHBoxLayout
from PyQt6.QtWidgets import QLabel
from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtWidgets import QScrollArea
from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QIntValidator
from PyQt6.QtGui import QRegularExpressionValidator
from PyQt6.QtCore import QRegularExpression

from handlers.handler_pdf import handler_live_pdf
from handlers import handler_print
from services.get_item import get_item
from services.get_item_by_property import get_item_by_property
from services.message_bus import status_bar_instance
from services.parse_consignment_table import fetch_consignment_data
from src.core import generate_agg_data
from src.user import current_user
from ui.tabs.base import BaseTab
from ui.core.autogen_date import generate_host_datetime
from ui.core.autogen_ticket_num import autogen_ticket_num
from ui.core.revenue_by_product_type import RevenueByProdType
from ui.core.revenue_generation import RevenueGeneration
from ui.core import format_phone
from ui.core import format_price
from ui.core import format_state
from utils.core import generate_excel as xls_gen
import utils.logger.logger as log

import decimal as d

class CreateNewTab(BaseTab):
    def __init__(self, api_handler, db_connection):
        self.ticket_input = None
        self.vendor_id_input = None
        self.phone_input = None
        self.datetime_input = None
        self.first_name_input = None
        self.middle_name_input = None
        self.last_name_input = None
        self.address_input = None
        self.city_input = None
        self.state_input = None
        self.products_layout = None
        self.remove_product_btn = None
        self.add_product_btn = None
        self.clear_btn = None
        self.revenue_generation = None
        self.create_btn = None

        self.rates_container = fetch_consignment_data()
        self.product_sections = []
        self.product_counter = 1
        self.db_connection = db_connection

        super().__init__(api_handler, "create_new")

        self.setup_button_connections()

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

        # Push to the right
        vendor_section_row_0.addStretch()

        # Ticket Number on right: Read-only
        vendor_section_row_0.addWidget(QLabel("Ticket Number:"))
        self.ticket_input = QLineEdit()
        self.ticket_input.setObjectName("READ_ONLY")
        self.update_ticket_number()
        self.ticket_input.setReadOnly(True)
        self.ticket_input.setFixedWidth(240)
        vendor_section_row_0.addWidget(self.ticket_input)

        # Ends creation and adds vendor_section_row_0 to window
        layout.addLayout(vendor_section_row_0)

        hr0 = QFrame()
        hr0.setFrameShape(QFrame.Shape.HLine)
        hr0.setFrameShadow(QFrame.Shadow.Sunken)
        hr0.setObjectName("hr")
        layout.addWidget(hr0)

        # Vendor Line 1 Creation: Vendor ID + Phone Number + Date and Time
        vendor_section_row_1 = QHBoxLayout()

        # Vendor ID
        vendor_section_row_1.addWidget(QLabel("ID:"))
        self.vendor_id_input = QLineEdit()
        self.vendor_id_input.setObjectName("DEFAULT")
        self.vendor_id_input.setPlaceholderText("V ID")
        self.vendor_id_input.setMaxLength(4)
        self.vendor_id_input.setFixedWidth(80)
        self.vendor_id_input.setValidator(QIntValidator(0, 9999, self))
        self.vendor_id_input.returnPressed.connect(self.auto_pop_vend)
        vendor_section_row_1.addWidget(self.vendor_id_input)

        # Phone Number
        vendor_section_row_1.addWidget(QLabel("Phone Number:"))
        self.phone_input = format_phone.PhoneNumField()
        self.phone_input.setObjectName("DEFAULT")
        self.phone_input.setFixedWidth(150)
        self.phone_input.returnPressed.connect(self.auto_pop_vend_by_phone)
        vendor_section_row_1.addWidget(self.phone_input)

        vendor_section_row_1.addStretch()

        # Date and Time - Read-only
        vendor_section_row_1.addWidget(QLabel("DateTime:"))
        self.datetime_input = QLineEdit()
        self.datetime_input.setObjectName("READ_ONLY")
        self.datetime_input.setFixedWidth(263)
        self.update_datetime()
        self.datetime_input.setReadOnly(True)
        vendor_section_row_1.addWidget(self.datetime_input)

        # Ends creation and adds vendor_section_row_1 to window
        layout.addLayout(vendor_section_row_1)

        # Vendor Line 2: First Name + Middle Name + Last Name
        vendor_section_row_2 = QHBoxLayout()

        # First Name
        vendor_section_row_2.addWidget(QLabel("First Name:"))
        self.first_name_input = QLineEdit()
        self.first_name_input.setPlaceholderText("First Name")
        self.first_name_input.setMaxLength(30)
        self.first_name_input.setMinimumWidth(263)
        alpha_validator = QRegularExpressionValidator(QRegularExpression("[A-Za-z ]+"))
        self.first_name_input.setValidator(alpha_validator)
        vendor_section_row_2.addWidget(self.first_name_input)

        # Middle Name
        vendor_section_row_2.addWidget(QLabel("Middle Name:"))
        self.middle_name_input = QLineEdit()
        self.middle_name_input.setPlaceholderText("Middle Name")
        self.middle_name_input.setMaxLength(10)
        self.middle_name_input.setMinimumWidth(103)
        self.middle_name_input.setValidator(alpha_validator)
        vendor_section_row_2.addWidget(self.middle_name_input)

        # Last Name
        vendor_section_row_2.addWidget(QLabel("Last Name:"))
        self.last_name_input = QLineEdit()
        self.last_name_input.setPlaceholderText("Last Name")
        self.last_name_input.setMaxLength(30)
        self.last_name_input.setMinimumWidth(263)
        self.last_name_input.setValidator(alpha_validator)
        vendor_section_row_2.addWidget(self.last_name_input)

        # End creation and adds vendor_section_row_2 to the window
        layout.addLayout(vendor_section_row_2)

        # Vendor Line 3: Address + City + State
        vendor_section_row_3 = QHBoxLayout()

        # Address
        vendor_section_row_3.addWidget(QLabel("Address:"))
        self.address_input = QLineEdit()
        self.address_input.setPlaceholderText("Address")
        self.address_input.setMaxLength(255)
        address_validator = QRegularExpressionValidator(QRegularExpression("[A-Za-z0-9 ]+"))
        self.address_input.setValidator(address_validator)
        vendor_section_row_3.addWidget(self.address_input)

        # City
        vendor_section_row_3.addWidget(QLabel("City:"))
        self.city_input = QLineEdit()
        self.city_input.setPlaceholderText("City")
        self.city_input.setMaxLength(30)
        self.city_input.setValidator(alpha_validator)
        vendor_section_row_3.addWidget(self.city_input)

        # State
        vendor_section_row_3.addWidget(QLabel("State:"))
        self.state_input = format_state.FormatState()
        self.state_input.setMaxLength(2)
        self.state_input.setFixedWidth(50)
        self.state_input.setValidator(alpha_validator)
        vendor_section_row_3.addWidget(self.state_input)

        # Zip Code
        vendor_section_row_3.addWidget(QLabel("Zip Code:"))
        self.zip_input = QLineEdit()
        self.zip_input.setPlaceholderText("Zip")
        self.zip_input.setMaxLength(5)
        self.zip_input.setFixedWidth(70)
        zip_validator = QIntValidator(0, 99999, self)
        self.zip_input.setValidator(zip_validator)
        vendor_section_row_3.addWidget(self.zip_input)

        # End creation and adds vendor_section_row_3 to the window
        layout.addLayout(vendor_section_row_3)

        # HR Line between Vendor and Product sections
        hr1 = QFrame()
        hr1.setFrameShape(QFrame.Shape.HLine)
        hr1.setFrameShadow(QFrame.Shadow.Sunken)
        hr1.setObjectName("hr")
        layout.addWidget(hr1)

        # Product Line 0: title
        product_section_row_0 = QHBoxLayout()

        # Product Information title
        product_title = QLabel("Product Information")
        product_title.setObjectName("post_title")
        product_section_row_0.addWidget(product_title)

        product_section_row_0.addStretch()

        # End creation and adds product_section_row_0 to the window
        layout.addLayout(product_section_row_0)

        # Product Line 1: Product sections container
        self.products_layout = QVBoxLayout()

        # Add the first two product sections by default
        self.add_product_section()
        self.add_product_section()

        layout.addLayout(self.products_layout)

        # Product Line Management buttons
        product_section_row_2 = QHBoxLayout()

        # Add Product Line button
        self.add_product_btn = QPushButton("Add Product Line")
        product_section_row_2.addWidget(self.add_product_btn)

        layout.addLayout(product_section_row_2)
        layout.addStretch(1)

        # HR Line between Product and Revenue sections
        hr2 = QFrame()
        hr2.setFrameShape(QFrame.Shape.HLine)
        hr2.setFrameShadow(QFrame.Shadow.Sunken)
        hr2.setObjectName("hr")
        layout.addWidget(hr2)

        # combo_section_row_0
        combo_section_row_0 = QHBoxLayout()

        clear_section = QVBoxLayout()
        # Clear Form button on left bottom

        clear_section.addStretch()
        self.clear_btn = QPushButton("Clear Form")
        self.clear_btn.setObjectName("crit_large_btn")
        clear_section.addWidget(self.clear_btn)

        combo_section_row_0.addLayout(clear_section)

        # HR Line to separate clear button from revenue fields
        vr1 = QFrame()
        vr1.setFrameShape(QFrame.Shape.VLine)
        vr1.setFrameShadow(QFrame.Shadow.Sunken)
        vr1.setObjectName("hr")
        combo_section_row_0.addWidget(vr1)
        combo_section_row_0.addStretch()

        # wrap bottom middle to enable calculate button to expand
        bot_mid_widget = QWidget()
        bot_mid_layout = QVBoxLayout(bot_mid_widget)
        bot_mid_layout.setContentsMargins(0, 0, 0, 0)

        # top half of the bottom contains the revenue data
        middle_top_row = QHBoxLayout()

        rev_by_prod_widget = QWidget()
        rev_prod_section = QVBoxLayout(rev_by_prod_widget)
        rev_by_prod_title = QLabel("Revenue by Product Type")
        rev_by_prod_title.setObjectName("post_title")
        rev_prod_section.addWidget(rev_by_prod_title, alignment=Qt.AlignmentFlag.AlignRight)
        self.rev_by_prod = RevenueByProdType()
        rev_prod_section.addWidget(self.rev_by_prod)
        middle_top_row.addWidget(rev_by_prod_widget)

        vr2 = QFrame()
        vr2.setFrameShape(QFrame.Shape.VLine)
        vr2.setFrameShadow(QFrame.Shadow.Sunken)
        vr2.setObjectName("hr")
        middle_top_row.addWidget(vr2)

        revenue_widget = QWidget()
        revenue_section = QVBoxLayout(revenue_widget)
        revenue_title = QLabel("Revenue Sharing")
        revenue_title.setObjectName("post_title")
        revenue_section.addWidget(revenue_title, alignment=Qt.AlignmentFlag.AlignCenter)
        self.revenue_generation = RevenueGeneration()
        revenue_section.addWidget(self.revenue_generation)
        revenue_section.addStretch()
        middle_top_row.addWidget(revenue_widget)

        bot_mid_layout.addLayout(middle_top_row)

        self.calc_btn = QPushButton("Calculate")
        self.calc_btn.setObjectName("post_title")
        bot_mid_layout.addWidget(self.calc_btn)

        combo_section_row_0.addWidget(bot_mid_widget)
        combo_section_row_0.addStretch()

        # HR Line to separate revenue fields from action buttons
        vr3 = QFrame()
        vr3.setFrameShape(QFrame.Shape.VLine)
        vr3.setFrameShadow(QFrame.Shadow.Sunken)
        vr3.setObjectName("hr")
        combo_section_row_0.addWidget(vr3)

        # Action buttons
        action_layout = QVBoxLayout()

        self.excel_btn = QPushButton("Excel")
        self.pdf_btn = QPushButton("PDF")
        self.print_btn = QPushButton("Print")

        action_layout.addWidget(self.excel_btn)
        action_layout.addWidget(self.pdf_btn)
        action_layout.addWidget(self.print_btn)

        action_layout.addStretch()

        # Create Record button on right
        self.create_btn = QPushButton("Create Record")
        self.create_btn.setObjectName("large_btn")
        action_layout.addWidget(self.create_btn)

        combo_section_row_0.addLayout(action_layout)
        layout.addLayout(combo_section_row_0)

        # Set up the scroll area
        scroll.setWidget(scroll_content)
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(scroll)

    def add_product_section(self):
        """
        :purpose: adds additional product lines
        :return: None
        :author(s): Joe Lee
        """
        product_section = {}

        # Product section container
        section_widget = QWidget()
        section_layout = QVBoxLayout(section_widget)
        section_layout.setContentsMargins(0, 0, 0, 0)

        hr1 = QFrame()
        hr1.setFrameShape(QFrame.Shape.HLine)
        hr1.setFrameShadow(QFrame.Shadow.Sunken)
        hr1.setObjectName("hr")
        section_layout.addWidget(hr1)

        # Line 1: Product ID and Product Name
        line1_layout = QHBoxLayout()

        # Product ID - Fixed width for 10 integers
        line1_layout.addWidget(QLabel("ID:"))
        product_id_input = QLineEdit()
        product_id_input.setPlaceholderText("P ID")
        product_id_input.setMaxLength(10)
        product_id_input.setFixedWidth(120)
        product_id_validator = QRegularExpressionValidator(QRegularExpression("[0-9]{0,10}"))
        product_id_input.setValidator(product_id_validator)

        product_id_input.returnPressed.connect(self.auto_pop_prod)

        line1_layout.addWidget(product_id_input)
        product_section['product_id'] = product_id_input

        product_type_label = QLabel("Type:")
        line1_layout.addWidget(product_type_label)

        product_type_input = QComboBox()
        product_types = ["Hot Food", "General", "Produce"]
        product_type_input.addItems(product_types)
        product_type_input.setCurrentIndex(-1)
        product_type_input.setPlaceholderText("Type")
        line1_layout.addWidget(product_type_input)
        product_section['product_type'] = product_type_input

        # Product Name - Takes up remaining space
        line1_layout.addWidget(QLabel("Name:"))
        product_name_input = QLineEdit()
        product_name_input.setPlaceholderText("Product name")
        alpha_validator = QRegularExpressionValidator(QRegularExpression("[A-Za-z ]+"))
        product_name_input.setValidator(alpha_validator)

        product_name_input.returnPressed.connect(self.auto_pop_prod_by_name)

        line1_layout.addWidget(product_name_input)
        product_section['product_name'] = product_name_input

        # Add removal button for this specific line
        remove_btn = QPushButton("Remove Product Line")
        remove_btn.setObjectName("red_btn")
        remove_btn.clicked.connect(self.create_removal_handler(section_widget, product_section))
        line1_layout.addWidget(remove_btn)

        section_layout.addLayout(line1_layout)

        # Line 2: Notes, Price, Quantity
        line2_layout = QHBoxLayout()

        # Notes - Takes up most of the space
        line2_layout.addWidget(QLabel("Notes:"))
        notes_input = QLineEdit()
        notes_input.setPlaceholderText("Product notes")
        line2_layout.addWidget(notes_input)
        product_section['notes'] = notes_input

        # Rate - integer only, placed to the right of Notes
        line2_layout.addWidget(QLabel("Rate:"))
        rate_input = QLineEdit()
        rate_input.setReadOnly(True)
        rate_input.setObjectName("READ_ONLY")
        rate_input.setPlaceholderText("Rate")
        rate_input.setFixedWidth(80)
        rate_input.setValidator(QIntValidator(0, 100, self))
        # Default to BASE_RATE until type indicates otherwise
        rate_input.textChanged.connect(self.handle_total)
        line2_layout.addWidget(rate_input)
        product_section['rate'] = rate_input

        # Price - Fixed width
        line2_layout.addWidget(QLabel("Price:"))
        price_input = format_price.PriceField()
        price_input.setObjectName("DEFAULT")
        price_input.setFixedWidth(100)
        price_input.setMaxLength(9)
        price_input.setValidator(QIntValidator(0, 2147483647, self))
        price_input.textChanged.connect(self.handle_total)

        line2_layout.addWidget(price_input)
        product_section['price'] = price_input

        # Quantity - Fixed width (same as price)
        line2_layout.addWidget(QLabel("Qty:"))
        quantity_input = QLineEdit()
        quantity_input.setPlaceholderText("Qty")
        quantity_input.setFixedWidth(100)
        quantity_input.setValidator(QRegularExpressionValidator(QRegularExpression(r'^\d*$')))
        quantity_input.textChanged.connect(self.handle_total)
        line2_layout.addWidget(quantity_input)
        product_section['quantity'] = quantity_input

        # Total - Fixed width (same as price)
        line2_layout.addWidget(QLabel("Total:"))
        total_input = QLineEdit()
        total_input.setPlaceholderText("$0.00")
        total_input.setReadOnly(True)
        total_input.setObjectName("READ_ONLY")
        total_input.setFixedWidth(100)
        line2_layout.addWidget(total_input)
        product_section['total'] = total_input

        section_layout.addLayout(line2_layout)

        product_type_input.currentTextChanged.connect(
            lambda _txt, sec=product_section: self._on_product_type_changed(sec)
        )

        # Add to container
        self.products_layout.addWidget(section_widget)
        self.product_sections.append(product_section)
        self.product_counter += 1
        status_bar_instance.send_message(f"Added product line. Total: {len(self.product_sections)}")

    def handle_total(self):
        widget = self.sender()
        if not widget:
            return

        section = self.get_sending_widget(widget)
        if section:
            self.on_price_qty_changed(section)

    def get_sending_widget(self, widget):
        for section in self.product_sections:
            if (section['price'] is widget or section['quantity'] is widget or section['rate'] is widget):
                return section
        return None

    def on_price_qty_changed(self, section):
        price_text = section['price'].text().strip()
        qty_text = section['quantity'].text().strip()
        rate_text = section['rate'].text().strip()

        if not price_text or not qty_text or not rate_text:
            # require all fields, prevent invalid data
            section['total'].setText("$0.00")
            return

        fixed_price = generate_agg_data.convert_price(price_text)
        if fixed_price is None:
            section['total'].setText("$0.00")
            return

        try:
            qty = int(qty_text)
        except ValueError:
            section['total'].setText("$0.00")
            return

        total = RevenueGeneration.calculate_total(fixed_price, qty, rate_text)
        section['total'].setText(f"${total:.2f}")

    def _on_product_type_changed(self, product_section: dict):
        try:
            #update any admin changes to table
            self.rates_container = fetch_consignment_data()
            rate_widget = product_section.get('rate')
            type_widget = product_section.get('product_type')
            if not rate_widget or not type_widget:
                log.error("Could not retreive type and rate subwidgets")
                return
            new_rate = self.rates_container[type_widget.currentText()]
            rate_widget.setText(str(new_rate))
        except Exception as e:
            log.error(f"Failed to auto-set rate: {e}")

    def create_removal_handler(self, widget, product_section):
        def removal_handler():
            if self.show_remove_product_warning(product_section):
                self.remove_product_line(widget, product_section)

        return removal_handler

    def remove_product_line(self, widget, product_section):
        """
        :purpose: removes a specific product line
        :param widget: the widget to remove
        :param product_section: the product section data to remove
        :return: None
        """
        if product_section in self.product_sections:
            self.product_sections.remove(product_section)

        self.products_layout.removeWidget(widget)
        widget.deleteLater()

        self.product_counter -= 1
        status_bar_instance.send_message(f"Removed product line. Total: {len(self.product_sections)}")

    def show_remove_product_warning(self, product_section):
        product_id = product_section['product_id'].text().strip()
        product_name = product_section['product_name'].text().strip()

        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Warning - Product Line Removal")
        msg_box.setText(f"Are you sure you want to remove this product line?\n{product_id} - {product_name}")
        confirm_btn = msg_box.addButton("Confirm", QMessageBox.ButtonRole.AcceptRole)
        cancel_btn = msg_box.addButton("Cancel", QMessageBox.ButtonRole.RejectRole)

        msg_box.setDefaultButton(confirm_btn)

        msg_box.exec()
        return msg_box.clickedButton() == confirm_btn

    def gather_record(self):
        vendor_info = self._gather_vendor_data()
        product_info = self._gather_products_data()
        revenue_data = self._gather_revenue_data()
        return {
            'vendor_info': vendor_info,
            'prod_info': product_info,
            'revenue_shared': revenue_data['shared'],
            'revenue_grouped': revenue_data['grouped'],
            'revenue_payout': []
        }

    def handle_excel_btn(self):
        self.handle_calc_btn()
        data = self.gather_record()
        xls_gen.generate_excel(data)

    def setup_button_connections(self):
        """
        :purpose: links buttons with methods
        :return: None
        :author(s): Joe Lee
        """
        self.create_btn.clicked.connect(self.create_record)
        self.clear_btn.clicked.connect(self.clear_form)
        self.add_product_btn.clicked.connect(self.add_product_section)
        self.calc_btn.clicked.connect(self.handle_calc_btn)
        self.excel_btn.clicked.connect(self.handle_excel_btn)
        self.pdf_btn.clicked.connect(self.on_pdf_clicked)
        self.print_btn.clicked.connect(self.on_print_clicked)

        # wire up Clear Form
        self.clear_btn.clicked.connect(self.clear_form)

    def on_print_clicked(self):
        ticket = self.ticket_input.text().strip()

        if not self.on_pdf_clicked():
            return

        try:
            handler_print.handler_print(ticket)
            log.info(f"Print requested for ticket {ticket}")
        except Exception as e:
            QMessageBox.critical(self, "Print Failed", f"Failed to print ticket {ticket}:\n\n{e}")

    def on_pdf_clicked(self):
        vendor_data = self._gather_vendor_data()
        products_data = self._gather_products_data()
        self.update_revenue_fields()
        self.rev_by_prod.handle_updating(self.product_sections)
        revenue_data = self._gather_revenue_data()

        try:
            if self._validate_required_fields(vendor_data, products_data):
                handler_live_pdf(vendor_data, products_data, revenue_data)
                log.info(f"PDF generated for ticket {vendor_data['ticket_number']}")
                return True
            else:
                log.error("PDF generation for ticket failed")
                return False
        except Exception as e:
            log.error(f"ERROR generating PDF for ticket {vendor_data['ticket_number']}: {e}")
            return False

    def create_record(self):
        """
        :author(s): Joe Lee, Alexander Bubienko
        :purpose: gathers all text inputs and posts to Azure SQL database as a single record
        :return: record ID on success, -1 on error
        """
        try:
            self.update_revenue_fields()
            self.rev_by_prod.handle_updating(self.product_sections)
            self.repaint()
            QApplication.processEvents()

            # Get vendor data
            vendor_data = self._gather_vendor_data()

            # Validate required fields
            if not self._validate_required_fields(vendor_data):
                return -1
            
            # Get products data
            products_data = self._gather_products_data()
        
            # Get revenue data
            revenue_data = self._gather_revenue_data()
        
            # Combine into record data for database
            record_data = {
                'vendor': vendor_data,
                'products': products_data,
                'revenue': revenue_data
            }

            # Post to database
            record_id = self._post_to_database(record_data)

            if record_id != -1:
                self.clear_form()
                status_bar_instance.send_message(f"Record created successfully! ID: {record_id}")
                return record_id
            else:
                log.error("Failed to create record")
                return -1

        except Exception as e:
            log.error(f"Database error: {e}")
            return -1

    def _gather_vendor_data(self):
        """
        :author(s): Alexander Bubienko
        :purpose: Gather vendor field data and convert empty strings to NULL
        :return: Dictionary containing vendor data
        """
        # Vendor information
        vendor_data = {
            'ticket_number': self.ticket_input.text().strip() or "NULL",
            'vendor_id': self.vendor_id_input.text().strip() or "NULL",
            'phone': self.phone_input.text().strip() or "NULL",
            'datetime': self.datetime_input.text().strip() or "NULL",
            'first_name': self.first_name_input.text().strip() or "NULL",
            'middle_name': self.middle_name_input.text().strip() or "NULL",
            'last_name': self.last_name_input.text().strip() or "NULL",
            'address': self.address_input.text().strip() or "NULL",
            'city': self.city_input.text().strip() or "NULL",
            'state': self.state_input.text().strip() or "NULL",
            'zip': int(self.zip_input.text().strip()) if self.zip_input.text().strip() else None
        }
        return vendor_data
    
    def _gather_products_data(self):
        """
        :author(s): Alexander Bubienko
        :purpose: Gather product field data and convert empty strings to NULL
        :return: List of dictionaries containing product data
        """
        # Product information
        products_data = []
        for i, product_section in enumerate(self.product_sections):
            if not product_section['product_id'].text().strip():
                continue

            product_data = {
                'product_id': int(product_section['product_id'].text().strip()) or "NULL",
                'product_type': product_section['product_type'].currentText().strip() or "NULL",
                'product_name': product_section['product_name'].text().strip() or "NULL",
                'notes': product_section['notes'].text().strip() or "",
                'rate': product_section.get('rate').text().strip() if product_section.get('rate') else "NULL",
                'price': self._parse_money(product_section['price'].text()) or 0.0,
                'quantity': int(product_section['quantity'].text().strip()) or "NULL",
                'total': self._parse_money(product_section['total'].text()) or 0.0,
            }
            products_data.append(product_data)
        return products_data

    def _gather_revenue_data(self):
        """
        :purpose: Gather revenue data and convert empty strings to NULL
        :return: Dictionary containing shared revenue and grouped revenue
        :author(s): Alexander Bubienko, Joe Lee
        """
        # Revenue sharing data
        return {
            'shared': self.revenue_generation.get_revenue_data(),
            'grouped': self.rev_by_prod.get_revenue_data(),
            'payout': []
        }

    def _validate_required_fields(self, vendor_data, products_data=None):
        """
        :author(s): Alexander Bubienko, Colin Henderson, Joe Lee
        :purpose: Validate that required fields are filled
        :return: True if all required fields are valid, False otherwise
        """
        if not vendor_data['vendor_id'] or vendor_data['vendor_id'] == "NULL":
            log.error("Error: Vendor ID is required")
            return False

        if products_data is None:
            products_data = self._gather_products_data()

        has_valid_product = False
        for product in products_data:
            if (
                    product['product_id'] and product['product_id'] != "NULL"
                    and
                    product['product_type'] and product['product_type'] != "SELECT"
                    and
                    product['price'] and product['price'] > 0
                    and
                    product['quantity'] and product['quantity'] != "NULL"
            ):
                has_valid_product = True
                break

        if not has_valid_product:
            log.error("Error: At least one product requires Product ID, Product Type, Price, and Quantity")
            return False

        return True

    def _post_to_database(self, record_data):
        """
        :author(s): Alexander Bubienko, Joe Lee
        :purpose: Create documents in both Entities and Consignments containers
        :return: document ID on success, -1 on error
        """
        try:
            entities_container = self.db_connection.connect('Entities')
            consignments_container = self.db_connection.connect('Consignments')

            # Validate vendor_id exists
            vendor_id = record_data['vendor']['vendor_id']
            if not vendor_id or vendor_id == "NULL":
                log.error("Error: No vendor ID provided")
                return -1

            # Create vendor document
            vendor_document = {
                'id': f"vendor_{vendor_id}",
                'partitionKey': f"vendor_{vendor_id}",
                'type': 'vendor',
                'vendor_id': int(vendor_id),
                'phone': record_data['vendor']['phone'],
                'first_name': record_data['vendor']['first_name'],
                'middle_name': record_data['vendor']['middle_name'],
                'last_name': record_data['vendor']['last_name'],
                'address': record_data['vendor']['address'],
                'city': record_data['vendor']['city'],
                'state': record_data['vendor']['state'],
                'zip': record_data['vendor']['zip']
            }

            log.info(f"Creating vendor document with ID: vendor_{vendor_id}")

            try:
                vendor_response = entities_container.upsert_item(body=vendor_document)
                log.info("Vendor document created successfully")
            except Exception as e:
                log.error(f"Error creating vendor document: {e}")
                return -1

            product_ids = []
            for i, product in enumerate(record_data['products']):
                if self._has_product_data(product):
                    product_id = product['product_id']
                    product_name = product['product_name']
                    if not product_id or product_id == "NULL":
                        log.warning(f"Skipping product {i} - no product ID")
                        continue
                    if not product_name or product_name == "NULL":
                        log.error("Error: Product Name is required for all products")
                        return -1

                    rate_value = self._convert_rate(product.get('rate'))
                    if rate_value is None:
                        rate_value = self.rates_container[product.get('product_type')]

                    product_doc = {
                        'id': f"product_{product_id}",
                        'partitionKey': f"product_{product_id}",
                        'type': 'product',
                        'product_id': self._convert_product_id(product_id),
                        'product_name': self._convert_null(product['product_name']),
                        'product_type': self._convert_null(product['product_type']),
                        'rate': rate_value,
                        'total': product['total'],
                    }
                    log.info(f"Creating product document: product_{product_id}")
                    try:
                        product_response = entities_container.upsert_item(body=product_doc)
                        product_ids.append(product_id)
                        log.info(f"Product document created: {product_id}")
                    except Exception as e:
                        log.error(f"Error creating product document {product_id}: {e}")

            ticket_number = record_data['vendor']['ticket_number']
            if not ticket_number or ticket_number == "NULL":
                log.error("Error: No ticket number provided")
                return -1

            consignment_document = {
                'id': f"consignment_{str(ticket_number)}",
                'partitionKey': f"consignment_{str(ticket_number)}",
                'type': 'consignment',
                'ticket_number': int(ticket_number),
                'vendor_id': int(vendor_id),
                'user_id': int(current_user.get_user_id()),
                'datetime': record_data['vendor']['datetime'],
                'status': "OPEN",
                'products': [
                    {
                        'product_id': product['product_id'],
                        'product_type': product['product_type'],
                        'product_name': product['product_name'],
                        'notes': product['notes'],
                        'rate': (
                            self._convert_rate(product.get('rate'))
                            if self._convert_rate(product.get('rate')) is not None
                            else self.rates_container[product.get('product_type')]
                        ),
                        'price': self._convert_null(product['price']),
                        'quantity': self._convert_quantity(product['quantity']),
                        'total': product['total'],
                        'sold': 0,
                        'remaining': self._convert_quantity(product['quantity'])
                    }
                    for product in record_data['products']
                    if self._has_product_data(product)
                    ],
                'revenue': {
                    'shared': record_data['revenue']['shared'],
                    'grouped': record_data['revenue']['grouped'],
                    'payout': record_data['revenue']['payout'],
                }
            }

            log.info(f"Creating consignment document with ID: {ticket_number}")
            try:
                consignment_response = consignments_container.create_item(body=consignment_document)
                log.info("Consignment document created successfully")
            except Exception as e:
                log.error(f"Error creating consignment document: {e}")
                return -1

            success_msg = f"Record created successfully! Ticket: {ticket_number}"
            log.info(success_msg)
            return ticket_number

        except Exception as e:
            error_msg = f"Cosmos DB insertion error: {e}"
            log.error(error_msg)
            import traceback
            traceback.print_exc()
            # self.status_label.setText(f"Error creating record: {str(e)}")
            return -1

    def _convert_product_id(self, product_id_str):
        """
        :author(s): Alexander Bubienko
        :purpose: Convert product ID to be within 0-9999 range for the CHECK constraint
        :return: Valid product ID as integer, or None if invalid
        """
        if product_id_str == "NULL" or not product_id_str:
            return None

        try:
            product_id = int(product_id_str)
            # Ensure it's within the CHECK constraint range (0-9999)
            if 0 <= product_id <= 99999:
                return product_id
            else:
                log.error(f"Product ID {product_id} is outside valid range")
                return None
        except (ValueError, TypeError):
            log.error(f"Invalid product ID: {product_id_str}")
            return None

    def _convert_quantity(self, quantity_str):
        """
        :author(s): Alexander Bubienko
        :purpose: Convert quantity to be within 0-9999 range for the CHECK constraint
        :return: Valid quantity as integer, or None if invalid
        """
        if quantity_str == "NULL" or not quantity_str:
            return None

        try:
            quantity = int(quantity_str)
            # Ensure it's within the CHECK constraint range (0-9999)
            if 0 <= quantity:
                return quantity
            else:
                log.error(f"Quantity {quantity} must be at least 1")
                return None
        except (ValueError, TypeError):
            log.error(f"Invalid quantity: {quantity_str}")
            return None

    def _convert_rate(self, rate_str):
        """
            :purpose: check if rate is in acceptable range
            :return: int
            :author(s): Colin Henderson
        """
        if rate_str is None:
            return None
        if rate_str == "NULL":
            return None
        cleaned = str(rate_str).strip()
        if cleaned == "":
            return None
        try:
            val = int(cleaned)
            if 0 <= val <= 100:
                return val
            log.error(f"Rate {val} outside valid range 0-100")
            return None
        except (ValueError, TypeError):
            log.error(f"Invalid rate: {rate_str}")
            return None

    def _convert_null(self, value):
        """
        :author(s): Alexander Bubienko
        :purpose: Convert "NULL" string to actual None for database NULL
        :return: None if value is "NULL", otherwise the original value
        """
        return None if value == "NULL" else value

    def _has_product_data(self, product):
        """
        :author(s): Alexander Bubienko
        :purpose: Check if product has any data (not all fields are NULL/empty)
        :return: True if product has at least one non-NULL field, False otherwise
        """
        return any(field != "NULL" and field for field in product.values())

    def _has_revenue_data(self, revenue_data):
        """
        :author(s): Alexander Bubienko
        :purpose: Check if revenue data exists
        :return: True if revenue data exists, False otherwise
        """
        return bool(revenue_data)

    def update_ticket_number(self):
        """
        :purpose: updates ticket number
        :return: None
        :author(s): Joe Lee
        """
        ticket_num = str(autogen_ticket_num())
        self.ticket_input.setText(ticket_num)

    def update_datetime(self):
        """
        :purpose: updates datetime
        :return: None
        :author(s): Kyle Valdez
        """
        datetime = str(generate_host_datetime())
        self.datetime_input.setText(datetime)

    def clear_form(self):
        """
        :purpose: clears all input fields, resets the product lines to 2
        :return: None
        :author(s): Joe Lee, Colin Henderson
        """
        self.rev_by_prod.clear()
        self.ticket_input.clear()

        fields = [
            self.vendor_id_input,
            self.phone_input,
            self.first_name_input,
            self.middle_name_input,
            self.last_name_input,
            self.address_input,
            self.city_input,
            self.state_input,
            self.zip_input
        ]
        for field in fields:
            field.clear()
            field.setReadOnly(False)
            field.setObjectName("DEFAULT")
            field.style().unpolish(field)
            field.style().polish(field)
        self.auto_pop_vend()

        # Clear all product fields
        while self.products_layout.count():
            child = self.products_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        self.product_sections.clear()
        self.product_counter = 1
        self.add_product_section()
        self.add_product_section()
        self.revenue_generation.clear_revenue_data()
        status_bar_instance.send_message("Form cleared")
        self.update_ticket_number()

    def _parse_money(self, s: str) -> float:
        """Parse '$1,234.56' / '1234.56' / '' -> float (empty -> 0.0). Raises ValueError if bad."""
        if s is None:
            return 0.0
        cleaned = s.replace("$", "").replace(",", "").strip()
        if cleaned == "":
            return 0.0
        return float(cleaned)

    def _parse_int(self, s: str) -> int:
        """Parse integer quantity (empty -> 0). Raises ValueError if bad."""
        if s is None:
            return 0
        cleaned = s.strip()
        if cleaned == "":
            return 0
        return int(cleaned)

    def _valid_revenue_result(self, res: dict) -> bool:
        """Ensure SXC-22 output has required numeric fields."""
        try:
            return (
                    isinstance(res, dict)
                    and all(k in res for k in ("gross", "vendor", "super_x"))
                    and all(float(res[k]) >= 0 for k in ("gross", "vendor", "super_x"))
            )
        except Exception:
            return False

    def handle_calc_btn(self):
        self.val_prod_sections()
        self.handle_total()
        self.update_revenue_fields()
        self.rev_by_prod.handle_updating(self.product_sections)

    def val_prod_sections(self):
        for prod in self.product_sections:
            if prod['price'] is None:
                log.error("Invalid price")
                return False
            if prod['quantity'] is None:
                log.error("Invalid quantity")
                return False
            if prod['rate'] is None:
                log.error("Invalid rate")
                return False
        return True

    def update_revenue_fields(self) -> int:
        """
        SXC-22 button action:
        - Compute subtotal = sum(price * quantity) across product lines
        - For each row (25/50/75/100%), call RevenueGeneration.calculate_revenues
        - Validate outputs and populate the revenue widget fields
        - Update status; return -1 on any error, 0 on success
        """
        try:
            records = getattr(self.revenue_generation, "revenue_records", None)
            if not records or len(records) != 4:
                log.error("Error: Revenue widget not initialized")
                return -1

            calc = getattr(self.revenue_generation, "calculate_revenues", None)
            if not callable(calc):
                log.error("Error: Revenue calculation method (SXC-22) not found")
                return -1

            #over every percentage sold bracket
            for rec in records:
                subtotal = {'gross': d.Decimal('0.00'), 
                            'vendor': d.Decimal('0.00'), 
                            'super_x': d.Decimal('0.00')}
                #iterate over every product
                for section in self.product_sections:
                    price = self._parse_money(section['price'].text())
                    qty = self._parse_int(section['quantity'].text())
                    #This will catch both empty values and values that don't exist in the table for some reason (i.e somehow someone tries 'Car' product type)
                    try:
                        rate_key = section['product_type'].currentText()
                        rate = self.rates_container[rate_key]
                    except KeyError:
                        log.warning(f"Product type {rate_key} has no matching rate")
                        continue

                    if price < 0 or qty < 0:
                        log.error("Error: Negative price or quantity")
                        return -1
                    
                    pct_label = rec['percentage'].text()
                    #calculate that products revanue contribution at its consignment rate for amount sold
                    result = calc(price, qty, pct_label, rate)

                    if result == -1 or not self._valid_revenue_result(result):
                        log.error(f"Error: Invalid revenue output for {pct_label}")
                        return -1      

                    #Add to totals
                    subtotal['gross'] += result['gross']
                    subtotal['vendor'] += result['vendor']
                    subtotal['super_x'] += result['super_x']

                rec['vendor'].setText(f"${float(subtotal['vendor']):.2f}")
                rec['super_x'].setText(f"${float(subtotal['super_x']):.2f}")

            status_bar_instance.send_message("Revenue fields updated")
            return 0

        except ValueError:
            log.error("Error: Non-numeric price or quantity")
            return -1
        except Exception as e:
            log.error(f"Error calculating revenues: {e}")
            return -1

    def auto_pop_prod(self):
        """
        SXC-136 action:
        - autofill product_id and product_name when product_id exists
        in the Products table
        note - attempting formatting for further use
        return: none
        author: Tyler Slagboom, Joe Lee, Colin Henderson
        """
        try:
            sender = self.sender()
            if not sender:
                return

            for product_section in self.product_sections:
                if product_section['product_id'] is sender:
                    prod_id = product_section['product_id'].text().strip()
                    if not prod_id:
                        return

                    item = get_item("Entities", "product", prod_id)

                    if item:
                        # Product exists - populate and lock
                        if "product_name" in item:
                            product_section['product_name'].setText(item["product_name"])
                            product_section['product_name'].setObjectName("READ_ONLY")
                            product_section['product_name'].setReadOnly(True)
                            product_section['product_name'].style().unpolish(product_section['product_name'])
                            product_section['product_name'].style().polish(product_section['product_name'])
                        if "product_type" in item:
                            index = product_section['product_type'].findText(item["product_type"])
                            if index >= 0:
                                product_section['product_type'].setCurrentIndex(index)
                            product_section['product_type'].setObjectName("READ_ONLY")
                            product_section['product_type'].setEnabled(False)
                            product_section['product_type'].style().unpolish(product_section['product_type'])
                            product_section['product_type'].style().polish(product_section['product_type'])
                        if "product_rate" in product_section:
                            if item and "rate" in item and item["rate"] is not None:
                                product_section['rate'].setText(str(item["rate"]))
                        else:
                         product_section['rate'].setText(str(self.rates_container[item.get("product_type")]) if item else "")

                    else:
                        # Product doesn't exist - clear and unlock
                        product_section['product_name'].setText("")
                        product_section['product_name'].setObjectName("")
                        product_section['product_name'].setReadOnly(False)
                        product_section['product_name'].style().unpolish(product_section['product_name'])
                        product_section['product_name'].style().polish(product_section['product_name'])

                        product_section['product_type'].setCurrentText("SELECT")
                        product_section['product_type'].setObjectName("")
                        product_section['product_type'].setEnabled(True)
                        product_section['product_type'].style().unpolish(product_section['product_type'])
                        product_section['product_type'].style().polish(product_section['product_type'])

                        if 'rate' in product_section:
                            product_section['rate'].setText("Rate")
                    break
        except Exception as e:
            log.error(f"Failed to fetch record: {e}")

    def auto_pop_prod_by_name(self):
        try:
            sender = self.sender()
            if not sender:
                return

            for product_section in self.product_sections:
                if product_section['product_name'] is sender:
                    prod_name = sender.text().strip()
                    if not prod_name:
                        return

                    item = get_item_by_property("Entities", "product", "product_name", prod_name)

                    if item:
                        if "product_id" in item:
                            product_section['product_id'].setText(str(item["product_id"]))
                            product_section['product_id'].setObjectName("READ_ONLY")
                            product_section['product_id'].setReadOnly(True)
                            product_section['product_id'].style().unpolish(product_section['product_id'])
                            product_section['product_id'].style().polish(product_section['product_id'])

                        if "product_type" in item:
                            index = product_section['product_type'].findText(item["product_type"])
                            if index >= 0:
                                product_section['product_type'].setCurrentIndex(index)
                            product_section['product_type'].setObjectName("READ_ONLY")
                            product_section['product_type'].setEnabled(False)
                            product_section['product_type'].style().unpolish(product_section['product_type'])
                            product_section['product_type'].style().polish(product_section['product_type'])

                        if 'rate' in product_section:
                            if "rate" in item and item["rate"] is not None:
                                product_section['rate'].setText(str(item["rate"]))
                            else:
                                product_section['rate'].setText(self.rates_container[item.get("product_type")])
                    else:
                        product_section['product_id'].setObjectName("DEFAULT")
                        product_section['product_id'].setReadOnly(False)
                        product_section['product_id'].style().unpolish(product_section['product_id'])
                        product_section['product_id'].style().polish(product_section['product_id'])

                        product_section['product_type'].setCurrentText("SELECT")
                        product_section['product_type'].setObjectName("DEFAULT")
                        product_section['product_type'].setEnabled(True)
                        product_section['product_type'].style().unpolish(product_section['product_type'])
                        product_section['product_type'].style().polish(product_section['product_type'])

                        product_section['rate'].setObjectName("DEFAULT")
                        product_section['rate'].setText("Rate")
                    break
        except Exception as e:
            log.error(f"Failed to fetch record by name: {e}")

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
                            input_field.setText(str(item[field_name]))
                            input_field.setObjectName("READ_ONLY")
                            input_field.setReadOnly(True)
                else:
                    for input_field in field_mapping.values():
                        input_field.setObjectName("DEFAULT")
                        input_field.setReadOnly(False)
            else:
                for input_field in field_mapping.values():
                    input_field.setObjectName("DEFAULT")
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
                        input_field.setObjectName("DEFAULT")
                        input_field.setReadOnly(False)
            else:
                for input_field in field_mapping.values():
                    input_field.setObjectName("DEFAULT")
                    input_field.setReadOnly(False)

            for input_field in field_mapping.values():
                input_field.style().unpolish(input_field)
                input_field.style().polish(input_field)

        except Exception as e:
            log.error(f"Failed to fetch vendor by phone: {e}")