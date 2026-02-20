from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QVBoxLayout, QTabWidget, QComboBox
from PyQt6.QtWidgets import QHBoxLayout
from PyQt6.QtWidgets import QLabel
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtWidgets import QScrollArea
from PyQt6.QtWidgets import QWidget
from PyQt6.QtWidgets import QDialog
from PyQt6.QtWidgets import QMessageBox

from ui.core.prompts import hash_security_question_answer
from ui.tabs.base import BaseTab
from ui.core import prompts

from src.core.hash_password import hash_password
from services.connect_database import db_connection
from services.create_user import create_user




class UsersTab(BaseTab):
    def __init__(self, api_handler, db_connection):
        self.tickets_section = []
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

        # Line 0 Creation
        header_section = QHBoxLayout()

        # Ticket Header
        title = QLabel("View Users")
        title.setObjectName("post_title")
        header_section.addWidget(title)

        # Push to the left
        header_section.addStretch()

        # Ends creation and adds header_section to window
        layout.addLayout(header_section)

        # HR Line between Vendor and Tickets sections
        hr1 = QLabel()
        hr1.setObjectName("hr")
        layout.addWidget(hr1)

        # Ticket Line 1: Tickets sections container
        self.tickets_layout = QVBoxLayout()

        layout.addLayout(self.tickets_layout)

        tickets_section = QHBoxLayout()

        layout.addLayout(tickets_section)
        layout.addStretch()

        vendor_section_row_3 = QHBoxLayout()
        self.create_btn = QPushButton("Create New User")
        vendor_section_row_3.addWidget(self.create_btn)
        self.create_btn.clicked.connect(self.create_new_user_prompt)

        vendor_section_row_3.addStretch()

        self.update_btn = QPushButton("Update")
        vendor_section_row_3.addWidget(self.update_btn)
        layout.addLayout(vendor_section_row_3)

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
        :purpose: adds ticket lines
        :return: None
        :author(s): Joe Lee
        """
        tickets_section = {}

        # Ticket section container
        section_widget = QWidget()
        section_layout = QVBoxLayout(section_widget)
        section_layout.setContentsMargins(0, 0, 0, 0)

        # Line 1: ticket_num + datetime + status + buttons
        line1_layout = QHBoxLayout()

        # user id
        line1_layout.addWidget(QLabel("UserID:"))
        user_id = QLineEdit()
        user_id.setObjectName("READ_ONLY")
        user_id.setPlaceholderText("30 CHAR")
        user_id.setReadOnly(True)
        user_id.setMaxLength(30)
        user_id.setFixedWidth(55)
        line1_layout.addWidget(user_id)

        # username
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
        # first name
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
        # btns
        self.view_btn = QPushButton("View")
        line3_layout.addWidget(self.view_btn)
        self.edit_btn = QPushButton("Edit")
        self.edit_btn.setObjectName("red_btn")
        line3_layout.addWidget(self.edit_btn)
        self.del_btn = QPushButton("Delete")
        self.del_btn.setObjectName("red_btn")
        line3_layout.addWidget(self.del_btn)

        section_layout.addLayout(line3_layout)

        # HR Line between Vendor and Product sections
        hr = QLabel()
        hr.setObjectName("hr")
        section_layout.addWidget(hr)

        # Add to container
        self.tickets_layout.addWidget(section_widget)
        self.tickets_section.append(tickets_section)

    def remove_ticket_section(self):
        """
        :purpose: removes and clears all ticket sections
        :return: None
        :author(s): Joe Lee
        """
        # Remove all widgets from the layout
        for i in reversed(range(self.tickets_layout.count())):
            widget = self.tickets_layout.itemAt(i).widget()
            if widget:
                self.tickets_layout.removeWidget(widget)
                widget.deleteLater()

        # Clear the tickets_section list
        self.tickets_section.clear()

        # Update status
        # self.status_label.setText("All tickets cleared")

    def fetch_on_clicked(self):
        """
        :purpose: calls fetch method and adds ticket sections
        :return: None
        :author(s): Joe Lee
        """
        self.remove_ticket_section()
        users = self.fetch()
        if not users:
            # self.status_label.setText("No users found")
            print("err") # delete when fixed
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
            SELECT c.id, c.username, c.first_name, c.last_name
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
                    'user_id': item['id'],
                    'username': item.get('username', ''),
                    'first_name': item.get('first_name', ''),
                    'last_name': item.get('last_name', '')
                })
            return users

        except Exception as e:
            print(f"Error fetching users: {e}")
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
        layout.addWidget(username_input)

        layout.addWidget(QLabel("First Name:"))
        first_name_input = QLineEdit()
        layout.addWidget(first_name_input)

        layout.addWidget(QLabel("Last Name:"))
        last_name_input = QLineEdit()
        layout.addWidget(last_name_input)

        layout.addWidget(QLabel("Password:"))
        password_input = QLineEdit()
        layout.addWidget(password_input)


        # Security Questions
        prompt_label = QLabel("Security Question 1:")
        prompt_label.setObjectName("label")
        layout.addWidget(prompt_label)
        question1 = QComboBox()
        question1.addItems(self.questionList)
        question1.setObjectName("prompt_label")
        question1.setCurrentIndex(-1)
        layout.addWidget(question1)


        res1_label = QLabel("Response for Question 1:")
        res1_label.setObjectName("label")
        layout.addWidget(res1_label)
        question1_response = QLineEdit()
        question1_response.setPlaceholderText("Question 1 Response")
        question1_response.setObjectName("response_field")
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
        question2.setObjectName("prompt_label")
        question2.setCurrentIndex(-1)
        layout.addWidget(question2)

        res2_label = QLabel("Response for Question 2:")
        res2_label.setObjectName("label")
        layout.addWidget(res2_label)
        question2_response = QLineEdit()
        question2_response.setPlaceholderText("Question 2 Response")
        question2_response.setObjectName("response_field")
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
        create_btn.clicked.connect(lambda: self.handle_create(dialog, username_input, first_name_input,
                                                              last_name_input, password_input, question1,
                                                    question1_response, question2, question2_response))
        cancel_btn.clicked.connect(dialog.reject)

        dialog.exec()


    def setup_button_connections(self):
        """
        :purpose: links buttons with methods
        :return: None
        :author(s): Joe Lee
        """
        self.update_btn.clicked.connect(self.fetch_on_clicked)


    def handle_create(self, dialog, username_input, first_name_input,
                      last_name_input, password_input, question1, question1_response,
                      question2, question2_response):
        """
        :purpose: links buttons with methods. When user clicks "Create" button, this method will execute to create a new user
        :return: None.
        :param dialog: The dialog window that triggered the "create" action
        :param username_input: The username input
        :param first_name_input: The first name input
        :param last_name_input: The last name input
        :param password_input: The password input
        :param question1: The first security question selected
        :param question1_response: The input field containing the user's response to question1
        :param question2: The second security question selected
        :param question2_response: The input field containing the user's response to question2
        :author(s): Colin Heinselman
        """

        raw_user_data = self.extract_raw_user_data(dialog, username_input, first_name_input,
                      last_name_input, password_input, question1, question1_response,
                      question2, question2_response)

        # Ensures that all prompts are answered
        prompts_valid = self.validate_prompts(question1, question2, raw_user_data)
        if not prompts_valid:
            return

        user_insertion_status = self.insert_user_data(raw_user_data)
        if user_insertion_status == 0:
            dialog.accept()
        else:
            self.invalid_user_message(dialog, user_insertion_status)


    def validate_prompts(self, question1, question2, user_data):
        # Ensure all fields have input data. Returns are simply used to properly exit the function and ensure UI works
        # Validate that both security questions are selected
        if question1.currentIndex() == -1 or question2.currentIndex() == -1:
            QMessageBox.warning(self, "Missing Information", "Please select both security questions.")
            return False
        # Validate that security questions are different
        elif question1.currentIndex() == question2.currentIndex():
            QMessageBox.warning(self, "Invalid Selection", "Please select two different security questions.")
            return False
        # Validate that response fields have input

        elif user_data["q1_a"] == "" or user_data["q2_a"] == "":
            QMessageBox.warning(self, "Missing Information", "Please provide responses for both security questions.")
            return False
        elif not user_data["username"]:
            QMessageBox.warning(self, "Missing Information", "Please provide username.")
            return False
        elif not user_data["first_name"]:
            QMessageBox.warning(self, "Missing Information", "Please provide first name.")
            return False
        elif not user_data["last_name"]:
            QMessageBox.warning(self, "Missing Information", "Please provide last name.")
            return False
        elif not user_data["password"]:
            QMessageBox.warning(self, "Missing Information", "Please provide password.")
            return False

        return True

    def hash_security_q_and_a(self, user_data):
        # Hash security questions and answers
        q_a_dict = {
            user_data["q1_q"]: user_data["q1_a"],
            user_data["q2_q"]: user_data["q2_a"],
        }

        q_dict_hashed = hash_security_question_answer(q_a_dict)
        q_keys = list(q_dict_hashed.keys())
        q_values = list(q_dict_hashed.values())

        return q_keys, q_values

    def insert_user_data(self, raw_user_data):

        # Hash security questions and answers
        q_keys, q_values = self.hash_security_q_and_a(raw_user_data)

        user_data = {
            "username": raw_user_data["username"],
            "first_name": raw_user_data["first_name"],
            "last_name": raw_user_data["last_name"],
            "password": hash_password(raw_user_data["password"]),
            "q1_q": q_keys[0],
            "q1_a": q_values[0],
            "q2_q": q_keys[1],
            "q2_a": q_values[1],
            "admin": False
        }

        return create_user(user_data)


    def extract_raw_user_data(self, dialog, username_input, first_name_input,
                      last_name_input, password_input, question1, question1_response,
                      question2, question2_response):

        raw_user_data = {
            "username": username_input.text().strip(),
            "first_name": first_name_input.text().strip(),
            "last_name": last_name_input.text().strip(),
            "password": password_input.text().strip(),
            "q1_q": question1.currentText().strip(),
            "q1_a": question1_response.text().strip(),
            "q2_q": question2.currentText().strip(),
            "q2_a": question2_response.text().strip(),
            "admin": False
        }
        return raw_user_data

    def invalid_user_message(self, dialog, user_insertion_status):
        reason = ""
        if user_insertion_status == -1:
            reason = "User is missing required fields"
        elif user_insertion_status == -2:
            reason = ("Invalid Username. Ensure your username meets all of the following requirements:\n"
                      " - Doesn't contain any banned characters: (#, *, /, ^, etc.)\n"
                      " - Doesn't contain any banned words: (admin, test, system, etc.)\n"
                      " - Is at least 3 characters long.")

        QMessageBox.warning(self, "Invalid User Information", reason)