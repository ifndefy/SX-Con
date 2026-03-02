import bcrypt
from PyQt6.QtWidgets import QDialog
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtWidgets import QLabel
from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtCore import Qt

import SPOT
from services.get_item_by_property import get_item_by_property
from services.get_property import get_property
from services.update_property import update_property
from src.core.hash_password import hash_password
from ui.prompts.password_dialog import PasswordChangeDialog
from ui.prompts.answer_sec_q import AnsSecQDialog
import utils.logger.logger as log

class ForgotPasswordScreen(QDialog):
    def __init__(self, theme_manager, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.theme_manager = theme_manager
        self.setWindowTitle("SX-Con - Password Reset")
        self.setFixedSize(500, 400)
        self.setModal(True)

        self.setup_ui()
        self.theme_manager.apply_default_theme(self)

    def setup_ui(self):
        layout = QVBoxLayout()

        # Title
        title = QLabel("SX-Con Password Reset")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setObjectName("title")
        layout.addWidget(title)

        # Username
        username_label = QLabel("Username:")
        username_label.setObjectName("label")
        layout.addWidget(username_label)
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter username")
        self.username_input.setObjectName("response_field")
        self.username_input.setMaxLength(30)

        layout.addWidget(self.username_input)
        layout.addStretch()

        req_btn = QPushButton("Request for Username")
        req_btn.clicked.connect(self.on_request_clicked)
        layout.addWidget(req_btn)

        self.setLayout(layout)

    def on_request_clicked(self):
        un = self.username_input.text().strip()
        if un is None or un == "":
            QMessageBox.critical(self, "Error", "Please enter a username")
            return
        if get_item_by_property("Entities", "user", "username", un):
            self._on_found_username(un)
        else:
            QMessageBox.critical(self, "Error", "Username not found")
            return

    def _on_found_username(self, username):
        user_item = get_item_by_property("Entities", "user", "username", username)
        self.user_id = user_item.get("user_id", '')
        user_qs = self.get_sec_questions(self.user_id)
        qa_dialog = AnsSecQDialog(self.theme_manager, self, self.user_id, user_qs)

        if qa_dialog.exec() == QDialog.DialogCode.Accepted:
            self.show_password_change_dialog()

    def show_password_change_dialog(self):
        """
        :purpose: Show dialog to enter and confirm new password
        :author(s): Alexander Bubienko
        """
        dialog = PasswordChangeDialog(self.theme_manager, self)

        if dialog.exec() == QDialog.DialogCode.Accepted and dialog.new_password:
            self.perform_password_update(dialog.new_password)

    def perform_password_update(self, new_password):
        """
        :purpose: Update the password in the database using update_property.py
        :author(s): Alexander Bubienko
        """
        username = self.username_input.text().strip()

        if not username:
            QMessageBox.critical(self, "Error", "No user logged in")
            return

        try:
            # Hash the new password
            hashed_password = hash_password(new_password)

            if hashed_password == "-1":
                QMessageBox.critical(self, "Error", "Failed to hash password")
                return

            # Get user ID
            if not self.user_id:
                QMessageBox.critical(self, "Error", "Could not determine user ID")
                return

            # Update password in database
            result = update_property(
                container_name='Entities',
                entity_type='user',
                entity_id=str(self.user_id),
                property_name='password',
                property_value=hashed_password
            )

            if result == 0:  # Success
                log.info(f"Password successfully changed for user: {username}")

                QMessageBox.information(self, "Success",
                                        "Password changed successfully.")
                self.close()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")
            log.error(f"Password update exception: {e}")

    def get_sec_questions(self, user_id):
        q_list = SPOT.QUESTIONS_LIST
        wanted_qs = []
        for q in q_list:
            if bcrypt.checkpw(q.encode('utf-8'), get_property("Entities", "q1_q", "user", user_id).encode('utf-8')):
                wanted_qs.append(q)
            if bcrypt.checkpw(q.encode('utf-8'), get_property("Entities", "q2_q", "user", user_id).encode('utf-8')):
                wanted_qs.append(q)
        return wanted_qs
