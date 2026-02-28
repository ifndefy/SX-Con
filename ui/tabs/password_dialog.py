# ui/tabs/password_dialog.py
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt6.QtCore import Qt
from src.core.hash_password import hash_password
import utils.logger.logger as log

class PasswordChangeDialog(QDialog):
    """
    purpose: Dialog for changing user password
    author(s): Alexander Bubienko
    """
    def __init__(self, theme_manager, parent=None):
        super().__init__(parent)
        self.theme_manager = theme_manager
        self.setWindowTitle("Change Password")
        self.setFixedSize(400, 250)
        self.setModal(True)
        
        self.new_password = None
        self.setup_ui()
        
        if self.theme_manager:
            self.theme_manager.apply_default_theme(self)
    
    def setup_ui(self):
        """
        purpose: Initialize the password change UI
        author(s): Alexander Bubienko
        """
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("Enter New Password")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setObjectName("dialog_title")
        layout.addWidget(title)
        
        layout.addStretch()
        
        # New Password
        layout.addWidget(QLabel("New Password:"))
        self.new_password_input = QLineEdit()
        self.new_password_input.setPlaceholderText("Enter new password")
        self.new_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.new_password_input)
        
        # Confirm Password
        layout.addWidget(QLabel("Confirm Password:"))
        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setPlaceholderText("Confirm new password")
        self.confirm_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.confirm_password_input)
        
        layout.addStretch()
        
        # Buttons
        btn_layout = QHBoxLayout()
        
        self.update_btn = QPushButton("Update")
        self.update_btn.clicked.connect(self.on_update_clicked)
        btn_layout.addWidget(self.update_btn)
        
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(self.cancel_btn)
        
        layout.addLayout(btn_layout)
        
        self.setLayout(layout)
    
    def on_update_clicked(self):
        """
        purpose: Validate and accept the new password
        author(s): Alexander Bubienko
        """
        new_pass = self.new_password_input.text()
        confirm_pass = self.confirm_password_input.text()
        
        # Validation
        if not new_pass:
            QMessageBox.warning(self, "Invalid Input", "Password cannot be empty")
            return
            
        if new_pass != confirm_pass:
            QMessageBox.warning(self, "Password Mismatch", "Passwords do not match")
            self.confirm_password_input.clear()
            return
        
        self.new_password = new_pass
        self.accept()