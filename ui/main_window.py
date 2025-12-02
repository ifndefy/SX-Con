from PyQt6.QtWidgets import QWidget
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtWidgets import QTabWidget
from PyQt6.QtWidgets import QHBoxLayout
from PyQt6.QtWidgets import QLabel
from PyQt6.QtWidgets import QPushButton

from handlers.api_handler import APIHandler
from src import SPOT
from ui.core.theme_manager import ThemeManager
from ui.tabs.create_new import CreateNewTab
from ui.tabs.vendor_tickets import VendorTicketsTab
from ui.tabs.open_tickets import OpenTicketsTab
from ui.tabs.settings import SettingsTab
from ui.tabs.admin_settings import AdminSettingsTab
from services.connect_database import db_connection

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.revision_label = None
        self.theme_dropdown_menu = None
        self.tabs = None
        self.create_new_tab = None
        self.vendor_tickets_tab = None
        self.open_tickets_tab = None
        self.settings_tab = None
        self.admin_settings_tab = None

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

        logout_button = QPushButton("Logout")
        logout_button.setObjectName("logout_button")
        logout_button.clicked.connect(self.logout)
        title_layout.addWidget(logout_button)

    def setup_tabs(self):
        self.tabs = QTabWidget()
        self.tabs.setObjectName("main_tabs")

        self.create_new_tab = CreateNewTab(self.api_handler, self.db_connection)
        self.vendor_tickets_tab = VendorTicketsTab(self.api_handler, self.db_connection)
        self.open_tickets_tab = OpenTicketsTab(self.api_handler, self.db_connection)
        self.settings_tab = SettingsTab(self.api_handler)
        self.admin_settings_tab = AdminSettingsTab(self.api_handler, self.db_connection)

        self.tabs.addTab(self.create_new_tab, "Create New")
        self.tabs.addTab(self.vendor_tickets_tab, "Vendor Tickets")
        self.tabs.addTab(self.open_tickets_tab, "Open Tickets")
        self.tabs.addTab(self.settings_tab, "Settings")
        self.tabs.addTab(self.admin_settings_tab, "Admin Settings")

        self.tabs.currentChanged.connect(self.on_tab_changed)

    def on_tab_changed(self, index):
        print(f"{self.tabs.tabText(index)} tab clicked")

    def logout(self):
        """
        Handle user logout.

        When the login screen is implemented, this method should:
          - show the login window
          - close this main window

        For now, it safely handles the case where LoginWindow doesn't exist yet.
        """
        try:
            # Adjust the import path to wherever your LoginWindow will live
            from ui.core.login_window import LoginWindow

            self.login_window = LoginWindow()
            self.login_window.show()
            print("Logged out: returning to login screen.")
        except ImportError:
            # Fallback behavior until login is implemented
            print("LoginWindow not implemented yet. Closing application on logout.")

        # Close the main window either way
        self.close()
