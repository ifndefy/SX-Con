from PyQt6.QtWidgets import QWidget
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtWidgets import QTabWidget
from PyQt6.QtWidgets import QHBoxLayout
from PyQt6.QtWidgets import QLabel

from handlers.api_handler import APIHandler
from src import SPOT
from ui.core.theme_manager import ThemeManager
from ui.tabs.post import PostTab
from ui.tabs.get import GetTab
from ui.tabs.view import ViewTab
from ui.tabs.settings import SettingsTab
from ui.tabs.admin import AdminTab

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
        self.setup_window()
        self.theme_manager.apply_default_theme(self)
        self.setup_ui()

    def setup_window(self):
        self.setWindowTitle("SX-Con")
        self.setGeometry(0, 0, 1100, 756)
        self.setMinimumSize(1100, 756)
        # todo: Resize height to fit Super X logo when delivered to developers

    def setup_ui(self):
        layout = QVBoxLayout(self)

        # Logo + Program title + Revision info
        title_layout = QHBoxLayout()

        # todo: Insert Super X image logo

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

        # Setup tabs
        self.setup_tabs()
        layout.addWidget(self.tabs)

    def setup_tabs(self):
        self.tabs = QTabWidget()

        self.post_tab = PostTab(self.api_handler)
        self.get_tab = GetTab(self.api_handler)
        self.view_tab = ViewTab(self.api_handler)
        self.settings_tab = SettingsTab(self.api_handler)
        self.admin_tab = AdminTab(self.api_handler)

        self.tabs.addTab(self.post_tab, "Create New Record")
        self.tabs.addTab(self.get_tab, "Fetch from Database")
        self.tabs.addTab(self.view_tab, "View Open Tickets")
        self.tabs.addTab(self.settings_tab, "Settings")
        # self.tabs.addTab(self.admin_tab, "Admin Settings")

        self.tabs.currentChanged.connect(self.on_tab_changed)

    def on_tab_changed(self, index):
        print(f"{self.tabs.tabText(index)} tab clicked")