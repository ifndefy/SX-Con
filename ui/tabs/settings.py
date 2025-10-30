from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtWidgets import QLabel
from PyQt6.QtWidgets import QPushButton
from ui.tabs.base import BaseTab

class SettingsTab(BaseTab):
    def __init__(self, api_handler):
        super().__init__(api_handler, "settings")

    def setup_ui(self):
        layout = QVBoxLayout(self)
        self.label = QLabel("SETTINGS tab")
        self.button = QPushButton("Do Something")
        layout.addWidget(self.label)
        layout.addWidget(self.button)

    def btn_actions(self):
        self.button.clicked.connect(self.on_button_clicked)

    def on_button_clicked(self):
        super().on_button_clicked()
        result = self.api_handler.process_action("SETTINGS")
        self.label.setText(result)