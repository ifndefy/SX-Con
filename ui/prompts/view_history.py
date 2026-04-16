from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtWidgets import QHBoxLayout
from PyQt6.QtWidgets import QLabel
from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtWidgets import QFrame
from PyQt6.QtWidgets import QWidget
from PyQt6.QtWidgets import QMessageBox

from services.get_item import get_item
from services.get_property import get_property
from handlers.handler_pdf import handler_live_pdf
from handlers.handler_print import handler_print
from utils.core import generate_excel as xls_gen

import utils.logger.logger as log


class ViewPayoutHistory(QDialog):
    def __init__(self, parent, payout_list, consignment_id):
        super().__init__(parent)
        self.payout_list = payout_list
        self.consignment_id = consignment_id
        self.setFixedWidth(600)
        self.setWindowTitle("Payout History")
        self.setup_ui()

    def setup_ui(self):
        """
        :purpose: builds the payout history dialog with collapsible cards
        :author(s): Joe Lee
        """
        dialog_layout = QVBoxLayout(self)

        if not self.payout_list:
            no_data = QLabel("No payouts yet")
            no_data.setAlignment(Qt.AlignmentFlag.AlignCenter)
            dialog_layout.addWidget(no_data)
        else:
            for i in reversed(range(len(self.payout_list))):
                entry = self.payout_list[i]
                card = self._make_entry(i + 1, i, entry)
                dialog_layout.addWidget(card)

                if i > 0:
                    hr = QFrame()
                    hr.setFrameShape(QFrame.Shape.HLine)
                    hr.setFrameShadow(QFrame.Shadow.Sunken)
                    hr.setObjectName("hr")
                    dialog_layout.addWidget(hr)

        self.adjustSize()

    def _make_entry(self, number, payout_index, payout_data):
        """
        :purpose: builds a collapsible payout entry with date, product rows, totals, and export buttons
        :author(s): Joe Lee
        """
        entry = QFrame()
        entry.setFrameShape(QFrame.Shape.NoFrame)
        layout = QVBoxLayout(entry)
        layout.setContentsMargins(5, 5, 5, 5)

        # Always visible row
        top_layout = QHBoxLayout()

        header = QLabel(f"Payout #{number}")
        header.setObjectName("post_title")
        header.setStyleSheet("font-weight: bold;")
        top_layout.addWidget(header)

        top_layout.addStretch()

        top_layout.addWidget(QLabel("Date:"))
        date_field = QLineEdit(payout_data.get('datetime', 'N/A'))
        date_field.setReadOnly(True)
        date_field.setObjectName("READ_ONLY")
        date_field.setFixedWidth(195)
        top_layout.addWidget(date_field)

        top_layout.addStretch()

        expand_btn = QPushButton("View")
        top_layout.addWidget(expand_btn)

        layout.addLayout(top_layout)

        # Collapsible content
        details = QWidget()
        details.setObjectName("view_bg")
        details.setVisible(False)
        details_layout = QVBoxLayout(details)
        details_layout.setContentsMargins(5, 5, 5, 5)

        issuer_layout = QHBoxLayout()
        issuer_layout.addWidget(QLabel("Issuer:"))
        issuer_input = QLineEdit(payout_data.get('user', 'Unknown'))
        issuer_input.setReadOnly(True)
        issuer_input.setObjectName("READ_ONLY")
        issuer_input.setFixedWidth(200)
        issuer_layout.addWidget(issuer_input)
        issuer_layout.addStretch()
        details_layout.addLayout(issuer_layout)

        products = payout_data.get('products', [])
        for prod in products:
            row_layout = QHBoxLayout()

            row_layout.addWidget(QLabel("ID:"))
            product_id = QLineEdit(str(prod.get('product_id', '')))
            product_id.setReadOnly(True)
            product_id.setObjectName("READ_ONLY")
            product_id.setFixedWidth(60)
            row_layout.addWidget(product_id)

            product_name = prod.get('product_name', '')
            if not product_name:
                product_name = get_property("Entities", "product_name", "product", prod.get('product_id'))
                if product_name == "-1":
                    product_name = ''

            row_layout.addWidget(QLabel("Name:"))
            product_name = QLineEdit(product_name)
            product_name.setReadOnly(True)
            product_name.setObjectName("READ_ONLY")
            product_name.setFixedWidth(150)
            row_layout.addWidget(product_name)

            row_layout.addWidget(QLabel("Sold:"))
            qty_sold_output = QLineEdit(str(prod.get('sold', 0)))
            qty_sold_output.setReadOnly(True)
            qty_sold_output.setObjectName("READ_ONLY")
            qty_sold_output.setFixedWidth(40)
            row_layout.addWidget(qty_sold_output)

            row_layout.addWidget(QLabel("Payout:"))
            vendor_payout_output = QLineEdit(f"${prod.get('vendor', 0):.2f}")
            vendor_payout_output.setReadOnly(True)
            vendor_payout_output.setObjectName("READ_ONLY")
            vendor_payout_output.setFixedWidth(80)
            row_layout.addWidget(vendor_payout_output)
            details_layout.addLayout(row_layout)

        totals_layout = QHBoxLayout()
        excel_btn = QPushButton("Excel")
        excel_btn.setProperty("payout_index", payout_index)
        excel_btn.clicked.connect(self._handle_entry_excel)
        totals_layout.addWidget(excel_btn)

        pdf_btn = QPushButton("PDF")
        pdf_btn.setProperty("payout_index", payout_index)
        pdf_btn.clicked.connect(self._handle_entry_pdf)
        totals_layout.addWidget(pdf_btn)

        print_btn = QPushButton("Print")
        print_btn.setProperty("payout_index", payout_index)
        print_btn.clicked.connect(self._handle_entry_print)
        totals_layout.addWidget(print_btn)

        totals_layout.addStretch()

        totals_layout.addWidget(QLabel("Payout Total:"))
        total_payout_output = QLineEdit(f"${payout_data.get('vendor', 0):.2f}")
        total_payout_output.setReadOnly(True)
        total_payout_output.setObjectName("READ_ONLY")
        total_payout_output.setFixedWidth(100)
        totals_layout.addWidget(total_payout_output)
        details_layout.addLayout(totals_layout)

        layout.addWidget(details)

        def toggle():
            visible = details.isVisible()
            details.setVisible(not visible)
            expand_btn.setText("Hide" if not visible else "View")
            entry.adjustSize()
            self.layout().activate()
            self.resize(600, self.layout().sizeHint().height())

        expand_btn.clicked.connect(toggle)

        return entry

    def _get_payout_ticket_data(self, payout_index):
        """
        :purpose: fetches consignment and vendor data, slices payout list up to payout_index
        :return: (consignment, vendor_data, revenue_data) or (None, None, None) on failure
        :author(s): Joe Lee
        """
        consignment = get_item("Consignments", "consignment", self.consignment_id)
        if not consignment:
            log.error("Failed to fetch consignment for payout export")
            QMessageBox.critical(self, "Error", "Failed to fetch consignment data")
            return None, None, None

        vendor_id = consignment.get('vendor_id')
        vendor = get_item("Entities", "vendor", vendor_id)
        if not vendor:
            log.error(f"Failed to fetch vendor {vendor_id} for payout export")
            QMessageBox.critical(self, "Error", "Failed to fetch vendor data")
            return None, None, None

        revenue_data = {
            'shared': consignment.get('revenue', {}).get('shared', []),
            'grouped': consignment.get('revenue', {}).get('grouped', []),
            'payout': self.payout_list[:payout_index + 1],
            'accumulated': consignment.get('revenue', {}).get('accumulated', {})
        }

        return consignment, vendor, revenue_data

    def _handle_entry_pdf(self):
        """
        :purpose: generates a PDF for the ticket at a specific payout state
        :author(s): Joe Lee
        """
        payout_index = self.sender().property("payout_index")
        consignment, vendor, revenue_data = self._get_payout_ticket_data(payout_index)
        if not consignment:
            return

        try:
            handler_live_pdf(
                self.consignment_id,
                vendor,
                consignment.get('products', []),
                revenue_data,
                consignment.get('datetime', ''),
                payout_number=payout_index + 1
            )
            QMessageBox.information(self, "PDF Generated", f"PDF generated for Ticket Number: {self.consignment_id} Payout #{payout_index + 1}")
            log.info(f"PDF generated for Ticket Number: {self.consignment_id} Payout #{payout_index + 1}")
        except Exception as e:
            log.error(f"Failed to generate PDF for payout #{payout_index + 1}: {e}")
            QMessageBox.critical(self, "PDF Failed", f"Failed to generate PDF:\n\n{e}")

    def _handle_entry_print(self):
        """
        :purpose: generates a PDF for the specific payout state then sends to printer
        :author(s): Joe Lee
        """
        payout_index = self.sender().property("payout_index")
        consignment, vendor, revenue_data = self._get_payout_ticket_data(payout_index)
        if not consignment:
            return

        try:
            handler_live_pdf(
                self.consignment_id,
                vendor,
                consignment.get('products', []),
                revenue_data,
                consignment.get('datetime', ''),
                payout_number=payout_index + 1
            )
        except Exception as e:
            log.error(f"Failed to generate PDF for printing payout #{payout_index + 1}: {e}")
            QMessageBox.critical(self, "PDF Failed", f"Failed to generate PDF:\n\n{e}")
            return

        try:
            handler_print(f"{self.consignment_id}_payout_{payout_index + 1}")
            QMessageBox.information(self, "Print Sent", f"Payout #{payout_index + 1} sent to printer")
            log.info(f"Print requested for consignment {self.consignment_id} payout #{payout_index + 1}")
        except Exception as e:
            log.error(f"Failed to print payout #{payout_index + 1}: {e}")
            QMessageBox.critical(self, "Print Failed", f"Failed to print:\n\n{e}")

    def _handle_entry_excel(self):
        """
        :purpose: generates an Excel export for the ticket at a specific payout state
        :author(s): Joe Lee
        """
        payout_index = self.sender().property("payout_index")
        consignment, vendor, revenue_data = self._get_payout_ticket_data(payout_index)
        if not consignment:
            return

        try:
            data = {
                'ticket_info': {
                    'ticket_number': consignment.get('consignment_id'),
                    'vendor_id': consignment.get('vendor_id'),
                    'created': consignment.get('datetime'),
                    'status': consignment.get('status'),
                },
                'product_data': consignment.get('products', []),
                'revenue_shared': revenue_data['shared'],
                'revenue_grouped': revenue_data['grouped'],
                'revenue_payout': revenue_data['payout'],
            }
            xls_gen.generate_excel(data)
            QMessageBox.information(self, "Excel Generated", f"Excel generated for payout #{payout_index + 1}")
            log.info(f"Excel generated for consignment {self.consignment_id} payout #{payout_index + 1}")
        except Exception as e:
            log.error(f"Failed to generate Excel for payout #{payout_index + 1}: {e}")
            QMessageBox.critical(self, "Excel Failed", f"Failed to generate Excel:\n\n{e}")