from PyQt6.QtWidgets import QWidget
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtWidgets import QTabWidget
from PyQt6.QtWidgets import QHBoxLayout
from PyQt6.QtWidgets import QLabel

from handlers.api_handler import APIHandler
from src import SPOT
from ui.core.theme_manager import ThemeManager
from ui.tabs.create_new import PostTab
from ui.tabs.vendor_tickets import GetTab
from ui.tabs.open_tickets import ViewTab
from ui.tabs.settings import SettingsTab
from ui.tabs.admin_settings import AdminTab
from services.connect_database import db_connection

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.revision_label = None
        self.theme_dropdown_menu = None
        self.tabs = None
        self.post_tab = None
        self.get_tab = None
        self.view_tab = None
        self.settings_tab = None
        self.admin_tab = None

        self.api_handler = APIHandler()
        self.theme_manager = ThemeManager()
        self.db_connection = db_connection
        self.setup_window()
        self.theme_manager.apply_default_theme(self)
        self.setup_ui()

    def setup_window(self):
        self.setWindowTitle("SX-Con")
        self.setGeometry(0, 0, 1100, 762)
        self.setMinimumSize(1100, 762)

    def setup_ui(self):
        layout = QVBoxLayout(self)

        # Logo + Program title + Revision info
        title_layout = QHBoxLayout()

        # Program title
        program_name = QLabel("SX-Con")
        program_name.setObjectName("program_name")
        title_layout.addWidget(program_name)

        # Revision info
        self.revision_label = QLabel(SPOT.APP_VERSION)
        self.revision_label.setObjectName("revision_label")
        title_layout.addWidget(self.revision_label)

        title_layout.addStretch()  # Push to left
        layout.addLayout(title_layout)

        self.setup_tabs()
        layout.addWidget(self.tabs)

    def setup_tabs(self):
        self.tabs = QTabWidget()
        self.tabs.setObjectName("main_tabs")

        self.post_tab = PostTab(self.api_handler, self.db_connection)
        self.get_tab = GetTab(self.api_handler, self.db_connection)
        self.view_tab = ViewTab(self.api_handler, self.db_connection)
        self.settings_tab = SettingsTab(self.api_handler)
        self.admin_tab = AdminTab(self.api_handler, self.db_connection)

        self.tabs.addTab(self.post_tab, "Create New")
        self.tabs.addTab(self.get_tab, "Vendor Tickets")
        self.tabs.addTab(self.view_tab, "Open Tickets")
        self.tabs.addTab(self.settings_tab, "Settings")
        self.tabs.addTab(self.admin_tab, "Admin Settings")

        self.tabs.currentChanged.connect(self.on_tab_changed)

    def on_tab_changed(self, index):
        print(f"{self.tabs.tabText(index)} tab clicked")