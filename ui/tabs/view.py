from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtWidgets import QLabel
from PyQt6.QtWidgets import QPushButton
from ui.tabs.base import BaseTab

class ViewTab(BaseTab):
    def __init__(self, api_handler):
        super().__init__(api_handler, "view")

    def setup_ui(self):
        layout = QVBoxLayout(self)
        self.label = QLabel("VIEW tab")
        self.button = QPushButton("Do Something")
        layout.addWidget(self.label)
        layout.addWidget(self.button)

    def btn_actions(self):
        self.button.clicked.connect(self.on_button_clicked)

    def on_button_clicked(self):
        super().on_button_clicked()
        result = self.api_handler.process_action("VIEW")
        self.label.setText(result)