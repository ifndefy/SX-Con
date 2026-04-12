from PyQt6.QtCore import QRegularExpression
from PyQt6.QtGui import QRegularExpressionValidator
from PyQt6.QtWidgets import QComboBox
from PyQt6.QtWidgets import QFrame
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtWidgets import QHBoxLayout
from PyQt6.QtWidgets import QLabel
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtWidgets import QScrollArea
from PyQt6.QtWidgets import QWidget
from PyQt6.QtWidgets import QDialog
from PyQt6.QtWidgets import QMessageBox

import json

from ui.prompts.security_dialog import SecurityQuestionsDialog
from ui.tabs.base import BaseTab
from ui.prompts.login import LoginScreen
from ui.prompts.password_dialog import PasswordChangeDialog
from src.user import current_user

from services.get_property import get_property
from services.update_property import update_property
from src.core.hash_password import hash_password
from utils.core.json_helpers import json_to_dict
from utils.core.import_doc import import_offline_records

import utils.logger.logger as log

class SettingsTab(BaseTab):
    def __init__(self, api_handler, theme_manager, app, main_window=None):
        self.save_btn = None
        self.load_btn = None
        self.sync_btn = None
        self.theme_dropdown_menu = None
        self.ticket_counter = None
        self.tickets_layout = None
        self.current_username_input = None
        self.change_username_btn = None
        self.main_window = main_window
        self.theme_manager = theme_manager
        self.app = app

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
        hr0 = QFrame()
        hr0.setFrameShape(QFrame.Shape.HLine)
        hr0.setFrameShadow(QFrame.Shadow.Sunken)
        hr0.setObjectName("hr")
        layout.addWidget(hr0)

        user_layout_line_0 = QHBoxLayout()
        user_title = QLabel("Username:")
        user_title.setObjectName("post_title")
        user_layout_line_0.addWidget(user_title)

        self.current_username_input = QLineEdit("test")
        self.current_username_input.setText(current_user.get_username() or "Not logged in")
        alpha_validator = QRegularExpressionValidator(QRegularExpression("[A-Za-z ]+"))
        self.current_username_input.setValidator(alpha_validator)
        self.current_username_input.setReadOnly(True)
        user_layout_line_0.addWidget(self.current_username_input)

        self.change_username_btn = QPushButton("Change Username")
        user_layout_line_0.addWidget(self.change_username_btn)

        layout.addLayout(user_layout_line_0)

        # HR Line
        hr1 = QFrame()
        hr1.setFrameShape(QFrame.Shape.HLine)
        hr1.setFrameShadow(QFrame.Shadow.Sunken)
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
        hr2 = QFrame()
        hr2.setFrameShape(QFrame.Shape.HLine)
        hr2.setFrameShadow(QFrame.Shadow.Sunken)
        hr2.setObjectName("hr")
        layout.addWidget(hr2)

        q_line = QHBoxLayout()
        qa_layout_line_0 = QLabel("Security Questions:")
        qa_layout_line_0.setObjectName("post_title")
        q_line.addWidget(qa_layout_line_0)

        self.change_qa_btn = QPushButton("Change Q/A")
        q_line.addWidget(self.change_qa_btn)

        layout.addLayout(q_line)

        # Push buttons to the bottom
        layout.addStretch()

        # HR Line to separate buttons at the bottom
        hr3 = QFrame()
        hr3.setFrameShape(QFrame.Shape.HLine)
        hr3.setFrameShadow(QFrame.Shadow.Sunken)
        hr3.setObjectName("hr")
        layout.addWidget(hr3)

        self.sync_btn = QPushButton("Sync Offline Tickets")
        layout.addWidget(self.sync_btn, 1)

        # Set up the scroll area
        scroll.setWidget(scroll_content)
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(scroll)

        btn_layout = QHBoxLayout()
        self.load_btn = QPushButton("Load Settings")
        btn_layout.addWidget(self.load_btn)

        self.save_btn = QPushButton("Save Settings")
        btn_layout.addWidget(self.save_btn)

        main_layout.addLayout(btn_layout)

        self.setup_button_connections()
        self.load_user_preferences(silent=True)

    def on_theme_changed(self, theme_name):
        """
        :Purpose: Logs when theme is changed
        :Author(s): Joe Lee
        """
        self.theme_manager.apply_theme(theme_name, self.app)
        log.info(f"Changed theme to {theme_name}")

    def setup_button_connections(self):
        """
        :purpose: links buttons with methods
        :return: None
        :author(s): Joe Lee, Alexander Bubienko
        """
        self.change_username_btn.clicked.connect(self.on_change_username_clicked)
        self.change_pw_btn.clicked.connect(self.on_change_password_clicked)
        self.change_qa_btn.clicked.connect(self.on_change_qa_clicked)
        self.sync_btn.clicked.connect(self.on_sync_clicked)
        self.load_btn.clicked.connect(self.load_user_preferences)
        self.save_btn.clicked.connect(self.save_user_preferences)

    def on_sync_clicked(self):
        """
        :Purpose: uploads offline tickets to the database
        :Author(s): Joe Lee
        """
        try:
            import_offline_records()
            QMessageBox.information(self, "Sync Complete", "Offline records synced successfully.")
        except Exception as e:
            log.error(f"Sync failed: {e}")
            QMessageBox.critical(self, "Sync Failed", f"Failed to sync offline records:\n\n{e}")

    def on_change_qa_clicked(self):
        """
        :Purpose: handle security qa hange button click
        :Author(s): Joe Lee
        """
        if self.verify_credentials_for_cred_change():
            self.show_qa_change_dialog()
        else:
            QMessageBox.warning(self, "Verification Failed",
                                "Invalid credentials. Security Questions and Answers cannot be changed.")
            log.warning("Security QA change verification failed")

    def show_qa_change_dialog(self):
        """
        :purpose: Show dialog to enter and confirm new password
        :author(s): Alexander Bubienko, Joe Lee
        """
        dialog = SecurityQuestionsDialog(self.theme_manager, self)

        if dialog.exec() == QDialog.DialogCode.Accepted and dialog.hashed_questions_answers:
            self.perform_qa_update(dialog.hashed_questions_answers)

    def perform_qa_update(self, hashed_qa):
        """
        :Purpose: wrap user_property to update the user's security q and a
        :param hashed_qa: hashed questions answers
        :Author(s): Joe Lee
        """
        username = current_user.get_username()
        if not username:
            QMessageBox.critical(self, "Unknown Username", "User not logged in")
            return
        try:
            user_id = self.get_user_id_from_username(username)
            if not user_id:
                QMessageBox.critical(self, "Error", f"Count not find user_id for {username}")
                return
            updated = True
            for p_name, p_value in hashed_qa.items():
                result = update_property(
                    container_name="Entities",
                    entity_type="user",
                    entity_id=str(user_id),
                    property_name=p_name,
                    property_value=p_value
                )
                if result != 0:
                    log.error(f"Failed to update {p_name} for user {username}")
                    updated = False

            if updated:
                log.info(f"Successfully updated Security Questions and Answers for {username}")
                QMessageBox.information(self, "Success", f"Successfully updated Security Questions and Answers for {username}")
            else:
                QMessageBox.critical(self, "Error", f"Failed to update Security Questions and Answers for {username}")
        except Exception as e:
            log.error(f"Could not update user security questions and answers {e}")
            QMessageBox.critical(self, "Error", f"Failed to update user security questions and answers {e}")

    def on_change_password_clicked(self):
        """
        :purpose: Handle password change button click
        :author(s): Alexander Bubienko, Joe Lee
        """
        if self.verify_credentials_for_cred_change():
            self.show_password_change_dialog()
        else:
            QMessageBox.warning(self, "Verification Failed",
                                "Invalid credentials. Password cannot be changed.")
            log.warning("Password change verification failed")

    def verify_credentials_for_cred_change(self):
        """
        :purpose: Show login dialog to verify user credentials before allowing credential changes
        :author(s): Alexander Bubienko, Joe Lee
        """
        login_dialog = LoginScreen(self.theme_manager, self)
        login_dialog.setWindowTitle("Verify Credentials")
        
        if login_dialog.exec() == QDialog.DialogCode.Accepted:
            return True
        return False

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
            query = f"SELECT * FROM c WHERE c.username = '{username}' AND c.entity_type = 'user'"
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

    def load_user_preferences(self, silent=False):
        """
        Purpose: loads the user's preferences from DB, defaults to Super if not found
        Author(s): Joe Lee
        """
        user_id = self._get_current_user_id()
        if user_id is None:
            log.error(f"Failed to find user id")
            self.theme_manager.apply_default_theme(self.app)
            return

        user_prefs = self._get_user_preferences(user_id)
        if user_prefs is None:
            self.theme_manager.apply_default_theme(self.app)
            if not silent:
                QMessageBox.information(self, "Settings Loaded", "No preference found. \nPlease save a preference first.")
                return

        preferences = json_to_dict(user_prefs)
        self._apply_theme_from_preferences(preferences)

        if not silent:
            QMessageBox.information(self, "Settings Loaded", "Preferences loaded successfully.")

    def _get_current_user_id(self):
        """
        :Purpose: Wraps get_user_id_from_username to retrieve current user ID
        :Return: User ID
        :Author(s): Joe Lee
        """
        username = current_user.get_username()
        if not username:
            QMessageBox.warning(self, "Not Logged In", "No user is currently logged in.")
            return None

        user_id = self.get_user_id_from_username(username)
        if not user_id:
            QMessageBox.critical(self, "Error", "Could not determine user ID.")
            return None

        return user_id

    def _get_user_preferences(self, user_id):
        """
        :Purpose: Wraps get_property to retrieve user's preferences json
        :param: user_id: User ID
        :Return: user pref
        """
        try:
            preferences_json = get_property(
                container_name='Entities',
                attribute='preferences',
                entity_type='user',
                id_value=str(user_id)
            )
            # get_property returns "-1" on error, otherwise the string value
            if preferences_json == "-1":
                log.warning(f"No preferences found for user ID {user_id}; Save a preference first.")
                return None
            return preferences_json
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to fetch preferences: {str(e)}")
            log.error(f"Error in _fetch_preferences_json: {e}")
            return None

    @staticmethod
    def json_to_dict(json_string):
        """
        :Purpose: parse a json string and converts it into a dictionary
        :param: preferences_json: json string to parse
        :Return: dictionary of input json string
        :Author(s): Joe Lee
        """
        try:
            return json.loads(json_string)
        except json.JSONDecodeError:
            log.error(f"Invalid JSON string: {json_string}. Resetting to empty.")
            return {}

    def _apply_theme_from_preferences(self, preferences):
        """
        :Purpose: Applies theme from preferences
        :param: preferences: preferences dictionary
        :Author(s): Joe Lee
        """
        theme = preferences.get('theme')
        if theme and theme in self.theme_manager.get_available_themes():
            self.theme_dropdown_menu.blockSignals(True)
            self.theme_dropdown_menu.setCurrentText(theme)
            self.theme_dropdown_menu.blockSignals(False)
            self.theme_manager.apply_theme(theme, self.app)
            log.info(f"Applied theme '{theme}' from preferences.")
        else:
            log.info("No valid theme preference found. Applying default theme.")
            self.theme_dropdown_menu.blockSignals(True)
            self.theme_dropdown_menu.setCurrentText("Super")
            self.theme_dropdown_menu.blockSignals(False)
            self.theme_manager.apply_default_theme(self.app)

    def save_user_preferences(self):
        """
        :Purpose: Saves user preferences to database
        :Author(s): Joe Lee
        """
        user_id = self._get_current_user_id()
        if user_id is None:
            log.error(f"Failed to find user id")
            return

        preferences_json = self._build_preferences_json()
        if self._save_preferences_to_db(user_id, preferences_json):
            QMessageBox.information(self, "Success", "Settings saved successfully.")
        else:
            QMessageBox.critical(self, "Error", "Failed to save settings to database.")

    def _build_preferences_json(self):
        """
        :Purpose: Builds preferences json string
        :Author(s): Joe Lee
        """
        preferences = {
            'theme': self.theme_dropdown_menu.currentText()
            # place additional settings here
        }
        return json.dumps(preferences)

    def _save_preferences_to_db(self, user_id, preferences_json):
        """
        :Purpose: wraps update_property to update preferences property of user item
        :param: user_id: User ID
        :param: preferences_json: json string to update
        :Author(s): Joe Lee
        """
        try:
            result = update_property(
                container_name='Entities',
                entity_type='user',
                entity_id=str(user_id),
                property_name='preferences',
                property_value=preferences_json
            )
            if result == 0:
                log.info(f"Preferences saved for user ID {user_id}: {preferences_json}")
                return True
            else:
                log.error(f"Save preferences failed with result: {result}")
                return False
        except Exception as e:
            log.error(f"Save preferences exception: {e}")
            return False