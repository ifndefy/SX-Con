from PyQt6.QtWidgets import QDialog
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtWidgets import QHBoxLayout
from PyQt6.QtWidgets import QLabel
from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtCore import Qt

from SPOT import APP_VERSION


class LoginScreen(QDialog):
    def __init__(self, theme_manager, parent=None):
        super().__init__(parent)
        self.theme_manager = theme_manager
        self.setWindowTitle("SX-Con - Login")
        self.setFixedSize(500, 400)
        self.setModal(True)

        self.username = None
        self.setup_ui()

        self.theme_manager.apply_default_theme(self)

    def setup_ui(self):
        layout = QVBoxLayout()

        # todo: Insert Client Logo
        logo = QLabel("CLIENT LOGO GOES HERE")
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo.setObjectName("logo")
        layout.addWidget(logo)

        # Title
        title = QLabel("SX-Con Login")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setObjectName("login_title")
        layout.addWidget(title)

        # Revision
        rev = QLabel(APP_VERSION)
        rev.setAlignment(Qt.AlignmentFlag.AlignCenter)
        rev.setObjectName("rev_label")
        layout.addWidget(rev)

        layout.addStretch()

        # Username
        layout.addWidget(QLabel("Username:"))
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter username")
        self.username_input.setMaxLength(30)
        layout.addWidget(self.username_input)

        # Password
        layout.addWidget(QLabel("Password:"))
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter password")
        self.password_input.setMaxLength(255) # todo: require at least 8 characters in PW
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password_input)

        # Login button
        login_btn = QPushButton("Login")
        login_btn.clicked.connect(self.attempt_login)
        layout.addWidget(login_btn)

        # Enter key also triggers login
        self.password_input.returnPressed.connect(login_btn.click)

        # Forgot Password button
        forgot_pw_btn = QPushButton("Forgot Password")
        # forgot_pw_btn.clicked.connect() # todo: go to forgot pw screen
        layout.addWidget(forgot_pw_btn)


        self.setLayout(layout)

    def attempt_login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text()

        if self.authenticate(username, password):
            self.username = username
            self.accept()
        else:
            QMessageBox.warning(self, "Login Failed", "Invalid username or password!")
            self.password_input.clear()
            self.username_input.selectAll()

    def authenticate(self, username, password):
        # todo: replace with Azure DB built in authentication
        valid_users = {
            "admin": "admin123"
        }
        return username in valid_users and valid_users[username] == password

    def get_username(self):
        return self.username