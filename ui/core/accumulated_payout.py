from PyQt6.QtWidgets import QWidget
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtWidgets import QHBoxLayout
from PyQt6.QtWidgets import QLabel
from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtCore import Qt

from services.get_item import get_item

import utils.logger.logger as log


class AccumulatedPayout(QWidget):
    def __init__(self):
        super().__init__()
        self.consignment_id = None
        self.signed_vendor = None
        self.signed_super_x = None
        self.accumulated_vendor = None
        self.accumulated_super_x = None
        self.remaining_vendor = None
        self.remaining_super_x = None
        self.setup_ui()

    def setup_ui(self):
        """
        :purpose: initializes the accumulated payout widget with signed, paid out, and remaining rows
        :author(s): Joe Lee
        """
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        header_layout = QHBoxLayout()

        spacer = QLabel("")
        spacer.setFixedWidth(120)
        header_layout.addWidget(spacer)

        vendor_header = QLabel("Vendor")
        vendor_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        vendor_header.setFixedWidth(120)
        header_layout.addWidget(vendor_header)

        super_x_header = QLabel("Super X")
        super_x_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        super_x_header.setFixedWidth(120)
        header_layout.addWidget(super_x_header)

        main_layout.addLayout(header_layout)

        signed_layout = QHBoxLayout()
        signed_label = QLabel("Signed:")
        signed_label.setFixedWidth(120)
        signed_layout.addWidget(signed_label)

        self.signed_vendor = QLineEdit("$0.00")
        self.signed_vendor.setReadOnly(True)
        self.signed_vendor.setObjectName("READ_ONLY")
        self.signed_vendor.setFixedWidth(120)
        signed_layout.addWidget(self.signed_vendor)

        self.signed_super_x = QLineEdit("$0.00")
        self.signed_super_x.setReadOnly(True)
        self.signed_super_x.setObjectName("READ_ONLY")
        self.signed_super_x.setFixedWidth(120)
        signed_layout.addWidget(self.signed_super_x)

        main_layout.addLayout(signed_layout)

        accumulated_layout = QHBoxLayout()
        accumulated_label = QLabel("Paid Out:")
        accumulated_label.setFixedWidth(120)
        accumulated_layout.addWidget(accumulated_label)

        self.accumulated_vendor = QLineEdit("$0.00")
        self.accumulated_vendor.setReadOnly(True)
        self.accumulated_vendor.setObjectName("READ_ONLY")
        self.accumulated_vendor.setFixedWidth(120)
        accumulated_layout.addWidget(self.accumulated_vendor)

        self.accumulated_super_x = QLineEdit("$0.00")
        self.accumulated_super_x.setReadOnly(True)
        self.accumulated_super_x.setObjectName("READ_ONLY")
        self.accumulated_super_x.setFixedWidth(120)
        accumulated_layout.addWidget(self.accumulated_super_x)

        main_layout.addLayout(accumulated_layout)

        remaining_layout = QHBoxLayout()
        remaining_label = QLabel("Remaining:")
        remaining_label.setFixedWidth(120)
        remaining_layout.addWidget(remaining_label)

        self.remaining_vendor = QLineEdit("$0.00")
        self.remaining_vendor.setReadOnly(True)
        self.remaining_vendor.setObjectName("READ_ONLY")
        self.remaining_vendor.setFixedWidth(120)
        remaining_layout.addWidget(self.remaining_vendor)

        self.remaining_super_x = QLineEdit("$0.00")
        self.remaining_super_x.setReadOnly(True)
        self.remaining_super_x.setObjectName("READ_ONLY")
        self.remaining_super_x.setFixedWidth(120)
        remaining_layout.addWidget(self.remaining_super_x)

        main_layout.addLayout(remaining_layout)
        main_layout.addStretch()

    def load(self, consignment_id):
        """
        :purpose: fetches consignment from DB and populates all fields
        :param consignment_id: the consignment ID to fetch
        :author(s): Joe Lee
        """
        self.consignment_id = consignment_id
        consignment = get_item("Consignments", "consignment", self.consignment_id)
        if not consignment:
            log.error(f"Failed to fetch consignment {self.consignment_id} for accumulated payout")
            return

        revenue = consignment.get('revenue', {})
        accumulated = revenue.get('accumulated', {})

        if accumulated:
            signed_v = float(accumulated['signed_vendor'])
            signed_sx = float(accumulated['signed_super_x'])
            acc_v = float(accumulated['vendor'])
            acc_sx = float(accumulated['super_x'])
        else:
            shared = revenue.get('shared', [])
            if shared:
                signed_v = float(shared[-1]['vendor'])
                signed_sx = float(shared[-1]['super_x'])
            else:
                signed_v = 0.0
                signed_sx = 0.0
            acc_v = 0.0
            acc_sx = 0.0

        self.signed_vendor.setText(f"${signed_v:.2f}")
        self.signed_super_x.setText(f"${signed_sx:.2f}")
        self.accumulated_vendor.setText(f"${acc_v:.2f}")
        self.accumulated_super_x.setText(f"${acc_sx:.2f}")
        self.remaining_vendor.setText(f"${signed_v - acc_v:.2f}")
        self.remaining_super_x.setText(f"${signed_sx - acc_sx:.2f}")

    def refresh(self):
        """
        :purpose: re-fetches from DB and updates display
        :author(s): Joe Lee
        """
        self.load(self.consignment_id)