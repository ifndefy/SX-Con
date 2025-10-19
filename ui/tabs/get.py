from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtWidgets import QLabel
from PyQt6.QtWidgets import QPushButton
from .base import BaseTab

class GetTab(BaseTab):
    def __init__(self, api_handler):
        super().__init__(api_handler, "get")

    def setup_ui(self):
        layout = QVBoxLayout(self)
        self.label = QLabel("GET tab")
        self.button = QPushButton("Do Something")
        layout.addWidget(self.label)
        layout.addWidget(self.button)

    def button_actions(self):
        self.button.clicked.connect(self.on_button_clicked)

    def on_button_clicked(self):
        super().on_button_clicked()
        result = self.api_handler.process_action("GET")
        self.label.setText(result)