from PyQt6.QtWidgets import QComboBox
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtWidgets import QHBoxLayout
from PyQt6.QtWidgets import QLabel
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtWidgets import QScrollArea
from PyQt6.QtWidgets import QWidget
from PyQt6.QtWidgets import QDialog
from PyQt6.QtWidgets import QMessageBox

from ui.core.theme_manager import ThemeManager
from ui.tabs.base import BaseTab
from ui.prompts.login import LoginScreen
from src.user import current_user
from services.update_property import update_property
from ui.prompts.password_dialog import PasswordChangeDialog
from src.core.hash_password import hash_password
import utils.logger.logger as log

class SettingsTab(BaseTab):
    def __init__(self, api_handler, main_window=None):
        self.save_btn = None
        self.load_btn = None
        self.theme_dropdown_menu = None
        self.ticket_counter = None
        self.tickets_layout = None
        self.current_username_input = None
        self.change_username_btn = None
        self.theme_manager = ThemeManager()
        self.main_window = main_window

        super().__init__(api_handler, "settings")

    def setup_ui(self):
        """
        :purpose: initializes the "Create New Record" tab
        :return: None
        :author(s): Joe Lee
        """
        # Enable scrolling for when the content exceeds the height of the window
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        layout = QVBoxLayout(scroll_content)

        # Line 0 Creation
        theme_layout = QHBoxLayout()

        # Ticket Header
        title = QLabel("Themes:")
        title.setObjectName("post_title")
        theme_layout.addWidget(title)

        self.theme_dropdown_menu = QComboBox()

        themes = self.theme_manager.get_available_themes()
        self.theme_dropdown_menu.addItems(themes)
        self.theme_dropdown_menu.setCurrentText(self.theme_manager.get_current_theme())
        self.theme_dropdown_menu.currentTextChanged.connect(self.on_theme_changed)
        theme_layout.addWidget(self.theme_dropdown_menu)

        theme_layout.addStretch()

        layout.addLayout(theme_layout)

        # HR Line
        hr0 = QLabel()
        hr0.setObjectName("hr")
        layout.addWidget(hr0)

        user_layout_line_0 = QHBoxLayout()
        user_title = QLabel("Username:")
        user_title.setObjectName("post_title")
        user_layout_line_0.addWidget(user_title)

        self.current_username_input = QLineEdit("test")
        self.current_username_input.setText(current_user.get_username() or "Not logged in")
        self.current_username_input.setReadOnly(True)
        user_layout_line_0.addWidget(self.current_username_input)

        self.change_username_btn = QPushButton("Change Username")
        user_layout_line_0.addWidget(self.change_username_btn)

        layout.addLayout(user_layout_line_0)

        # HR Line
        hr1 = QLabel()
        hr1.setObjectName("hr")
        layout.addWidget(hr1)

        pw_layout_line_0 = QHBoxLayout()
        pw_title = QLabel("Password:")
        pw_title.setObjectName("post_title")
        pw_layout_line_0.addWidget(pw_title)

        self.change_pw_btn = QPushButton("Change Password")
        pw_layout_line_0.addWidget(self.change_pw_btn)

        layout.addLayout(pw_layout_line_0)

        # HR Line
        hr2 = QLabel()
        hr2.setObjectName("hr")
        layout.addWidget(hr2)

        qa_layout_line_0 = QHBoxLayout()
        qa_title = QLabel("Security Questions:")
        qa_title.setObjectName("post_title")
        qa_layout_line_0.addWidget(qa_title)

        layout.addLayout(qa_layout_line_0)

        qa_layout_line_1 = QHBoxLayout()
        qa_1 = QLabel("Question 1:")
        qa_1_input = QLineEdit()
        qa_1_input.setReadOnly(True)
        qa_layout_line_1.addWidget(qa_1)
        qa_layout_line_1.addWidget(qa_1_input)

        layout.addLayout(qa_layout_line_1)

        qa_layout_line_2 = QHBoxLayout()
        qa_2 = QLabel("Answer 1:")
        qa_2_input = QLineEdit()
        qa_2_input.setReadOnly(True)
        qa_layout_line_2.addWidget(qa_2)
        qa_layout_line_2.addWidget(qa_2_input)

        layout.addLayout(qa_layout_line_2)

        qa_layout_line_3 = QHBoxLayout()
        qa_3 = QLabel("Question 2:")
        qa_3_input = QLineEdit()
        qa_3_input.setReadOnly(True)
        qa_layout_line_3.addWidget(qa_3)
        qa_layout_line_3.addWidget(qa_3_input)

        layout.addLayout(qa_layout_line_3)

        qa_layout_line_4 = QHBoxLayout()
        qa_4 = QLabel("Answer 2:")
        qa_4_input = QLineEdit()
        qa_4_input.setReadOnly(True)
        qa_layout_line_4.addWidget(qa_4)
        qa_layout_line_4.addWidget(qa_4_input)

        layout.addLayout(qa_layout_line_4)

        q_line_5 = QHBoxLayout()
        self.change_qa_btn = QPushButton("Change Q/A")
        q_line_5.addWidget(self.change_qa_btn)

        layout.addLayout(q_line_5)

        # Push buttons to the bottom
        layout.addStretch()

        # HR Line to separate buttons at the bottom
        hr3 = QLabel()
        hr3.setObjectName("hr")
        layout.addWidget(hr3)

        btn_layout = QHBoxLayout()
        self.load_btn = QPushButton("Load Settings")
        layout.addWidget(self.load_btn)
        btn_layout.addWidget(self.load_btn)

        btn_layout.addStretch()

        self.save_btn = QPushButton("Save Settings")
        layout.addWidget(self.save_btn)
        btn_layout.addWidget(self.save_btn)

        layout.addLayout(btn_layout)

        # HR Line to separate buttons at the bottom
        hr4 = QLabel()
        hr4.setObjectName("hr")
        layout.addWidget(hr4)

        # Set up the scroll area
        scroll.setWidget(scroll_content)
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(scroll)

        self.setup_button_connections()

    def on_theme_changed(self, theme_name):
        self.theme_manager.apply_theme(theme_name, self)
        log.info(f"Changed theme to {theme_name}")

    def setup_button_connections(self):
        """
        :purpose: links buttons with methods
        :return: None
        :author(s): Joe Lee, Alexander Bubienko
        """

        self.change_username_btn.clicked.connect(self.on_change_username_clicked)

        if hasattr(self, 'change_pw_btn'):
            self.change_pw_btn.clicked.connect(self.on_change_password_clicked)
            log.info("Change password button connected")

    def verify_credentials_for_password_change(self):
        """
        :purpose: Show login dialog to verify user credentials before allowing password change
        :author(s): Alexander Bubienko
        """
        login_dialog = LoginScreen(self.theme_manager, self)
        login_dialog.setWindowTitle("Verify Credentials")
        
        if login_dialog.exec() == QDialog.DialogCode.Accepted:
            # Credentials verified - open password change dialog
            self.show_password_change_dialog()
        else:
            QMessageBox.warning(self, "Verification Failed", 
                            "Invalid credentials. Password cannot be changed.")
            log.warning("Password change verification failed")

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
        username = current_user.get_username()
        
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
            user_id = self.get_user_id_from_username(username)
            
            if not user_id:
                QMessageBox.critical(self, "Error", "Could not determine user ID")
                return
            
            # Update password in database
            result = update_property(
                container_name='Entities',
                entity_type='user',
                entity_id=str(user_id),
                property_name='password',
                property_value=hashed_password
            )
            
            if result == 0:  # Success
                log.info(f"Password successfully changed for user: {username}")
                
                QMessageBox.information(self, "Success", 
                                    "Password changed successfully. You will now be logged out.")
                
                # Log out the user
                if hasattr(self, 'main_window') and self.main_window:
                    self.main_window.logout()
                else:
                    parent = self.parent()
                    while parent:
                        if hasattr(parent, 'logout'):
                            parent.logout()
                            break
                        parent = parent.parent()
            else:
                QMessageBox.critical(self, "Error", "Failed to update password in database")
                log.error(f"Password update failed with result: {result}")
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")
            log.error(f"Password update exception: {e}")

    def on_change_password_clicked(self):
        """
        :purpose: Handle password change button click
        :author(s): Alexander Bubienko
        """
        self.verify_credentials_for_password_change()

    def on_change_username_clicked(self):
        """
        :purpose: Handle username change button clicks (toggles between Change/Update modes)
        :author(s): Alexander Bubienko
        """
        if self.current_username_input.isReadOnly():
            # Currently in "Change Username" mode - verify credentials first
            self.verify_credentials_for_username_change()
        else:
            # Currently in "Update" mode - perform the username update
            self.perform_username_update()

    def verify_credentials_for_username_change(self):
        """
        :purpose: Show login dialog to verify user credentials before allowing username change
        :author(s): Alexander Bubienko
        """
        # Create a login dialog for verification
        login_dialog = LoginScreen(self.theme_manager, self)
        
        # Modify the dialog appearance to show it's for verification
        login_dialog.setWindowTitle("Verify Credentials")
        
        # Show the dialog and check if authentication succeeded
        if login_dialog.exec() == QDialog.DialogCode.Accepted:
            # Credentials verified - enable username editing
            self.current_username_input.setReadOnly(False)
            self.current_username_input.setFocus()
            self.current_username_input.selectAll()
            self.change_username_btn.setText("Update")
            log.info("Credentials verified, username edit enabled")
        else:
            # Verification failed
            QMessageBox.warning(self, "Verification Failed", 
                               "Invalid credentials. Username cannot be changed.")
            log.warning("Username change verification failed")

    def perform_username_update(self):
        """
        :purpose: Update the username in the database using update_property.py
        :author(s): Alexander Bubienko
        """
        new_username = self.current_username_input.text().strip()
        old_username = current_user.get_username()
        
        # Validate new username
        if not new_username:
            QMessageBox.warning(self, "Invalid Input", "Username cannot be empty")
            return
            
        if new_username == old_username:
            QMessageBox.information(self, "No Change", "New username is the same as current username")
            # Reset to read-only mode
            self.cancel_username_update()
            return
        
        confirm = QMessageBox.question(
            self, 
            "Confirm Username Change",
            f"Are you sure you want to change your username from '{old_username}' to '{new_username}'?\n\n"
            "You will be logged out after this change.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if confirm != QMessageBox.StandardButton.Yes:
            return
        
        try:
            user_id = self.get_user_id_from_username(old_username)
            
            if not user_id:
                QMessageBox.critical(self, "Error", "Could not determine user ID")
                return
            
            # Use update_property to change the username
            result = update_property(
                container_name='Entities',
                entity_type='user',
                entity_id=str(user_id),
                property_name='username',
                property_value=new_username
            )
            
            if result == 0:  # Success
                log.info(f"Username successfully changed from {old_username} to {new_username}")
                
                # Update the user class with new username
                current_user.set_user(new_username, current_user.is_admin())
                
                QMessageBox.information(self, "Success", 
                                    "Username changed successfully. You will now be logged out.")
                
                if hasattr(self, 'main_window') and self.main_window:
                    self.main_window.logout()
                else:
                    # If no main_window reference, try to find it
                    parent = self.parent()
                    while parent:
                        if hasattr(parent, 'logout'):
                            parent.logout()
                            break
                        parent = parent.parent()
                
            else:
                QMessageBox.critical(self, "Error", "Failed to update username in database")
                log.error(f"Username update failed with result: {result}")
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")
            log.error(f"Username update exception: {e}")

    def get_user_id_from_username(self, username):
        """
        :purpose: Helper method to get user ID from username
        :author(s): Alexander Bubienko
        """
        try:
            from services.connect_database import db_connection
            container = db_connection.connect('Entities')
            
            # Query for user by username
            query = f"SELECT * FROM c WHERE c.username = '{username}' AND c.type = 'user'"
            users = list(container.query_items(
                query=query,
                enable_cross_partition_query=True
            ))
            
            if users:
                return users[0].get('user_id') or users[0].get('id')
            return None
        except Exception as e:
            log.error(f"Error getting user ID: {e}")
            return None

    def cancel_username_update(self):
        """
        :purpose: Cancel username update and return to read-only state
        :author(s): Alexander Bubienko
        """
        self.current_username_input.setText(current_user.get_username() or "")
        self.current_username_input.setReadOnly(True)
        self.change_username_btn.setText("Change Username")