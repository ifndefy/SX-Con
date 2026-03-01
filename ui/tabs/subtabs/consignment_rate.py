from ui.tabs.base import BaseTab

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QSizePolicy, QScrollArea, QSpacerItem
from PyQt6.QtWidgets import QLabel, QLineEdit, QPushButton

class CRTab(BaseTab):
    def __init__(self, api_handler):
        super().__init__(api_handler, "consignment_rates")
        self.ticket_list = []
    
    def setup_ui(self):
        #Create main layout
        self.main_layout = QVBoxLayout(self)

        #Create main 'Canvas' for the widget and give it the content layout
        self.tab_content = QWidget()
        self.tab_content_layout = QVBoxLayout(self.tab_content)

        #Create Title box
        self.tab_title = QLabel("Consignment Rates")
        self.tab_title.setObjectName("post_title")
        
        self.tab_header = QHBoxLayout()
        self.tab_header.addWidget(self.tab_title)
        self.tab_header.addStretch()
        
        #Add break line
        hr1 = QLabel()
        hr1.setObjectName("hr")

        #Ticket Section
        self.consignments_section = QWidget()
        self.consignments_section_layout = QVBoxLayout(self.consignments_section)
        self.consignments_section_layout.setSpacing(2)
        self.setup_consignment_fields()

        #Add objects to content Canvas
        self.tab_content_layout.addLayout(self.tab_header)
        self.tab_content_layout.addWidget(hr1)
        self.tab_content_layout.addWidget(self.scroll_zone)
        
        #Add Canvas to tab
        self.main_layout.addWidget(self.tab_content)

    #Parse the consignment ticket list and populate ui with the objects
    def setup_consignment_fields(self):
        #Setup scrolling for ticket box
        self.scroll_zone = QScrollArea()
        self.scroll_zone.setWidgetResizable(True)
        self.scroll_zone.setWidget(self.consignments_section)

        #big blob of tickets to test scrolling
        self.consignments_section_layout.addWidget(CRTicket())
        self.consignments_section_layout.addWidget(CRTicket())
        self.consignments_section_layout.addWidget(CRTicket())
        self.consignments_section_layout.addWidget(CRTicket())
        self.consignments_section_layout.addWidget(CRTicket())
        self.consignments_section_layout.addWidget(CRTicket())
        self.consignments_section_layout.addWidget(CRTicket())
        self.consignments_section_layout.addWidget(CRTicket())
        self.consignments_section_layout.addWidget(CRTicket())
        self.consignments_section_layout.addWidget(CRTicket())
        self.consignments_section_layout.addWidget(CRTicket())
        self.consignments_section_layout.addWidget(CRTicket())
        self.consignments_section_layout.addWidget(CRTicket())
        self.consignments_section_layout.addWidget(CRTicket())
        self.consignments_section_layout.addWidget(CRTicket())
        self.consignments_section_layout.addWidget(CRTicket())
        self.consignments_section_layout.addWidget(CRTicket())
        self.consignments_section_layout.addWidget(CRTicket())

    def setup_button_connections(self):
        pass

    #get consignment list items and store in our ticket list
    def parse_consignment_file(self):
        pass

class CRTicket(QWidget):
    def __init__(self, type = None, rate = None):
        super().__init__()  
        
        #Create 'box' to hold ticket fields/buttons
        self.ticket_container = QWidget()
        self.ticket_container.setObjectName("ticket_body")
        self.ticket_layout = QHBoxLayout(self.ticket_container)
  
        #Create Elements of ticket
        self.type_line = QLabel("Type:")
        self.type_line.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        
        self.product_type_input = QLineEdit()
        self.product_type_input.setPlaceholderText("Produce Type")
        self.product_type_input.setMaxLength(30)
        self.product_type_input.setFixedWidth(265)
        self.product_type_input.setReadOnly(True)

        self.middle_spacer = QSpacerItem(45, 50, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        
        self.rate_line = QLabel("Rate:")
        self.rate_line.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.product_rate_input = QLineEdit()
        self.product_rate_input.setPlaceholderText("Produce Rate")
        self.product_rate_input.setMaxLength(30)
        self.product_rate_input.setFixedWidth(265)
        self.product_rate_input.setReadOnly(True)

        self.end_spacer = QSpacerItem(45, 50, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.ticket_edit_btn = QPushButton("Edit")

        self.ticket_cancel_btn = QPushButton("Cancel")
        self.ticket_cancel_btn.setObjectName("red_btn")
        self.ticket_cancel_btn.hide()

        self.ticket_save_btn = QPushButton("Save")
        self.ticket_save_btn.hide()

        #Add elements to ticket container
        self.ticket_layout.addWidget(self.type_line)
        self.ticket_layout.addWidget(self.product_type_input)

        #self.ticket_layout.addSpacing(45)

        self.ticket_layout.addItem(self.middle_spacer)

        self.ticket_layout.addWidget(self.rate_line)
        self.ticket_layout.addWidget(self.product_rate_input)

        self.ticket_layout.addStretch()

        self.ticket_layout.addWidget(self.ticket_edit_btn)
        self.ticket_layout.addWidget(self.ticket_cancel_btn)
        self.ticket_layout.addWidget(self.ticket_save_btn)

        self.setup_button_connections()
        
        #Create top-level widget to store ticket container
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0,0,0,0)
        self.main_layout.addWidget(self.ticket_container)

    def setup_button_connections(self):
        self.ticket_edit_btn.clicked.connect(self.edit_btn_handler)
        self.ticket_cancel_btn.clicked.connect(self.cancel_btn_handler)
        self.ticket_save_btn.clicked.connect(self.save_btn_handler)

    def edit_btn_handler(self):
        #todo: save current ticket values for potential rollback
        self.product_type_input.setReadOnly(False)
        self.product_rate_input.setReadOnly(False)

        self.ticket_cancel_btn.show()
        self.ticket_save_btn.show()
        self.ticket_edit_btn.hide()

    def cancel_btn_handler(self):
        #todo:implement state rollback
        self.product_type_input.setReadOnly(True)
        self.product_rate_input.setReadOnly(True)

        self.ticket_cancel_btn.hide()
        self.ticket_save_btn.hide()
        self.ticket_edit_btn.show()

    def save_btn_handler(self):
        #todo: implement saving to SPOT
        print(f"hello world from {self}")
        self.product_type_input.setReadOnly(True)
        self.product_rate_input.setReadOnly(True)

        self.ticket_cancel_btn.hide()
        self.ticket_save_btn.hide()
        self.ticket_edit_btn.show()


