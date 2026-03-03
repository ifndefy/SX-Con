import pandas as pd

from ui.tabs.base import BaseTab
import utils.logger.logger as log

from PyQt6.QtWidgets import QWidget
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QSizePolicy, QScrollArea, QSpacerItem
from PyQt6.QtWidgets import QLabel, QLineEdit, QPushButton
from PyQt6.QtGui import QIntValidator

from services import parse_consignment_table as c_table

class CRTab(BaseTab):
    def __init__(self, api_handler):
        super().__init__(api_handler, "consignment_rates")
        self.entry_list = None

        self.scroll_zone = None

        self.consignments_section_layout = None
        self.consignments_section = None

        self.tab_header = None
        self.tab_title = None

        self.tab_content_layout = None
        self.tab_content = None

        self.main_layout = None
    
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

        #Setup scrolling for ticket box
        self.scroll_zone = QScrollArea()
        self.scroll_zone.setWidgetResizable(True)
        self.scroll_zone.setWidget(self.consignments_section)

        #Add objects to content Canvas
        self.tab_content_layout.addLayout(self.tab_header)
        self.tab_content_layout.addWidget(hr1)
        self.tab_content_layout.addWidget(self.scroll_zone)
        
        #Add Canvas to tab
        self.main_layout.addWidget(self.tab_content)
        #todo: move to on_active_tab to avoid fetching until we need the data
        self.populate_rate_settings()

    #Retrieve tha table from SPOT_CR.csv and turn it into entries in our widget's section
    def populate_rate_settings(self):
        self.entry_list = c_table.fetch_consignment_data()
        log.debug(f"Retrieved consignment rates: {self.entry_list}")
        for key, value in self.entry_list.items():
            self.consignments_section_layout.addWidget(_CREntry(key, value))
        self.consignments_section_layout.addStretch()

    #todo: add check in admin_settings to trigger on_active_tab when the tab being switched to has this function, use to populate tickets when needed
    def on_active_tab(self):
        pass

    def setup_button_connections(self):
        pass

#private entry object, should only be used by this subtab
class _CREntry(QWidget):
    def __init__(self, product_type = None, rate = None):
        super().__init__()
        #Store constructor data
        self.old_rate = None
        self.old_type = None
        self.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        
        #Create 'box' to hold ticket fields/buttons
        self.entry_container = QWidget()
        self.entry_container.setObjectName("entry_body")
        self.entry_container.setProperty("state", "READ_ONLY")
        self.entry_layout = QHBoxLayout(self.entry_container)
  
        #Create Elements of ticket
        self.type_line = QLabel("Type:")
        self.type_line.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        
        self.product_type_input = QLineEdit(f"{product_type}" if product_type else "")
        self.product_type_input.setPlaceholderText("Produce Type")
        self.product_type_input.setObjectName("entry_field")
        self.product_type_input.setProperty("state", "READ_ONLY")
        self.product_type_input.setMaxLength(30)
        self.product_type_input.setFixedWidth(265)
        self.product_type_input.setReadOnly(True)

        self.middle_spacer = QSpacerItem(45, 50, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        
        self.rate_line = QLabel("Rate:")
        self.rate_line.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.product_rate_input = QLineEdit(f"{rate}" if rate else "")
        self.product_rate_input.setPlaceholderText("Produce Rate")
        self.product_rate_input.setObjectName("entry_field")
        self.product_rate_input.setProperty("state", "READ_ONLY")
        self.product_rate_input.setMaxLength(30)
        self.product_rate_input.setFixedWidth(265)
        self.product_rate_input.setValidator(QIntValidator(0, 100, self))
        self.product_rate_input.setReadOnly(True)

        self.end_spacer = QSpacerItem(45, 50, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.entry_edit_btn = QPushButton("Edit")

        self.edit_cancel_btn = QPushButton("Cancel")
        self.edit_cancel_btn.setObjectName("red_btn")
        self.edit_cancel_btn.hide()

        self.edit_save_btn = QPushButton("Save")
        self.edit_save_btn.hide()

        #Add elements to entry container
        self.entry_layout.addWidget(self.type_line)
        self.entry_layout.addWidget(self.product_type_input)

        self.entry_layout.addItem(self.middle_spacer)

        self.entry_layout.addWidget(self.rate_line)
        self.entry_layout.addWidget(self.product_rate_input)

        self.entry_layout.addStretch()

        self.entry_layout.addWidget(self.entry_edit_btn)
        self.entry_layout.addWidget(self.edit_cancel_btn)
        self.entry_layout.addWidget(self.edit_save_btn)

        self.setup_button_connections()
        
        #Create top-level widget to store ticket container
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0,0,0,0)
        self.main_layout.addWidget(self.entry_container)

    def setup_button_connections(self):
        self.entry_edit_btn.clicked.connect(self.edit_btn_handler)
        self.edit_save_btn.clicked.connect(self.save_btn_handler)
        self.edit_cancel_btn.clicked.connect(self.cancel_btn_handler)

    def get_rate(self):
        return self.product_rate_input.text().strip() or None

    def get_type(self):
        return self.product_type_input.text().strip() or None

    #retrieves the values of the QlineEdit fields, returns a dict
    def fetch_field_values(self):
        return {
            "type" : self.get_type(),
            "rate" : self.get_rate()
        }

    #Save current values for roll back, unlock fields and swap to other button set
    def edit_btn_handler(self):
        self.old_type = self.get_type()
        self.old_rate = self.get_rate()
        log.info(f"Editing {self.old_type} entry, current value: {self.old_rate}")

        self.product_rate_input.setReadOnly(False)
        self.product_rate_input.setProperty("state", "READ_WRITE")
        self.entry_container.setProperty("state", "READ_WRITE")

        #Refresh the widget style to update appearance
        self.product_rate_input.style().unpolish(self.product_rate_input)
        self.product_rate_input.style().polish(self.product_rate_input)

        self.entry_container.style().unpolish(self.entry_container)
        self.entry_container.style().polish(self.entry_container)

        self.parent().setFocus()
        self.entry_edit_btn.hide()
        self.edit_cancel_btn.show()
        self.edit_save_btn.show()

    # lock fields, restore old values to fields and swap to other button set
    def cancel_btn_handler(self):

        log.info(f"Edit Aborted, resetting values {self.get_rate()} -> {self.old_rate}")
        self.product_rate_input.setReadOnly(True)
        self.product_rate_input.setProperty("state", "READ_ONLY")
        self.entry_container.setProperty("state", "READ_ONLY")

        #Refresh the widget style to update appearance
        self.product_rate_input.style().unpolish(self.product_rate_input)
        self.product_rate_input.style().polish(self.product_rate_input)

        self.entry_container.style().unpolish(self.entry_container)
        self.entry_container.style().polish(self.entry_container)

        self.product_rate_input.setText(self.old_rate)
        self.product_type_input.setText(self.old_type)

        self.parent().setFocus()
        self.edit_cancel_btn.hide()
        self.edit_save_btn.hide()
        self.entry_edit_btn.show()

    def save_btn_handler(self):
        field_data = self.fetch_field_values()

        if field_data["type"] is None or field_data["rate"] is None:
            log.warning(f"One or more fields is NULL, Aborting save...")
            return
        else:
            log.info(f"Saving to SPOT, new values: {field_data}")
            _write_to_spot_csv(field_data)

        self.product_rate_input.setReadOnly(True)
        self.product_rate_input.setProperty("state", "READ_ONLY")
        self.entry_container.setProperty("state", "READ_ONLY")

        #Refresh the widget style to update appearance, might want to wrap this in a function/ set up a util or service .py file to provide helpers with stuff like this
        self.product_rate_input.style().unpolish(self.product_rate_input)
        self.product_rate_input.style().polish(self.product_rate_input)

        self.entry_container.style().unpolish(self.entry_container)
        self.entry_container.style().polish(self.entry_container)
        
        self.parent().setFocus()
        self.edit_save_btn.hide()
        self.edit_cancel_btn.hide()
        self.entry_edit_btn.show()

#might be worth moving this, but ideally this remains private to consignment_rate.py since it should be the only one writing to SPOT
def _write_to_spot_csv(data):
    dataframe = pd.read_csv("./src/SPOT_CR.csv")
    dataframe = dataframe.set_index("Type")
    dataframe.loc[data["type"], "Rate"] = int(data["rate"])
    dataframe.to_csv("./src/SPOT_CR.csv")
