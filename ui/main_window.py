import sys
from PyQt6.QtWidgets import QWidget
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtWidgets import QLabel
from PyQt6.QtWidgets import QTabWidget
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtWidgets import QApplication
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
        self.post_label = QLabel("POST tab")
        self.post_button = QPushButton("Do Something")
        self.post_button.clicked.connect(self.on_post_clicked)
        post_layout.addWidget(self.post_label)
        post_layout.addWidget(self.post_button)
        self.post_tab.setLayout(post_layout)

        get_layout = QVBoxLayout()
        self.get_label = QLabel("GET tab")
        self.get_button = QPushButton("Do Something")
        self.get_button.clicked.connect(self.on_get_clicked)
        get_layout.addWidget(self.get_label)
        get_layout.addWidget(self.get_button)
        self.get_tab.setLayout(get_layout)

        delete_layout = QVBoxLayout()
        self.delete_label = QLabel("DELETE tab")
        self.delete_button = QPushButton("Do Something")
        self.delete_button.clicked.connect(self.on_delete_clicked)
        delete_layout.addWidget(self.delete_label)
        delete_layout.addWidget(self.delete_button)
        self.delete_tab.setLayout(delete_layout)

        view_layout = QVBoxLayout()
        self.view_label = QLabel("VIEW tab")
        self.view_button = QPushButton("Do Something")
        self.view_button.clicked.connect(self.on_view_clicked)
        view_layout.addWidget(self.view_label)
        view_layout.addWidget(self.view_button)
        self.view_tab.setLayout(view_layout)

        admin_layout = QVBoxLayout()
        self.admin_label = QLabel("ADMIN SETTINGS tab")
        self.admin_button = QPushButton("Do Something")
        self.admin_button.clicked.connect(self.on_admin_clicked)
        admin_layout.addWidget(self.admin_label)
        admin_layout.addWidget(self.admin_button)
        self.admin_tab.setLayout(admin_layout)

        self.tabs.currentChanged.connect(self.on_tab_changed)
        main_layout.addWidget(self.tabs)
        self.setLayout(main_layout)

    def on_tab_changed(self, index):
        self.post_label.setText("POST tab")
        self.get_label.setText("GET tab")
        self.delete_label.setText("DELETE tab")
        self.view_label.setText("VIEW tab")
        self.admin_label.setText("ADMIN SETTINGS tab")
        print(f"{self.tabs.tabText(index)} tab clicked")

    def on_post_clicked(self):
        print("POST button clicked")
        result = self.api_handler.process_action("POST")
        self.post_label.setText(result)

    def on_get_clicked(self):
        print("GET button clicked")
        result = self.api_handler.process_action("GET")
        self.get_label.setText(result)

    def on_delete_clicked(self):
        print("DELETE button clicked")
        result = self.api_handler.process_action("DELETE")
        self.delete_label.setText(result)

    def on_view_clicked(self):
        print("VIEW button clicked")
        result = self.api_handler.process_action("VIEW")
        self.view_label.setText(result)

    def on_admin_clicked(self):
        print("ADMIN SETTINGS button clicked")
        result = self.api_handler.process_action("ADMIN SETTINGS")
        self.admin_label.setText(result)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
