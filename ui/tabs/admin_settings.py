from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QVBoxLayout, QTabWidget
from PyQt6.QtWidgets import QHBoxLayout
from PyQt6.QtWidgets import QLabel
from PyQt6.QtWidgets import QScrollArea
from PyQt6.QtWidgets import QWidget

from ui.tabs.base import BaseTab
from ui.tabs.subtabs.tickets import RecordsTab
from ui.tabs.subtabs.users import UsersTab
from ui.tabs.subtabs.vendors import VendorsTab
from ui.tabs.subtabs.products import ProductsTab


class AdminSettingsTab(BaseTab):
    def __init__(self, api_handler, db_connection):
        self.db_connection = db_connection
        super().__init__(api_handler, "admin_settings")

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
        sub_layout = QVBoxLayout(self)

        # Setup tabs
        self.setup_subtabs()
        sub_layout.addWidget(self.tabs)

        # Set up the scroll area
        scroll.setWidget(scroll_content)
        sub_layout = QVBoxLayout(self)
        sub_layout.addWidget(scroll)

        # HR Line to separate buttons at the bottom
        hr3 = QLabel()
        hr3.setObjectName("hr")
        sub_layout.addWidget(hr3)

        # Status Section
        status_container = QWidget()
        status_container.setObjectName("status_container")
        status_section = QHBoxLayout(status_container)

        # Align to center
        status_section.addStretch()
        self.status_label = QLabel("Temporary")
        status_section.addWidget(self.status_label, alignment=Qt.AlignmentFlag.AlignCenter)
        status_section.addStretch()

        sub_layout.addWidget(status_container)

    def setup_subtabs(self):
        self.tabs = QTabWidget()
        self.tabs.setObjectName("subtabs")

        # Pass the database connection to all subtabs
        self.users_tab = UsersTab(self.api_handler, self.db_connection)
        self.vendors_tab = VendorsTab(self.api_handler, self.db_connection)
        self.products_tab = ProductsTab(self.api_handler, self.db_connection)
        self.records_tab = RecordsTab(self.api_handler, self.db_connection)

        self.tabs.addTab(self.users_tab, "Users")
        self.tabs.addTab(self.vendors_tab, "Vendors")
        self.tabs.addTab(self.products_tab, "Products")
        self.tabs.addTab(self.records_tab, "Records")

        self.tabs.currentChanged.connect(self.on_tab_changed)

    def on_tab_changed(self, index):
        print(f"{self.tabs.tabText(index)} tab clicked")