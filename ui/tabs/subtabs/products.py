from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QVBoxLayout, QTabWidget
from PyQt6.QtWidgets import QHBoxLayout
from PyQt6.QtWidgets import QLabel
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtWidgets import QScrollArea
from PyQt6.QtWidgets import QWidget

from services.database_service import DatabaseService
from ui.tabs.base import BaseTab

class ProductsTab(BaseTab):
    def __init__(self, api_handler):
        super().__init__(api_handler, "products")

    # self.setup_button_connections()

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



        # Set up the scroll area
        scroll.setWidget(scroll_content)
        sub_layout = QVBoxLayout(self)
        sub_layout.addWidget(scroll)

        # self.setup_button_connections()

    def btn_actions(self):
        pass