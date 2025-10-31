from PyQt6.QtWidgets import QWidget

class BaseTab(QWidget):
    def __init__(self, api_handler, tab_name):
        super().__init__()
        self.api_handler = api_handler
        self.tab_name = tab_name
        self.setObjectName(f"{tab_name.lower()}_tab")
        self.setup_ui()
        self.btn_actions()

    def setup_ui(self):
        raise NotImplementedError(f"{self.__class__.__name__} must implement setup_ui()")

    def btn_actions(self):
        pass

    def on_button_clicked(self):
        print(f"{self.tab_name} button clicked")
        result = self.api_handler.process_action(self.tab_name.upper())