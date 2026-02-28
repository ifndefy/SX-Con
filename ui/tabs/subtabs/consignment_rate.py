from ui.tabs.base import BaseTab

from PyQt6.QtWidgets import QWidget
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QSizePolicy
from PyQt6.QtWidgets import QLabel

class CRTab(BaseTab):
    def __init__(self, api_handler, tab_name):
        super().__init__(api_handler, "consignment_rates")
    
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
        
        self.consignments_section = QVBoxLayout()
        self.setup_consignment_fields()

        #Add objects to content Canvas
        self.tab_content_layout.addLayout(self.tab_header)
        self.tab_content_layout.addWidget(hr1)
        self.tab_content_layout.addLayout(self.consignments_section)
        self.tab_content_layout.addStretch()
        
        #Add Canvas to tab
        self.main_layout.addWidget(self.tab_content)

    #Parse the consignment rate list and populate ui
    def setup_consignment_fields(self):
        print(f"if there was an implementation, it would write to -> {self.consignments_section}")
        self.consignments_section.addWidget(QLabel("test1"))
        self.consignments_section.addWidget(QLabel("test2"))
        self.consignments_section.addWidget(QLabel("test3"))

    def setup_button_connections(self):
        pass

    def parse_consignment_file(self):
        pass
