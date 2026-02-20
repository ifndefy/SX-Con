from PyQt6.QtWidgets import QDialog
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtWidgets import QLabel
from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtCore import Qt

from src import SPOT
from ui.forgot_pw import ForgotPasswordScreen
from src.core.authenticate import authenticate_password
from services.connect_database import db_connection


class LoginScreen(QDialog):
    """
    purpose: object to store all screen elements
    author(s): Joe Lee
    """
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
        """
        purpose: initializes the UI
        author(s): Joe Lee
        """
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
        rev = QLabel(SPOT.APP_VERSION)
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
        forgot_pw_btn.setObjectName("red_btn")
        forgot_pw_btn.clicked.connect(self.show_forgot_password_screen)
        layout.addWidget(forgot_pw_btn)

        self.setLayout(layout)

    def show_forgot_password_screen(self):
        """
        purpose: opens the forgot password screen in another window
        author(s): Joe Lee
        """
        forgot_pw_screen = ForgotPasswordScreen(self.theme_manager, self)
        forgot_pw_screen.exec()

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
        """
        purpose: requires the username and password to be valid in order to login
        author(s): Joe Lee, Alexander Bubienko
        """
        """"
        if username.strip() and password.strip():
            # pass in "testfail" username to intentionally cause fail -- for testing purposes
            if username.strip().lower() == "testfail":
                return False
            return True

        return False
        """
        try:
            
            if not username.strip() or not password.strip():
                return False
                
            # Connect to Users container
            users_container = db_connection.connect('Entities')
            
            # Query for user by username
            query = f"SELECT * FROM c WHERE c.username = '{username}'"
            users = list(users_container.query_items(
                query=query,
                enable_cross_partition_query=True
            ))
            
            if not users:
                print(f"No user found with username: {username}")
                return False
                
            # Get the stored hash and authenticate
            stored_hash = users[0].get('password')
            if not stored_hash:
                return False
                
            # Use the existing authenticate_password function
            result = authenticate_password(password, stored_hash)
            
            return result == "1"
            
        except Exception as e:
            print(f"Authentication error: {e}")
            return False