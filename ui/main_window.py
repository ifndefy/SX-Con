import sys
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTabWidget
from handlers.api_handler import APIHandler


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SX-Con")
        self.setGeometry(0, 0, 1000, 600)

        self.api_handler = APIHandler()
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout()
        self.tabs = QTabWidget()

        self.post_tab = QWidget()
        self.get_tab = QWidget()
        self.delete_tab = QWidget()
        self.view_tab = QWidget()
        self.admin_tab = QWidget()

        self.tabs.addTab(self.post_tab, "POST")
        self.tabs.addTab(self.get_tab, "GET")
        self.tabs.addTab(self.delete_tab, "DELETE")
        self.tabs.addTab(self.view_tab, "VIEW")
        self.tabs.addTab(self.admin_tab, "ADMIN SETTINGS")

        post_layout = QVBoxLayout()
        self.post_label = QLabel("POST tab selected")
        post_layout.addWidget(self.post_label)
        self.post_tab.setLayout(post_layout)

        get_layout = QVBoxLayout()
        self.get_label = QLabel("GET tab selected")
        get_layout.addWidget(self.get_label)
        self.get_tab.setLayout(get_layout)

        delete_layout = QVBoxLayout()
        self.delete_label = QLabel("DELETE tab selected")
        delete_layout.addWidget(self.delete_label)
        self.delete_tab.setLayout(delete_layout)

        view_layout = QVBoxLayout()
        self.view_label = QLabel("VIEW tab selected")
        view_layout.addWidget(self.view_label)
        self.view_tab.setLayout(view_layout)

        admin_layout = QVBoxLayout()
        self.admin_label = QLabel("Admin Settings tab selected")
        admin_layout.addWidget(self.admin_label)
        self.admin_tab.setLayout(admin_layout)

        self.tabs.currentChanged.connect(self.on_tab_changed)
        main_layout.addWidget(self.tabs)
        self.setLayout(main_layout)

    def on_tab_changed(self, index):
        tab_name = self.tabs.tabText(index)
        print(f"{tab_name} tab clicked")
        result = self.api_handler.process_action(tab_name)
        if tab_name == "POST":
            self.post_label.setText(result)
        elif tab_name == "GET":
            self.get_label.setText(result)
        elif tab_name == "DELETE":
            self.delete_label.setText(result)
        elif tab_name == "VIEW":
            self.delete_label.setText(result)
        elif tab_name == "ADMIN SETTINGS":
            self.admin_label.setText(result)
