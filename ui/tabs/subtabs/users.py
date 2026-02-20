from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtWidgets import QComboBox
from PyQt6.QtWidgets import QHBoxLayout
from PyQt6.QtWidgets import QLabel
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtWidgets import QScrollArea
from PyQt6.QtWidgets import QWidget
from PyQt6.QtWidgets import QDialog
from PyQt6.QtWidgets import QMessageBox

from ui.tabs.base import BaseTab

from services.get_max_value import get_max_value
from services.insert_item import insert_item
from ui.core.prompts import hash_security_question_answer
from src.core.hash_password import hash_password
import utils.logger.logger as log
from services.message_bus import status_bar_instance

class UsersTab(BaseTab):
    def __init__(self, api_handler, db_connection):
        self.new_user_data = None
        self.update_btn = None
        self.users_layout = None
        self.create_btn = None
        self.users_section = []
        self.db_connection = db_connection
        super().__init__(api_handler, "users")

        self.questionList = [
            "What is your mother's maiden name?",
            "What color was your first car?",
            "Who was your best friend in the third grade?"
            # todo: add 2 more questions
        ]

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

        header_section = QHBoxLayout()
        title = QLabel("View Users") # Subtab header
        title.setObjectName("post_title")
        header_section.addWidget(title)
        header_section.addStretch() # Push to the left
        layout.addLayout(header_section) # Ends creation and adds header_section to window

        hr1 = QLabel() # HR Line to clear header
        hr1.setObjectName("hr")
        layout.addWidget(hr1)

        self.users_layout = QVBoxLayout() # Users container
        layout.addLayout(self.users_layout)

        users_section = QHBoxLayout()
        layout.addLayout(users_section)

        layout.addStretch()

        btn_section = QHBoxLayout()
        self.create_btn = QPushButton("Create New User")
        btn_section.addWidget(self.create_btn)
        self.create_btn.clicked.connect(self.create_new_user_prompt)

        btn_section.addStretch()

        self.update_btn = QPushButton("Update")
        btn_section.addWidget(self.update_btn)
        layout.addLayout(btn_section)

        # HR Line to separate buttons at the bottom
        hr3 = QLabel()
        hr3.setObjectName("hr")
        layout.addWidget(hr3)

        # Set up the scroll area
        scroll.setWidget(scroll_content)
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(scroll)

        self.setup_button_connections()

    def add_user_section(self):
        """
        :purpose: adds user items
        :return: None
        :author(s): Joe Lee
        """
        users_section = {}

        # Users section container
        section_widget = QWidget()
        section_layout = QVBoxLayout(section_widget)
        section_layout.setContentsMargins(0, 0, 0, 0)

        line1_layout = QHBoxLayout()
        line1_layout.addWidget(QLabel("UserID:"))
        user_id = QLineEdit()
        user_id.setObjectName("READ_ONLY")
        user_id.setPlaceholderText("30 CHAR")
        user_id.setReadOnly(True)
        user_id.setMaxLength(30)
        user_id.setFixedWidth(55)
        line1_layout.addWidget(user_id)

        line1_layout.addWidget(QLabel("Username:"))
        username = QLineEdit()
        username.setObjectName("READ_ONLY")
        username.setPlaceholderText("30 CHAR")
        username.setReadOnly(True)
        username.setMaxLength(30)
        username.setFixedWidth(265)
        line1_layout.addWidget(username)

        line1_layout.addStretch()

        # last consignment
        line1_layout.addWidget(QLabel("Last Consignment:"))
        last_con = QLineEdit()
        last_con.setObjectName("READ_ONLY")
        last_con.setPlaceholderText("datetime")
        last_con.setReadOnly(True)
        last_con.setMaxLength(30)
        last_con.setFixedWidth(190)
        line1_layout.addWidget(last_con)

        section_layout.addLayout(line1_layout)

        line2_layout = QHBoxLayout()
        line2_layout.addWidget(QLabel("First Name:"))
        first_name = QLineEdit()
        first_name.setObjectName("READ_ONLY")
        first_name.setPlaceholderText("30 CHAR")
        first_name.setReadOnly(True)
        first_name.setMaxLength(30)
        first_name.setFixedWidth(265)
        line2_layout.addWidget(first_name)

        # last name
        line2_layout.addWidget(QLabel("Last Name:"))
        last_name = QLineEdit()
        last_name.setObjectName("READ_ONLY")
        last_name.setPlaceholderText("OPEN")
        last_name.setReadOnly(True)
        last_name.setMaxLength(30)
        last_name.setFixedWidth(265)
        line2_layout.addWidget(last_name)

        line2_layout.addStretch()
        section_layout.addLayout(line2_layout)

        line3_layout = QHBoxLayout()

        view_btn = QPushButton("View")
        line3_layout.addWidget(view_btn)

        edit_btn = QPushButton("Edit")
        edit_btn.setObjectName("red_btn")
        line3_layout.addWidget(edit_btn)

        del_btn = QPushButton("Delete")
        del_btn.setObjectName("red_btn")
        line3_layout.addWidget(del_btn)

        section_layout.addLayout(line3_layout)

        hr = QLabel() # HR Line between entries
        hr.setObjectName("hr")
        section_layout.addWidget(hr)

        # Add to container
        self.users_layout.addWidget(section_widget)
        self.users_section.append(users_section)

    def fetch_on_clicked(self):
        """
        :purpose: calls fetch method and adds ticket sections
        :return: None
        :author(s): Joe Lee
        """
        users = self.fetch()
        if not users:
            log.error("No users found")
        else:
            for user in users:
                self.add_user_section()

    def fetch(self):
        """
        :purpose: fetches all users from Entities container
        :return: list of users
        :author(s): Joe Lee
        """
        try:
            container = self.db_connection.connect("Entities")

            query = """
            SELECT *
            FROM c
            WHERE c.type = 'user'
            ORDER BY c.username ASC
            """


            results = list(container.query_items(
                query=query,
                enable_cross_partition_query=True
            ))

            users = []
            for item in results:
                users.append({
                    'user_id': item.get('user_id'),
                    'username': item.get('username', ''),
                    'first_name': item.get('first_name', ''),
                    'last_name': item.get('last_name', '')
                })
            return users

        except Exception as e:
            log.error(f"Error fetching users: {e}")
            return []

    def create_new_user_prompt(self):
        '''
        :purpose: Sets up the UI and uses helper methods to create a user and insert it into the db
        :author(s): Colin Heinselman
        '''
        dialog = QDialog(self)
        dialog.setWindowTitle("Create New User")

        layout = QVBoxLayout(dialog)

        # Fields
        layout.addWidget(QLabel("Username:"))
        username_input = QLineEdit()
        username_input.setObjectName("username_input")
        layout.addWidget(username_input)

        layout.addWidget(QLabel("First Name:"))
        first_name_input = QLineEdit()
        first_name_input.setObjectName("first_name_input")
        layout.addWidget(first_name_input)

        layout.addWidget(QLabel("Last Name:"))
        last_name_input = QLineEdit()
        last_name_input.setObjectName("last_name_input")
        layout.addWidget(last_name_input)

        layout.addWidget(QLabel("Password:"))
        password_input = QLineEdit()
        password_input.setObjectName("password_input")
        layout.addWidget(password_input)

        # Security Questions
        prompt_label = QLabel("Security Question 1:")
        prompt_label.setObjectName("label")
        layout.addWidget(prompt_label)
        question1 = QComboBox()
        question1.addItems(self.questionList)
        question1.setObjectName("question1")
        question1.setCurrentIndex(-1)
        layout.addWidget(question1)


        res1_label = QLabel("Response for Question 1:")
        res1_label.setObjectName("label")
        layout.addWidget(res1_label)
        question1_response = QLineEdit()
        question1_response.setPlaceholderText("Question 1 Response")
        question1_response.setObjectName("response1")
        question1_response.setMaxLength(255)
        layout.addWidget(question1_response)

        hr2 = QLabel()
        hr2.setObjectName("hr")
        layout.addWidget(hr2)

        # Question 2
        prompt_label = QLabel("Security Question 2:")
        prompt_label.setObjectName("label")
        layout.addWidget(prompt_label)
        question2 = QComboBox()
        question2.addItems(self.questionList)
        question2.setObjectName("question2")
        question2.setCurrentIndex(-1)
        layout.addWidget(question2)

        res2_label = QLabel("Response for Question 2:")
        res2_label.setObjectName("label")
        layout.addWidget(res2_label)
        question2_response = QLineEdit()
        question2_response.setPlaceholderText("Question 2 Response")
        question2_response.setObjectName("response2")
        question2_response.setMaxLength(255)
        layout.addWidget(question2_response)

        layout.addStretch()

        # Buttons
        btn_layout = QHBoxLayout()
        create_btn = QPushButton("Create")
        cancel_btn = QPushButton("Cancel")

        btn_layout.addWidget(create_btn)
        btn_layout.addWidget(cancel_btn)
        layout.addLayout(btn_layout)

        # Connects
        create_btn.clicked.connect(self.on_create_clicked(dialog))
        cancel_btn.clicked.connect(dialog.reject)

        # Execute dialog
        result = dialog.exec()
        if result == QDialog.DialogCode.Accepted:
            self.handle_dialog_accepted(dialog)

    def setup_button_connections(self):
        """
        :purpose: links buttons with methods
        :return: None
        :author(s): Joe Lee
        """
        self.update_btn.clicked.connect(self.fetch_on_clicked)

    def on_create_clicked(self, dialog):
        """
        :Purpose: handles button initialization
        :Author(s): Joe Lee
        """
        def handler():
            if self.validate_user_data(dialog):
                dialog.accept()
        return handler

    def handle_dialog_accepted(self, dialog):
        """
        :Purpose: executes a sequence of events
        :Author(s): Joe Lee
        """
        self.new_user_data = self.gather_new_user_data(dialog)
        self.hash_security_q_and_a()
        insert_item("Entities", "user", self.new_user_data)

    def gather_new_user_data(self, dialog):
        """
        :Purpose: gathers user data from dialog's input fields
        :Method: passes in dialog then parses dialog for data
        :Author(s): Colin Heinselman, Joe Lee
        """
        raw_user_data = {
            "user_id": self.generate_new_user_id(),
            "username": dialog.findChild(QLineEdit, "username_input").text(),
            "first_name": dialog.findChild(QLineEdit, "first_name_input").text(),
            "last_name": dialog.findChild(QLineEdit, "last_name_input").text(),
            "password": hash_password(dialog.findChild(QLineEdit, "password_input").text()),
            "q1_q": dialog.findChild(QComboBox, "question1").currentText(),
            "q1_a": dialog.findChild(QLineEdit, "response1").text(),
            "q2_q": dialog.findChild(QComboBox, "question2").currentText(),
            "q2_a": dialog.findChild(QLineEdit, "response2").text(),
        }
        return raw_user_data

    def generate_new_user_id(self):
        """
        :Purpose: generates new user_id incrementing max value of database property by 1
        :Author(s): Joe Lee
        """
        new_id = get_max_value("Entities", "user_id") + 1
        return new_id

    def hash_security_q_and_a(self):
        """
        :Purpose: hashes user_data's security properties
        :Author(s): Colin Heinselman, Joe Lee
        """
        # Hash security questions and answers
        q_a_dict = {
            self.new_user_data["q1_q"]: self.new_user_data["q1_a"],
            self.new_user_data["q2_q"]: self.new_user_data["q2_a"],
        }

        q_dict_hashed = hash_security_question_answer(q_a_dict)
        q_keys = list(q_dict_hashed.keys())
        q_values = list(q_dict_hashed.values())
        self.new_user_data["q1_q"] = q_keys[0]
        self.new_user_data["q1_a"] = q_values[0]
        self.new_user_data["q2_q"] = q_keys[1]
        self.new_user_data["q2_a"] = q_values[1]

    def validate_user_data(self, dialog):
        """
        :Purpose: execute a series of validations on user data
        :Author(s): Colin Heinselman, Joe Lee
        """
        username = dialog.findChild(QLineEdit, "username_input").text()
        if not self.username_is_clean(username):
            return False
        if not self.validate_security_questions(dialog):
            return False
        return True

    def validate_security_questions(self, dialog):
        """
        :Purpose: validates security questions and responses within the dialog
        Author(s): Colin Heinselman
        """
        # Validate that both security questions are selected
        q1_q = dialog.findChild(QComboBox, "question1")
        q2_q = dialog.findChild(QComboBox, "question2")
        q1_a = dialog.findChild(QLineEdit, "response1")
        q2_a = dialog.findChild(QLineEdit, "response2")

        # Check both questions selected
        if q1_q.currentIndex() == -1 or q2_q.currentIndex() == -1:
            QMessageBox.warning(dialog, "Missing Information",
                                "Please select both security questions.")
            return False

        # Check questions are different
        if q1_q.currentIndex() == q2_q.currentIndex():
            QMessageBox.warning(dialog, "Invalid Selection",
                                "Please select two different security questions.")
            return False

        # Check responses not empty
        if not q1_a.text().strip() or not q2_a.text().strip():
            QMessageBox.warning(dialog, "Missing Information",
                                "Please provide responses for both security questions.")
            return False
        return True

    def username_is_clean(self, username: str) -> bool:
        """
        :purpose: Takes a username as input and determine if it includes any banned substrings
        :param username: The username to check
        :return: True if the username contains any banned substrings. False otherwise
        :author(s): Colin Heinselman
        """
        banned_substrings = [
            "administrator", "root", "system", "guest",
            "support", "help", "owner", "moderator",
            "login", "logout", "create", "delete", "config",
            "settings", "account", "profile", "username"
        ]

        lower_username = username.lower()  # make check case-insensitive
        for banned in banned_substrings:
            if banned in lower_username:
                return False
        return True
