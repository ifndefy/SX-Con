from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QWidget
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtWidgets import QTabWidget
from PyQt6.QtWidgets import QHBoxLayout
from PyQt6.QtWidgets import QLabel
from PyQt6.QtWidgets import QPushButton

from handlers.api_handler import APIHandler
from src import SPOT
from src.imgs import img_helpers
from src.user import current_user
from ui.core.theme_manager import ThemeManager
from ui.core.status_bar import StatusBar
from ui.tabs.create_new import CreateNewTab
from ui.tabs.vendor_tickets import VendorTicketsTab
from ui.tabs.open_tickets import OpenTicketsTab
from ui.tabs.settings import SettingsTab
from ui.tabs.admin_settings import AdminSettingsTab
from services.connect_database import db_connection
import utils.logger.logger as log

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.current_user = current_user
        self.status_label = None
        self.revision_label = None
        self.theme_dropdown_menu = None
        self.tabs = None
        self.create_new_tab = None
        self.vendor_tickets_tab = None
        self.open_tickets_tab = None
        self.settings_tab = None
        self.admin_settings_tab = None

        self.logo_path = img_helpers.get_window_logo_path()
        self.api_handler = APIHandler()
        self.theme_manager = ThemeManager()
        self.db_connection = db_connection
        self.setup_window()
        self.setup_ui()
        self.theme_manager.apply_default_theme(self)

    def setup_window(self):
        self.setWindowTitle("SX-Con")
        self.setGeometry(0, 0, 1100, 795)
        self.setMinimumSize(1100, 795)

    def setup_ui(self):
        layout = QVBoxLayout(self)

        # Logo + Program title + Revision info
        title_layout = QHBoxLayout()

        label = QLabel(self)
        logo_img = QPixmap(self.logo_path)
        scaled_logo_image = logo_img.scaledToWidth(logo_img.width(), Qt.TransformationMode.SmoothTransformation)
        label.setPixmap(scaled_logo_image)
        title_layout.addWidget(label, alignment=Qt.AlignmentFlag.AlignLeft)

        title_layout.addStretch()  # Push to left

        log_rev_container = QVBoxLayout()
        self.logout_button = QPushButton("Logout")
        self.logout_button.setObjectName("logout_button")
        self.logout_button.clicked.connect(self.logout)
        log_rev_container.addWidget(self.logout_button, alignment=Qt.AlignmentFlag.AlignTop)

        # Revision info
        self.revision_label = QLabel(SPOT.APP_VERSION)
        self.revision_label.setObjectName("revision_label")
        log_rev_container.addWidget(self.revision_label)

        title_layout.addLayout(log_rev_container)
        layout.addLayout(title_layout)

        self.setup_tabs()
        layout.addWidget(self.tabs)

        #Embed status bar into Main window
        status_container = StatusBar("status_container")
        status_container.add_handler(self.change_status_label)
        status_section = QHBoxLayout(status_container)

        status_section.addStretch()
        self.status_label = QLabel("Ready to create record")
        status_section.addWidget(self.status_label)
        status_section.addStretch()
        layout.addWidget(status_container)

    def setup_tabs(self):
        self.tabs = QTabWidget()
        self.tabs.setObjectName("main_tabs")

        self.create_new_tab = CreateNewTab(self.api_handler, self.db_connection)
        self.vendor_tickets_tab = VendorTicketsTab(self.api_handler, self.db_connection)
        self.open_tickets_tab = OpenTicketsTab(self.api_handler, self.db_connection)
        self.settings_tab = SettingsTab(self.api_handler)

        self.tabs.addTab(self.create_new_tab, "Create New")
        self.tabs.addTab(self.vendor_tickets_tab, "Vendor Tickets")
        self.tabs.addTab(self.open_tickets_tab, "Open Tickets")
        self.tabs.addTab(self.settings_tab, "Settings")

        if current_user.is_admin():
            self.admin_settings_tab = AdminSettingsTab(self.api_handler, self.db_connection)
            self.tabs.addTab(self.admin_settings_tab, "Admin Settings")
            self.tabs.tabBar().setStyleSheet("QTabBar::tab:last { background-color: #691601; }")
        self.tabs.currentChanged.connect(self.on_tab_changed)

    def on_tab_changed(self, index):
        log.info(f"{self.tabs.tabText(index)} tab clicked")

    def change_status_label(self, message):
        if self.status_label:
            self.status_label.setText(message)

    def logout(self):
        """
        Handle user logout.

        When the login screen is implemented, this method should:
          - show the login window
          - close this main window

        For now, it safely handles the case where LoginWindow doesn't exist yet.
        Author(s): Kyle Valdez, Joe Lee
        """
        self.logout_requested = True
        self.close()
