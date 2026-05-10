from PyQt6.QtCore import Qt
from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtWidgets import QRadioButton
from PyQt6.QtWidgets import QDialog
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
from pathlib import Path
import time
import sys

from src import SPOT

from handlers.handler_pdf import handler_live_pdf
from handlers import handler_print
from services.get_item import get_item
from services.get_all_items_by_property import get_all_items_by_property
from services.get_item_by_property import get_item_by_property
from services.get_max_value import get_max_value
from services.insert_item import insert_item
from src.core import generate_agg_data
from src.user import current_user
from validate.val_check_does_not_exist import val_check_does_not_exists
from ui.tabs.base import BaseTab
from ui.core.autogen_date import generate_host_datetime
from ui.core.revenue_by_product_type import RevenueByProdType
from ui.core.revenue_generation import RevenueGeneration
from ui.core import format_phone
from ui.core import format_price
from ui.core import format_state
from utils.core.export_doc import export_offline_record
from utils.core import generate_excel as xls_gen
from utils.parse_consignment_table import fetch_consignment_data
import validate as VAL

from utils.message_bus import status_bar_instance
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
        self.export_btn = None

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
        self.vendor_id_input.setValidator(QRegularExpressionValidator(QRegularExpression(r"\d{0,4}"), self))
        self.vendor_id_input.returnPressed.connect(self.auto_pop_vend_by_field)
        vendor_section_row_1.addWidget(self.vendor_id_input)

        # Phone Number
        vendor_section_row_1.addWidget(QLabel("Phone Number:"))
        self.phone_input = format_phone.PhoneNumField()
        self.phone_input.setObjectName("DEFAULT")
        self.phone_input.setFixedWidth(150)
        self.phone_input.returnPressed.connect(self.auto_pop_vend_by_field)
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
        self.first_name_input.returnPressed.connect(self.auto_pop_vend_by_field)
        vendor_section_row_2.addWidget(self.first_name_input)

        # Middle Name
        vendor_section_row_2.addWidget(QLabel("Middle Name:"))
        self.middle_name_input = QLineEdit()
        self.middle_name_input.setPlaceholderText("Middle Name")
        self.middle_name_input.setMaxLength(10)
        self.middle_name_input.setMinimumWidth(103)
        self.middle_name_input.setValidator(alpha_validator)
        self.middle_name_input.returnPressed.connect(self.auto_pop_vend_by_field)
        vendor_section_row_2.addWidget(self.middle_name_input)

        # Last Name
        vendor_section_row_2.addWidget(QLabel("Last Name:"))
        self.last_name_input = QLineEdit()
        self.last_name_input.setPlaceholderText("Last Name")
        self.last_name_input.setMaxLength(30)
        self.last_name_input.setMinimumWidth(263)
        self.last_name_input.setValidator(alpha_validator)
        self.last_name_input.returnPressed.connect(self.auto_pop_vend_by_field)
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

        # Add the first three product sections by default
        self.add_product_section()
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
        hr_prod = QFrame()
        hr_prod.setFrameShape(QFrame.Shape.HLine)
        hr_prod.setFrameShadow(QFrame.Shadow.Sunken)
        hr_prod.setObjectName("hr")
        rev_prod_section.addWidget(hr_prod)
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
        hr_rev = QFrame()
        hr_rev.setFrameShape(QFrame.Shape.HLine)
        hr_rev.setFrameShadow(QFrame.Shadow.Sunken)
        hr_rev.setObjectName("hr")
        revenue_section.addWidget(hr_rev)
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

        if SPOT.OFFLINE:
            self.export_btn = QPushButton("Export Record")
            self.export_btn.setObjectName('large_btn')
            action_layout.addWidget(self.export_btn)
        else:
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
            self._make_type_changed_handler(product_section)
        )

        # Add to container
        self.products_layout.addWidget(section_widget)
        self.product_sections.append(product_section)
        self.product_counter += 1
        status_bar_instance.send_message(f"Added product line. Total: {len(self.product_sections)}")

    def _make_type_changed_handler(self, sec):
        """
        :Purpose: Instance Handler
        :Author(s): Colin Heinselman, Colin Henderson
        """
        def handler(_txt):
            """
            :Purpose: Handles product type event
            :Author(s): Colin Heinselman, Colin Henderson
            """
            self._on_product_type_changed(sec)
        return handler

    def handle_total(self):
        """
        :Purpose: Handles price total calculation event
        :Author(s): Joe Lee
        """
        widget = self.sender()
        if not widget:
            return

        section = self.get_sending_widget(widget)
        if section:
            self.on_price_qty_changed(section)

    def get_sending_widget(self, widget):
        """
        :Purpose: Returns the sending widget if it exists
        :Author(s): Joe Lee
        """
        for section in self.product_sections:
            if (section['price'] is widget or section['quantity'] is widget or section['rate'] is widget):
                return section
        return None

    def on_price_qty_changed(self, section):
        """
        :Purpose: Handles price change event
        :Author(s): Joe Lee
        """
        price_text = section['price'].text().strip()
        qty_text = section['quantity'].text().strip()
        rate_text = section['rate'].text().strip().replace('%', '')

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
        """
        :Purpose: Handles product type change event
        :Author(s): Colin Heinselman, Colin Henderson
        """
        try:
            #update any admin changes to table
            self.rates_container = fetch_consignment_data()
            rate_widget = product_section.get('rate')
            type_widget = product_section.get('product_type')
            if not rate_widget or not type_widget:
                log.error("Could not retreive type and rate subwidgets")
                return
            new_rate = self.rates_container[type_widget.currentText()]
            rate_widget.setText(f"{str(new_rate)}%")
        except Exception as e:
            log.error(f"Failed to auto-set rate: {e}")

    def create_removal_handler(self, widget, product_section):
        """
        :Purpose: Handles product line removal
        :Author(s): Joe Lee
        """
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
        """
        :Purpose: Displays a warning pop up to confirm the user wants to remove the product line
        :Author(s): Joe Lee
        """
        product_id = product_section['product_id'].text().strip()
        product_name = product_section['product_name'].text().strip()

        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Warning - Product Line Removal")
        msg_box.setText(f"Are you sure you want to remove this product line?\n{product_id} - {product_name}")
        cancel_btn = msg_box.addButton("Cancel", QMessageBox.ButtonRole.NoRole)
        confirm_btn = msg_box.addButton("Confirm", QMessageBox.ButtonRole.NoRole)
        msg_box.setDefaultButton(confirm_btn)

        msg_box.exec()
        return msg_box.clickedButton() == confirm_btn

    def gather_record(self):
        """
        :Purpose: Gathers consignment data from the tab
        :Author(s): Maksym Komarov
        """
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
        """
        :Purpose: Handles excel button via a sequence of events
        :Author(s): Maksym Komarov
        """
        self.handle_calc_btn()
        data = self.gather_record()
        xls_gen.generate_excel(data)

    def setup_button_connections(self):
        """
        :purpose: links buttons with methods
        :return: None
        :author(s): Joe Lee
        """
        if self.create_btn:
            self.create_btn.clicked.connect(self.create_record)
        if self.export_btn:
            self.export_btn.clicked.connect(self.export_record)
        self.clear_btn.clicked.connect(self.clear_form)
        self.add_product_btn.clicked.connect(self.add_product_section)
        self.calc_btn.clicked.connect(self.handle_calc_btn)
        self.excel_btn.clicked.connect(self.handle_excel_btn)
        self.pdf_btn.clicked.connect(self.on_pdf_clicked)
        self.print_btn.clicked.connect(self.on_print_clicked)

    def on_print_clicked(self):
        """
        :Purpose: Handles print button via a sequence of events
        :Author(s): Joe Lee
        """
        ticket = self.ticket_input.text().strip()

        if not self.on_pdf_clicked():
            return

        if not self._wait_for_pdf(ticket):
            QMessageBox.critical(self, "Print Failed", f"PDF for ticket {ticket} was not ready in time.")
            return

        try:
            handler_print.handler_print(ticket)
            log.info(f"Print requested for ticket {ticket}")
            QMessageBox.information(self, "PDF Generation Succeeded", f"Ticket {ticket} successfully requested to print")
        except Exception as e:
            QMessageBox.critical(self, "Print Failed", f"Failed to print ticket {ticket}:\n\n{e}")

    def on_pdf_clicked(self):
        """
        :Purpose: Handles pdf button via a sequence of events
        :Author(s): Joe Lee
        """
        vendor_data = self._gather_vendor_data()
        if vendor_data is None:
            log.warning("PDF generation skipped: No Vendor data found")
            return False

        products_data = self._gather_products_data()
        if products_data is None:
            log.warning("PDF generation skipped: No Products data found")
            return False

        self.update_revenue_fields()
        self.rev_by_prod.handle_updating(self.product_sections)
        revenue_data = self._gather_revenue_data()
        ticket_number = self.ticket_input.text().strip()
        datetime = self.datetime_input.text().strip()

        try:
            handler_live_pdf(ticket_number, vendor_data, products_data, revenue_data, datetime)
            log.info(f"PDF generated for Ticket {ticket_number}")
            QMessageBox.information(self, "PDF Generation Succeeded",
                                    f"Ticket {ticket_number} successfully generated a PDF")
            return True
        except Exception as e:
            log.error(f"PDF generation failed: {e}")
            QMessageBox.information(self, "PDF Generation Failed", f"Failed to generate a PDF")
            return False

    def _wait_for_pdf(self, ticket, timeout=10, interval=0.2):
        """
        :Purpose: Polls for the PDF file to exist before proceeding to print
        :Author(s): Joe Lee
        """
        current_dir = Path(sys.executable).parent if getattr(sys, 'frozen', False) else (Path(__file__).parent.parent.parent / "utils")
        tickets_dir = current_dir / "tickets"
        pdf_path = tickets_dir / f"{ticket}.pdf"
        elapsed = 0.0
        while elapsed < timeout:
            if pdf_path.exists():
                return True
            time.sleep(interval)
            elapsed += interval

        log.error(f"Timed out waiting for PDF: {pdf_path}")
        return False

    def _gather_ticket_number(self):
        """
        :Purpose: Gets the ticket number
        :Author(s): Joe Lee
        """
        raw_ticket = self.ticket_input.text().strip()
        ticket_number = int(raw_ticket) if raw_ticket else None
        if not ticket_number:
            log.error("Ticket number is required")
            return None
        return ticket_number

    def _gather_vendor_data(self):
        """
        :Purpose: Gathers the input data for vendor
        :Author(s): Alexander Bubienko, Joe Lee
        """
        raw_vendor_id = self.vendor_id_input.text().strip()
        vendor_id = int(raw_vendor_id) if raw_vendor_id else None

        if VAL.val_vendor_id(vendor_id):
            validated_vendor_id = vendor_id
        else:
            validated_vendor_id = None
            self._flag_error(self.vendor_id_input)
            log.error("Invalid Vendor ID")
            return None

        phone = self.phone_input.text().strip() or None
        if VAL.val_phone_number(phone):
            validated_phone_number = phone
        else:
            validated_phone_number = None
            self._flag_error(self.phone_input)
            log.error("Invalid Phone Number")
            return None

        fname = self.first_name_input.text().strip() or None
        if VAL.val_fl_name(fname):
            validated_first_name = fname
        else:
            validated_first_name = None
            self._flag_error(self.first_name_input)
            log.error("Invalid First Name")
            return None

        mname = self.middle_name_input.text().strip() or None
        if VAL.val_m_name(mname):
            validated_middle_name = mname
        else:
            validated_middle_name = None
            self._flag_error(self.middle_name_input)
            log.error("Invalid Middle Name")
            return None

        lname = self.last_name_input.text().strip() or None
        if VAL.val_fl_name(lname):
            validated_last_name = lname
        else:
            validated_last_name = None
            self._flag_error(self.last_name_input)
            log.error("Invalid Last Name")
            return None

        address = self.address_input.text().strip() or None
        if VAL.val_address(address):
            validated_address = address
        else:
            validated_address = None
            self._flag_error(self.address_input)
            log.error("Invalid Address")
            return None

        city = self.city_input.text().strip() or None
        if VAL.val_city(city):
            validated_city = city
        else:
            validated_city = None
            self._flag_error(self.city_input)
            log.error("Invalid City")
            return None

        state = self.state_input.text().strip() or None
        if VAL.val_state(state):
            validated_state = state
        else:
            validated_state = None
            self._flag_error(self.state_input)
            log.error("Invalid State")
            return None

        zip = int(self.zip_input.text().strip()) if self.zip_input.text().strip() else None
        if VAL.val_zip(zip):
            validated_zip = zip
        else:
            validated_zip = None
            self._flag_error(self.zip_input)
            log.error("Invalid Zip")
            return None

        return {
            'vendor_id': validated_vendor_id,
            'phone': validated_phone_number,
            'first_name': validated_first_name,
            'middle_name': validated_middle_name,
            'last_name': validated_last_name,
            'address': validated_address,
            'city': validated_city,
            'state': validated_state,
            'zip': validated_zip
        }

    def _gather_revenue_data(self):
        """
        :Purpose: Gathers revenue data
        :Author(s): Alexander Bubienko, Joe Lee
        """
        return {
            'shared': self.revenue_generation.get_revenue_data(),
            'grouped': self.rev_by_prod.get_revenue_data(),
            'payout': []
        }

    def _gather_products_data(self):
        """
        :Purpose: Gathers products data
        :Author(s): Alexander Bubienko, Joe Lee
        """
        products = []
        has_valid_product = False
        for section in self.product_sections:
            if self.check_empty_prod_section(section):
                continue
            product_id = self._convert_product_id(section['product_id'].text().strip())
            if VAL.val_product_id(product_id):
                validated_product_id = product_id
            else:
                validated_product_id = None
                self._flag_error(section['product_id'])
                log.error(f"Invalid product id: {product_id}")
                return None

            product_type = section['product_type'].currentText().strip() or None
            if VAL.val_product_type(product_type):
                validated_product_type = product_type
            else:
                validated_product_type = None
                self._flag_error(section['product_type'])
                section['product_type'].showPopup()
                log.error(f"Invalid product type: {product_type}")
                return None

            product_name = section['product_name'].text().strip() or None
            if VAL.val_product_name(product_name):
                validated_product_name = product_name
            else:
                validated_product_name = None
                self._flag_error(section['product_name'])
                log.error(f"Invalid product name: {product_name}")
                return None

            rate = self._convert_rate(section['rate'].text().strip())
            if rate is None:
                rate = self.rates_container.get(product_type)
            if VAL.val_rate(rate):
                validated_rate = rate
            else:
                validated_rate = None
                self._flag_error(section['rate'])
                log.error(f"Invalid rate: {rate}")
                return None

            price = self._parse_money(section['price'].text())
            if VAL.val_price(price):
                validated_price = price
            else:
                validated_price = None
                self._flag_error(section['price'])
                log.error(f"Invalid price: {price}")
                return None

            quantity = self._convert_quantity(section['quantity'].text().strip())
            if VAL.val_quantity(quantity):
                validated_quantity = quantity
            else:
                validated_quantity = None
                self._flag_error(section['quantity'])
                log.error(f"Invalid quantity: {quantity}")
                return None

            has_valid_product = True
            products.append({
                'product_id': validated_product_id,
                'product_type': validated_product_type,
                'product_name': validated_product_name,
                'notes': section['notes'].text().strip() or "",
                'rate': validated_rate,
                'price': validated_price,
                'quantity': validated_quantity,
                'total': self._parse_money(section['total'].text()),
                'sold': 0,
                'remaining': validated_quantity,
            })

        if not has_valid_product:
            log.error("All product sections are empty")
            self._flag_error(self.product_sections[0]['product_id'])
            return None

        return products

    def _gather_consignment_data(self, vendor_data, products_data, revenue_data):
        """
        :Purpose: Gathers all consignment data
        :Author(s): Alexander Bubienko, Joe Lee
        """
        raw_ticket = self.ticket_input.text().strip()
        if not raw_ticket:
            log.error("Ticket number is required")
            return None
        ticket_number = raw_ticket if SPOT.OFFLINE else int(raw_ticket)

        return {
            'consignment_id': ticket_number,
            'vendor_id': vendor_data['vendor_id'],
            'user_id': current_user.get_user_id(),
            'datetime': self.datetime_input.text().strip(),
            'status': "OPEN",
            'products': products_data,
            'revenue': revenue_data
        }

    def _post_to_database(self, vendor_data, products_data, revenue_data):
        """
        :Purpose: Uploads gathered data to database
        :Author(s): Alexander Bubienko, Joe Lee
        """
        try:
            if val_check_does_not_exists("Entities", "vendor", "vendor_id", vendor_data['vendor_id']):
                if insert_item("Entities", "vendor", vendor_data) == -1:
                    log.error(f"Failed to insert vendor {vendor_data['vendor_id']}")
                    return -1
            else:
                log.info(f"Vendor {vendor_data['vendor_id']} already exists, skipping")

            for product in products_data:
                if val_check_does_not_exists("Entities", "product", "product_id", product['product_id']):
                    product_doc = dict(product)
                    product_doc['rate'] = ''
                    if insert_item("Entities", "product", product_doc) == -1:
                        log.error(f"Failed to insert product {product['product_id']}")
                        continue
                else:
                    log.info(f"Product {product['product_id']} already exists, skipping")

            consignment = self._gather_consignment_data(vendor_data, products_data, revenue_data)
            if consignment is None:
                return -1

            if insert_item("Consignments", "consignment", consignment) == -1:
                log.error(f"Failed to insert consignment {consignment['consignment_id']}")
                return -1

            log.info(f"Record created successfully! Ticket: {consignment['consignment_id']}")
            return consignment['consignment_id']

        except Exception as e:
            log.error(f"Cosmos DB insertion error: {e}")
            return -1

    def create_record(self):
        """
        :purpose: gathers all text inputs and posts to Cosmos database as a single record
        :return: record ID on success, -1 on error
        :author(s): Joe Lee, Alexander Bubienko
        """
        try:
            self.update_revenue_fields()
            self.rev_by_prod.handle_updating(self.product_sections)
            self.repaint()
            QApplication.processEvents()

            vendor_data = self._gather_vendor_data()
            if vendor_data is None:
                return -1

            products_data = self._gather_products_data()
            if products_data is None:
                return -1

            revenue_data = self._gather_revenue_data()

            record_id = self._post_to_database(vendor_data, products_data, revenue_data)

            if record_id != -1:
                self.on_print_clicked()
                self.clear_form()
                status_bar_instance.send_message(f"Ticket created successfully! Ticket Number: {record_id}")
                return record_id
            else:
                log.error("Failed to create record")
                return -1

        except Exception as e:
            log.error(f"Database error: {e}")
            return -1

    def export_record(self):
        """
        :purpose: Exports all record docs into a json file (only if SPOT.OFFLINE)
        :author(s): Joe Lee
        """
        try:
            self.update_revenue_fields()
            self.rev_by_prod.handle_updating(self.product_sections)

            vendor_data = self._gather_vendor_data()
            if vendor_data is None:
                return

            products_data = self._gather_products_data()
            if products_data is None:
                return

            revenue_data = self._gather_revenue_data()
            consignment_data = self._gather_consignment_data(vendor_data, products_data, revenue_data)
            if consignment_data is None:
                return

            ticket_number = consignment_data['consignment_id']
            export_offline_record(ticket_number, vendor_data, products_data, consignment_data)
            self.clear_form()
            status_bar_instance.send_message(f"Offline record exported: {ticket_number}")
            QMessageBox.information(self, "Export Succeeded", f"Ticket {ticket_number} exported successfully")

        except Exception as e:
            log.error(f"Export failed: {e}")
            QMessageBox.critical(self, "Export Failed", f"Failed to export record:\n\n{e}")

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
        cleaned = str(rate_str).strip().replace('%', '')
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
        if SPOT.OFFLINE:
            offline_dir = Path(__file__).parent.parent.parent / "utils" / "OFFLINE_tickets"
            max_num = 0
            if offline_dir.exists():
                for file in offline_dir.iterdir():
                    if file.stem.startswith("OFFLINE_"):
                        try:
                            num = int(file.stem.split('_')[1])
                            if num > max_num:
                                max_num = num
                        except ValueError:
                            continue
            self.ticket_input.setText(f"OFFLINE_{max_num + 1}")
        else:
            max = get_max_value("Consignments", "consignment_id")
            self.ticket_input.setText(str(int(max) + 1))

    def update_datetime(self):
        """
        :purpose: updates datetime
        :return: None
        :author(s): Kyle Valdez
        """
        datetime = str(generate_host_datetime())
        if VAL.val_datetime(datetime):
            validated_datetime = datetime
            self.datetime_input.setText(validated_datetime)
        else:
            self.datetime_input.setText(datetime)
            log.error(f"Failed to generate a valid datetime: {datetime}")

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

        self.phone_input.clear_phone()

        # Clear all product fields
        while self.products_layout.count():
            child = self.products_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        self.product_sections.clear()
        self.product_counter = 1
        self.add_product_section()
        self.add_product_section()
        self.add_product_section()
        self.revenue_generation.clear_revenue_data()
        status_bar_instance.send_message("Form cleared")
        self.update_ticket_number()

    def _parse_money(self, s: str) -> float:
        """
        Parse '$1,234.56' / '1234.56' / '' -> float (empty -> 0.0). Raises ValueError if bad.
        Purpose: Parse strings to make sure valid integer or float
        Return: float/int and True when checking for valid inputs, None/0 for error and False for invalid inputs
        Author: Kyle Valdez

        """
        if s is None:
            log.error(f"Invalid price: {s} is None")
            return None
        cleaned = s.replace("$", "").replace(",", "").strip()
        if cleaned == "":
            log.error(f"Invalid price: {s} is Empty")
            return None
        return float(cleaned)

    def _parse_int(self, s: str) -> int:
        """
        :Purpose: Parse integer quantity (empty -> 0). Raises ValueError if bad
        :Author(s): Kyle Valdez
        """
        if s is None:
            return 0
        cleaned = s.strip()
        if cleaned == "":
            return 0
        return int(cleaned)

    def _valid_revenue_result(self, res: dict) -> bool:
        """
        :Purpose: Checks if the revenue is valid
        :Author(s): Kyle Valdez
        """
        try:
            return (
                    isinstance(res, dict)
                    and all(k in res for k in ("gross", "vendor", "super_x"))
                    and all(float(res[k]) >= 0 for k in ("gross", "vendor", "super_x"))
            )
        except Exception:
            return False

    def handle_calc_btn(self):
        """
        :Purpose: Handles the calculate event via a sequence of events
        :Author(s): Joe Lee
        """
        if not self.val_prod_sections():
            return
        self.handle_total()
        self.update_revenue_fields()
        self.rev_by_prod.handle_updating(self.product_sections)

    def check_empty_prod_section(self, prod_section):
        """
        :Purpose: Checks if the prod_section is empty to skip
        :Author(s): Joe Lee
        """
        empty = (prod_section['product_id'].text().strip() == ''
                 and prod_section['product_name'].text().strip() == ''
                 and prod_section['product_type'].currentIndex() == -1
                 and prod_section['rate'].text().strip() == ''
                 and prod_section['price'].text().strip() == ''
                 and prod_section['quantity'].text().strip() == '')
        return empty

    def val_prod_sections(self):
        """
        :Purpose: Validates a product section is populated correctly
        :Author(s): Joe Lee
        """
        has_valid = False
        for prod in self.product_sections:
            if self.check_empty_prod_section(prod):
                continue
            has_valid = True
            if prod['product_id'].text().strip() == '':
                log.error(f"Please enter a product id")
                self._flag_error(prod['product_id'])
                return False
            else:
                if prod['product_type'].currentIndex() == -1:
                    log.error(f"Please enter a product type")
                    self._flag_error(prod['product_type'])
                    prod['product_type'].showPopup()
                    return False
                if prod['price'].text().replace('$', '').strip() == '':
                    log.error(f"Please enter a price")
                    self._flag_error(prod['price'])
                    return False
                if prod['quantity'].text().strip() == '':
                    log.error(f"Please enter a quantity")
                    self._flag_error(prod['quantity'])
                    return False
                if prod['rate'].text().replace('%', '').strip() == '':
                    log.error(f"Error: Failed to sync rate")
                    self._flag_error(prod['rate'])
                    return False
        if not has_valid:
            log.info(f"No products to calculate")
            return False
        return True

    def update_revenue_fields(self) -> int:
        """
        Purpose: Compute subtotal = sum(price * quantity) across product lines and validate outputs and populate the revenue widget fields
        Return: -1 on any error, 0 on success
        Author: Kyle Valdez
        """
        try:
            records = getattr(self.revenue_generation, "revenue_records", None)
            if not records or len(records) != 4:
                log.error("Error: Revenue widget not initialized")
                return -1

            calc = getattr(self.revenue_generation, "calculate_revenues", None)
            if not callable(calc):
                log.error("Error: Revenue calculation method not found")
                return -1

            #over every percentage sold bracket
            for rec in records:
                subtotal = {'gross': d.Decimal('0.00'), 
                            'vendor': d.Decimal('0.00'), 
                            'super_x': d.Decimal('0.00')}
                #iterate over every product
                for section in self.product_sections:
                    if self.check_empty_prod_section(section):
                        continue
                    price = self._parse_money(section['price'].text())
                    qty = self._parse_int(section['quantity'].text())
                    #This will catch both empty values and values that don't exist in the table for some reason (i.e somehow someone tries 'Car' product type)
                    try:
                        rate_key = section['product_type'].currentText()
                        rate = self.rates_container[rate_key]
                    except KeyError:
                        log.warning(f"Product type {rate_key} has no matching rate")
                        continue

                    if price < 0:
                        log.error(f"Error: Negative price: {price}")
                        return -1

                    if qty < 0:
                        log.error(f"Error: Negative quantity: {qty}")
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
        - autofill product_id and product_name when product_id exists
        in the Products table
        note - attempting formatting for further use
        return: none
        author: Tyler Slagboom, Joe Lee, Colin Henderson
        """
        if SPOT.OFFLINE:
            log.error(f"Unable to autopopulate product fields using product id. Not connected to the database.")
            return
        try:
            sender = self.sender()
            if not sender:
                return

            for product_section in self.product_sections:
                if product_section['product_id'] is sender:
                    prod_id = product_section['product_id'].text().strip()
                    if not prod_id:
                        product_section['product_name'].clear()
                        product_section['product_name'].setObjectName("DEFAULT")
                        product_section['product_name'].setReadOnly(False)
                        product_section['product_name'].style().unpolish(product_section['product_name'])
                        product_section['product_name'].style().polish(product_section['product_name'])

                        product_section['product_type'].setCurrentIndex(-1)
                        product_section['product_type'].setObjectName("DEFAULT")
                        product_section['product_type'].setEnabled(True)
                        product_section['product_type'].style().unpolish(product_section['product_type'])
                        product_section['product_type'].style().polish(product_section['product_type'])
                        return

                    item = get_item("Entities", "product", prod_id)

                    if item:
                        log.info(f"Autopopulating with found product id {prod_id}")
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
                    else:
                        log.info(f"Did not find existing product with id {prod_id}")
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
                    break
        except Exception as e:
            log.error(f"Failed to fetch record: {e}")

    def auto_pop_prod_by_name(self):
        """
        :Purpose: Autopopulates a product section using the input product name
        :Author(s): Joe Lee
        """
        if SPOT.OFFLINE:
            log.error(f"Unable to autopopulate product fields using product name. Not connected to the database.")
        try:
            sender = self.sender()
            if not sender:
                return

            for product_section in self.product_sections:
                if product_section['product_name'] is sender:
                    prod_name = sender.text().strip()
                    if not prod_name:
                        product_section['product_id'].clear()
                        product_section['product_id'].setObjectName("DEFAULT")
                        product_section['product_id'].setReadOnly(False)
                        product_section['product_id'].style().unpolish(product_section['product_id'])
                        product_section['product_id'].style().polish(product_section['product_id'])

                        product_section['product_type'].setCurrentIndex(-1)
                        product_section['product_type'].setObjectName("DEFAULT")
                        product_section['product_type'].setEnabled(True)
                        product_section['product_type'].style().unpolish(product_section['product_type'])
                        product_section['product_type'].style().polish(product_section['product_type'])
                        return

                    item = get_item_by_property("Entities", "product", "product_name", prod_name)

                    if item:
                        log.info(f"Autopopulating with found product name {prod_name}")
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
                    else:
                        log.info(f"Did not find existing product with name {prod_name}")
                        product_section['product_id'].setObjectName("DEFAULT")
                        product_section['product_id'].setReadOnly(False)
                        product_section['product_id'].style().unpolish(product_section['product_id'])
                        product_section['product_id'].style().polish(product_section['product_id'])

                        product_section['product_type'].setCurrentText("SELECT")
                        product_section['product_type'].setObjectName("DEFAULT")
                        product_section['product_type'].setEnabled(True)
                        product_section['product_type'].style().unpolish(product_section['product_type'])
                        product_section['product_type'].style().polish(product_section['product_type'])
                    break
        except Exception as e:
            log.error(f"Failed to fetch record by name: {e}")

    def auto_pop_vend_by_field(self):
        """
        :Purpose: Autopopulates the vendor section via the vendor id input
        :Author(s): Joe Lee
        """
        if SPOT.OFFLINE:
            log.error("Unable to autopopulate vendor fields. Not connected to the database.")
            return

        try:
            sender = self.sender()
            if not sender:
                return

            field_map = {
                self.vendor_id_input: "vendor_id",
                self.phone_input: "phone",
                self.first_name_input: "first_name",
                self.middle_name_input: "middle_name",
                self.last_name_input: "last_name",
            }

            db_field = field_map.get(sender)
            if not db_field:
                return

            populate_fields = {
                'vendor_id': self.vendor_id_input,
                'phone': self.phone_input,
                'first_name': self.first_name_input,
                'middle_name': self.middle_name_input,
                'last_name': self.last_name_input,
                'address': self.address_input,
                'city': self.city_input,
                'state': self.state_input,
                'zip': self.zip_input,
            }

            value = sender.text().strip()
            if db_field == "vendor_id":
                value = int(value)

            if not value:
                for input_field in populate_fields.values():
                    if input_field is not sender:
                        input_field.clear()
                    input_field.setObjectName("DEFAULT")
                    input_field.setReadOnly(False)
                for input_field in populate_fields.values():
                    input_field.style().unpolish(input_field)
                    input_field.style().polish(input_field)
                return

            result = get_all_items_by_property("Entities", "vendor", db_field, value)

            if result is not None:
                if isinstance(result, list):
                    item = self.prompt_vendor_selection(result)
                    if item is None:
                        return
                else:
                    item = result

                log.info(f"Autopopulating Vendor fields using {db_field}: {value}")
                for field_name, input_field in populate_fields.items():
                    if field_name in item:
                        input_field.setText(str(item[field_name]))
                        if input_field is not sender:
                            input_field.setObjectName("READ_ONLY")
                            input_field.setReadOnly(True)
            else:
                log.info(f"No vendor found with {db_field}: {value}")
                for input_field in populate_fields.values():
                    if input_field is not sender:
                        input_field.clear()
                    input_field.setObjectName("DEFAULT")
                    input_field.setReadOnly(False)

            for input_field in populate_fields.values():
                input_field.style().unpolish(input_field)
                input_field.style().polish(input_field)

        except Exception as e:
            log.error(f"Failed to fetch vendor by {db_field}: {e}")

    def prompt_vendor_selection(self, vendors):
        """
        :Purpose: Opens a dialog when multiple vendors are found with the same input value
        :Author(s): Joe Lee
        """
        dialog = QDialog(self)
        dialog.setWindowTitle("Multiple Vendors Found")
        dialog.setModal(True)

        layout = QVBoxLayout()

        label = QLabel("Select a vendor:")
        layout.addWidget(label)
        hr0 = QFrame()
        hr0.setFrameShape(QFrame.Shape.HLine)
        hr0.setFrameShadow(QFrame.Shadow.Sunken)
        hr0.setObjectName("hr")
        layout.addWidget(hr0)

        radio_buttons = []
        for vend in vendors:
            v_id = vend.get('vendor_id', '')
            fname = vend.get('first_name', '')
            mname = vend.get('middle_name', '')
            lname = vend.get('last_name', '')
            address = vend.get('address', '')
            radio_btn = QRadioButton(f"{v_id} : {fname} {mname} {lname}\n"
                                     f"{address}")
            radio_buttons.append(radio_btn)
            layout.addWidget(radio_btn)
            hr = QFrame()
            hr.setFrameShape(QFrame.Shape.HLine)
            hr.setFrameShadow(QFrame.Shadow.Sunken)
            hr.setObjectName("hr")
            layout.addWidget(hr)

        if radio_buttons:
            radio_buttons[0].setChecked(True)

        cancel_btn = QPushButton("Cancel")
        layout.addWidget(cancel_btn)

        confirm_btn = QPushButton("Confirm")
        layout.addWidget(confirm_btn)

        selected = [None]

        def on_confirm():
            """
            :Purpose: Handles the confirmation button in the vendor dialog
            :Author(s): Joe Lee
            """
            for i, rb in enumerate(radio_buttons):
                if rb.isChecked():
                    selected[0] = vendors[i]
                    break
            dialog.accept()

        confirm_btn.clicked.connect(on_confirm)

        dialog.setLayout(layout)

        if dialog.exec() == QDialog.DialogCode.Accepted and selected[0] is not None:
            return selected[0]
        return None

    def _flag_error(self, field):
        """
        :Purpose: sets the calling field to red on failed validation or error call
        :Author(s): Joe Lee
        """
        self._error_field = field
        field.setStyleSheet("background-color: #691601;")
        field.style().unpolish(field)
        field.style().polish(field)
        field.setFocus()
        if hasattr(field, 'selectAll'):
            field.selectAll()
        QTimer.singleShot(2000, self._clear_field_error)

    def _clear_field_error(self):
        """
        :Purpose: resets the calling field's style back to default
        :Author(s): Joe Lee
        """
        self._error_field.setStyleSheet("")
        self._error_field.style().unpolish(self._error_field)
        self._error_field.style().polish(self._error_field)