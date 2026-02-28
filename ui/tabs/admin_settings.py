from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QVBoxLayout, QTabWidget
from PyQt6.QtWidgets import QHBoxLayout
from PyQt6.QtWidgets import QLabel
from PyQt6.QtWidgets import QScrollArea
from PyQt6.QtWidgets import QWidget

from ui.tabs.base import BaseTab
from ui.tabs.subtabs.records import RecordsTab
from ui.tabs.subtabs.users import UsersTab
from ui.tabs.subtabs.vendors import VendorsTab
from ui.tabs.subtabs.products import ProductsTab
from ui.tabs.subtabs.consignment_rate import CRTab
import utils.logger.logger as log


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
        main_layout = QVBoxLayout(self)

        # Setup tabs
        self.setup_subtabs()
        main_layout.addWidget(self.tabs)

    def setup_subtabs(self):
        self.tabs = QTabWidget()
        self.tabs.setObjectName("subtabs")

        # Pass the database connection to all subtabs
        self.users_tab = UsersTab(self.api_handler, self.db_connection)
        self.vendors_tab = VendorsTab(self.api_handler, self.db_connection)
        self.products_tab = ProductsTab(self.api_handler, self.db_connection)
        self.records_tab = RecordsTab(self.api_handler, self.db_connection)
        self.cr_tab = CRTab(self.api_handler, "Rates")

        self.tabs.addTab(self.users_tab, "Users")
        self.tabs.addTab(self.vendors_tab, "Vendors")
        self.tabs.addTab(self.products_tab, "Products")
        self.tabs.addTab(self.records_tab, "Records")
        self.tabs.addTab(self.cr_tab, "Rates")

        self.tabs.currentChanged.connect(self.on_tab_changed)

    def on_tab_changed(self, index):
        log.info(f"Admin: {self.tabs.tabText(index)} tab clicked")