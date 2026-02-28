from ui.tabs.base import BaseTab

class CRTab(BaseTab):
    def __init__(self, api_handler, tab_name):
        super().__init__(api_handler, "consignment_rates")
    
    def setup_ui(self):
        pass

    def setup_button_connections(self):
        pass