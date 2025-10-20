import sys
from PyQt6.QtWidgets import QWidget
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtWidgets import QTabWidget
from PyQt6.QtWidgets import QApplication
from PyQt6.QtWidgets import QComboBox
from PyQt6.QtWidgets import QHBoxLayout
from PyQt6.QtWidgets import QLabel

from handlers.api_handler import APIHandler
from ui.core.theme_manager import ThemeManager
from ui.tabs.post import PostTab
from ui.tabs.get import GetTab
from ui.tabs.delete import DeleteTab
from ui.tabs.view import ViewTab
from ui.tabs.admin import AdminTab

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.revision_label = None
        self.theme_dropdown_menu = None
        self.tabs = None
        self.post_tab = None
        self.get_tab = None
        self.delete_tab = None
        self.view_tab = None
        self.admin_tab = None

        self.api_handler = APIHandler()
        self.theme_manager = ThemeManager()
        self.setup_window()
        self.theme_manager.apply_default_theme(self)
        self.setup_ui()

    def setup_window(self):
        self.setWindowTitle("SX-Con")
        self.setGeometry(0, 0, 1100, 695)
        # todo: Resize height to fit Super X logo when delivered to developers

    def setup_ui(self):
        main_layout = QVBoxLayout(self)

        # Setup theme selector (no argument needed)
        self.setup_theme_selector()

        # Setup tabs
        self.setup_tabs()
        main_layout.addWidget(self.tabs)

    def setup_theme_selector(self):
        # Create header layout
        header_layout = QHBoxLayout()

        # Left side: Logo + Program title + Revision info
        title_layout = QHBoxLayout()

        # todo: Insert Super X image logo

        # Program title
        program_name = QLabel("SX-Con")
        program_name.setObjectName("program_name")
        title_layout.addWidget(program_name)

        # Revision info
        self.revision_label = QLabel("v0.0.0")
        self.revision_label.setObjectName("revision_label")
        title_layout.addWidget(self.revision_label)

        title_layout.addStretch()  # Push to left
        header_layout.addLayout(title_layout)

        # Push to the right and add theme selector
        header_layout.addStretch()

        # Right side: Theme dropdown menu
        theme_label = QLabel("Theme:")
        self.theme_dropdown_menu = QComboBox()

        themes = self.theme_manager.get_available_themes()
        self.theme_dropdown_menu.addItems(themes)
        self.theme_dropdown_menu.setCurrentText(self.theme_manager.get_current_theme())
        self.theme_dropdown_menu.currentTextChanged.connect(self.on_theme_changed)

        header_layout.addWidget(theme_label)
        header_layout.addWidget(self.theme_dropdown_menu)

        # Add header to main layout
        main_layout = self.layout()
        if isinstance(main_layout, QVBoxLayout):
            main_layout.insertLayout(0, header_layout)

    def setup_tabs(self):
        self.tabs = QTabWidget()

        self.post_tab = PostTab(self.api_handler)
        self.get_tab = GetTab(self.api_handler)
        self.delete_tab = DeleteTab(self.api_handler)
        self.view_tab = ViewTab(self.api_handler)
        self.admin_tab = AdminTab(self.api_handler)

        self.tabs.addTab(self.post_tab, "Create New Record")
        self.tabs.addTab(self.get_tab, "Fetch from Database")
        self.tabs.addTab(self.delete_tab, "Delete (Temporary)")
        self.tabs.addTab(self.view_tab, "View Open Tickets")
        self.tabs.addTab(self.admin_tab, "Admin Settings")

        self.tabs.currentChanged.connect(self.on_tab_changed)

    def on_theme_changed(self, theme_name):
        self.theme_manager.apply_theme(theme_name, self)

    def on_tab_changed(self, index):
        print(f"{self.tabs.tabText(index)} tab clicked")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())