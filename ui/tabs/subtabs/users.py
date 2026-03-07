from PyQt6.QtCore import QTimer
from PyQt6.QtCore import QRegularExpression
from PyQt6.QtGui import QIntValidator
from PyQt6.QtGui import QRegularExpressionValidator
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtWidgets import QFrame
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
from src import SPOT

from datetime import datetime

from services.get_max_value import get_max_value
from services.insert_item import insert_item
from src.core.hash_qa import hash_security_question_answer
from src.core.hash_password import hash_password
import utils.logger.logger as log
from services.message_bus import status_bar_instance

class UsersTab(BaseTab):
    def __init__(self, api_handler, db_connection):
        self.new_user_data = None
        self.users_layout = None
        self.create_btn = None
        self.users_section = []
        self.db_connection = db_connection
        super().__init__(api_handler, "users")

        self.questionList = SPOT.QUESTIONS_LIST

        self.search_timer = QTimer()
        self.search_timer.setSingleShot(True)
        self.search_timer.timeout.connect(self.build_and_search)

    def setup_ui(self):
        """
        :purpose: initializes the "Create New Record" tab
        :return: None
        :author(s): Joe Lee
        """
        background = QVBoxLayout(self)

        main_layout_widget = QWidget()
        main_layout = QVBoxLayout(main_layout_widget)

        header_section = QHBoxLayout()
        title = QLabel("View Users")  # Subtab header
        title.setObjectName("post_title")
        header_section.addWidget(title)
        header_section.addStretch()  # Push to the left

        self.create_btn = QPushButton("Create New User")
        self.create_btn.setFixedWidth(200)
        header_section.addWidget(self.create_btn)

        main_layout.addLayout(header_section)  # Ends creation and adds header_section to window

        hr1 = QFrame()
        hr1.setFrameShape(QFrame.Shape.HLine)
        hr1.setFrameShadow(QFrame.Shadow.Sunken)
        hr1.setObjectName("hr")
        main_layout.addWidget(hr1)

        search_section_row_1 = QHBoxLayout()

        search_section_row_1.addWidget(QLabel("UserID:"))
        self.user_id_input = QLineEdit()
        self.user_id_input.setPlaceholderText("U ID")
        self.user_id_input.setMaxLength(30)
        self.user_id_input.setFixedWidth(55)
        self.user_id_input.setValidator(QIntValidator(0, 9999, self))
        self.user_id_input.textChanged.connect(self.on_search_input_changed)
        search_section_row_1.addWidget(self.user_id_input)

        search_section_row_1.addWidget(QLabel("Username:"))
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        self.username_input.setMaxLength(30)
        self.username_input.setFixedWidth(265)
        alpha_validator = QRegularExpressionValidator(QRegularExpression("[A-Za-z ]+"))
        self.username_input.setValidator(alpha_validator)
        self.username_input.textChanged.connect(self.on_search_input_changed)
        search_section_row_1.addWidget(self.username_input)

        search_section_row_1.addStretch()

        search_section_row_1.addWidget(QLabel("Last Consignment:"))
        self.last_consignment_input = QLineEdit()
        self.last_consignment_input.setPlaceholderText("Last Consignment")
        self.last_consignment_input.setMaxLength(30)
        self.last_consignment_input.setFixedWidth(265)
        self.last_consignment_input.textChanged.connect(self.on_search_input_changed)
        search_section_row_1.addWidget(self.last_consignment_input)

        main_layout.addLayout(search_section_row_1)

        search_section_row_2 = QHBoxLayout()

        search_section_row_2.addWidget(QLabel("First Name:"))
        self.first_name_input = QLineEdit()
        self.first_name_input.setPlaceholderText("First Name")
        self.first_name_input.setMaxLength(30)
        self.first_name_input.setFixedWidth(265)
        self.first_name_input.setValidator(alpha_validator)
        self.first_name_input.textChanged.connect(self.on_search_input_changed)
        search_section_row_2.addWidget(self.first_name_input)

        search_section_row_2.addWidget(QLabel("Last Name:"))
        self.last_name_input = QLineEdit()
        self.last_name_input.setPlaceholderText("Last Name")
        self.last_name_input.setMaxLength(30)
        self.last_name_input.setFixedWidth(265)
        self.last_name_input.setValidator(alpha_validator)
        self.last_name_input.textChanged.connect(self.on_search_input_changed)
        search_section_row_2.addWidget(self.last_name_input)

        search_section_row_2.addStretch()

        search_section_row_2.addWidget(QLabel("Admin:"))
        self.admin_field = QComboBox()
        self.admin_field.addItems(["True", "False"])
        self.admin_field.setCurrentIndex(-1)
        self.admin_field.setPlaceholderText("admin")
        self.admin_field.currentIndexChanged.connect(self.on_search_input_changed)
        search_section_row_2.addWidget(self.admin_field)

        main_layout.addLayout(search_section_row_2)

        search_section_row_3 = QHBoxLayout()
        self.clear_btn = QPushButton("Clear")
        self.clear_btn.setFixedWidth(200)
        search_section_row_3.addWidget(self.clear_btn)

        search_section_row_3.addStretch()
        self.search_btn = QPushButton("Search")
        self.search_btn.setFixedWidth(200)
        search_section_row_3.addWidget(self.search_btn)
        main_layout.addLayout(search_section_row_3)

        hr2 = QFrame()
        hr2.setFrameShape(QFrame.Shape.HLine)
        hr2.setFrameShadow(QFrame.Shadow.Sunken)
        hr2.setObjectName("hr")
        main_layout.addWidget(hr2)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)

        self.users_layout = QVBoxLayout()  # Users container
        scroll_layout.addLayout(self.users_layout)
        scroll_layout.addStretch()

        scroll.setWidget(scroll_content)
        main_layout.addWidget(scroll)
        background.addWidget(main_layout_widget)
        self.setup_button_connections()

    def clear(self):
        """
        :purpose: clears all input fields and fetched items
        :author(s): Joe Lee, Colin Henderson
        """
        self.search_timer.stop()
        self.remove_user_section()
        fields = [
            self.user_id_input,
            self.username_input,
            self.first_name_input,
            self.last_name_input,
        ]
        for field in fields:
            field.blockSignals(True)
            field.clear()
            field.setReadOnly(False)
            field.setObjectName("DEFAULT")
            field.blockSignals(False)
            field.style().unpolish(field)
            field.style().polish(field)

        self.admin_field.blockSignals(True)
        self.admin_field.setCurrentIndex(-1)
        self.admin_field.blockSignals(False)
        self.admin_field.style().unpolish(self.admin_field)
        self.admin_field.style().polish(self.admin_field)

        status_bar_instance.send_message("Query and Results cleared")

    def on_search_input_changed(self):
        """
        :Purpose: forces a wait
        :Author(s): Joe Lee
        """
        self.search_timer.start(300)

    def build_and_search(self):
        """
        :Purpose: Gathers properties to build a query then calls query_db
        :Author(s): Joe Lee
        """
        self.remove_user_section()

        conditions = ["c.type = 'user'"]
        properties = []

        def add_property(props, value, operator="="):
            """
            :Purpose: appends query conditions
            :Author(s): Joe Lee
            """
            if value is not None:
                prop_name = props
                if operator == "CONTAINS":
                    conditions.append(f"CONTAINS(LOWER(c.{props}), LOWER(@{prop_name}))")
                else:
                    conditions.append(f"c.{props} {operator} @{prop_name}")
                properties.append({"name": f"@{prop_name}", "value": value})

        user_id = self.user_id_input.text().strip()
        if user_id:
            try:
                user_id_int = int(user_id)
                add_property("user_id", user_id_int, "=")
            except ValueError:
                pass

        username = self.username_input.text().strip()
        if username:
            add_property("username", username, "CONTAINS")

        last_consignment = self.last_consignment_input.text().strip()
        if last_consignment:
            try:
                consignment_container = self.db_connection.connect("Consignments")
                consignment_query = f"""
                    SELECT DISTINCT c.user_id
                    FROM c
                    WHERE c.type = 'consignment'
                    AND CONTAINS(c.datetime, '{last_consignment}')
                """
                results = list(consignment_container.query_items(
                    query=consignment_query,
                    enable_cross_partition_query=True
                ))
                matching_user_ids = [r['user_id'] for r in results if r.get('user_id')]

                if not matching_user_ids:
                    self.remove_user_section()
                    status_bar_instance.send_message("No users found")
                    return

                id_list = ", ".join(str(uid) for uid in matching_user_ids)
                conditions.append(f"c.user_id IN ({id_list})")
            except Exception as e:
                log.error(f"Error querying consignments: {e}")
                return

        first_name = self.first_name_input.text().strip()
        if first_name:
            add_property("first_name", first_name, "CONTAINS")

        last_name = self.last_name_input.text().strip()
        if last_name:
            add_property("last_name", last_name, "CONTAINS")

        admin_status = self.admin_field.currentText().strip().lower()
        if admin_status in ("true", "false"):
            add_property("admin", admin_status == "true", "=")

        if len(conditions) == 1:
            self.fetch()
            return

        where_clause = " AND ".join(conditions)
        search_query = f"SELECT * FROM c WHERE {where_clause}"
        self.query_db(search_query, properties)

    def query_db(self, query: str, properties: list = None):
        """
        :Purpose: Queries against the database
        :Author(s): Joe Lee
        """
        self.remove_user_section()
        try:
            container = self.db_connection.connect("Entities")
            results = list(container.query_items(
                query=query,
                parameters=properties if properties else [],
                enable_cross_partition_query=True
            ))

            users = []
            for item in results:
                users.append({
                    'user_id': item.get('user_id'),
                    'username': item.get('username', ''),
                    'last_consignment': item.get('last_consignment', ''),
                    'first_name': item.get('first_name', ''),
                    'last_name': item.get('last_name', ''),
                    'admin': item.get('admin', ''),
                })

            users.sort(key=lambda user: int(user['user_id']))

            last_consignments = {}
            try:
                user_ids = [user['user_id'] for user in users]
                user_id_list = ", ".join(str(user_id) for user_id in user_ids)
                consignment_container = self.db_connection.connect("Consignments")
                batch_query = f"""
                    SELECT c.user_id, c.datetime
                    FROM c
                    WHERE c.type = 'consignment'
                    AND c.user_id IN ({user_id_list})
                """
                last_cons = list(consignment_container.query_items(
                    query=batch_query,
                    enable_cross_partition_query=True
                ))

                last_consignments = {}
                for consignment in last_cons:
                    user_id = consignment['user_id']
                    datetime_string = consignment.get('datetime', '')
                    if not datetime_string:
                        continue
                    try:
                        parsed_datetime = datetime.strptime(datetime_string, "%m/%d/%y -- %H:%M")
                        if user_id not in last_consignments or parsed_datetime > last_consignments[user_id]['parsed']:
                            last_consignments[user_id] = {
                                'parsed': parsed_datetime,
                                'raw': datetime_string
                            }
                    except ValueError:
                        continue

                last_consignments = {user_id: value['raw'] for user_id, value in last_consignments.items()}

            except Exception as e:
                log.error(f"Error fetching last consignments: {e}")

            for user in users:
                user['last_consignment'] = last_consignments.get(user['user_id']) or ''
                self.add_user_section(user)

            if not users:
                status_bar_instance.send_message("No users found")
            else:
                status_bar_instance.send_message(f"Found {len(users)} user(s)")

        except Exception as e:
            log.error(f"Error executing query: {e}")
            status_bar_instance.send_message("Query failed")

    def fetch(self):
        """
        :purpose: fetches all users from Entities container
        :return: list of users
        :author(s): Joe Lee
        """
        get_all_query = "SELECT * FROM c WHERE c.type = 'user'"
        self.query_db(get_all_query)

    def add_user_section(self, user_data):
        """
        :purpose: adds user items
        :return: None
        :author(s): Joe Lee
        """
        # Users section container
        section_widget = QWidget()
        section_layout = QVBoxLayout(section_widget)
        section_layout.setContentsMargins(0, 0, 0, 0)

        line1_layout = QHBoxLayout()
        line1_layout.addWidget(QLabel("UserID:"))
        user_id = QLineEdit()
        user_id.setText(str(user_data['user_id']))
        user_id.setObjectName("READ_ONLY")
        user_id.setReadOnly(True)
        user_id.setMaxLength(10)
        user_id.setFixedWidth(55)
        user_id_validator = QRegularExpressionValidator(QRegularExpression("[0-9]{0,10}"))
        user_id.setValidator(user_id_validator)
        line1_layout.addWidget(user_id)

        line1_layout.addWidget(QLabel("Username:"))
        username = QLineEdit()
        username.setText(str(user_data['username']))
        username.setObjectName("READ_ONLY")
        username.setReadOnly(True)
        username.setMaxLength(30)
        username.setFixedWidth(265)
        alpha_validator = QRegularExpressionValidator(QRegularExpression("[A-Za-z ]+"))
        username.setValidator(alpha_validator)
        line1_layout.addWidget(username)

        line1_layout.addStretch()

        line1_layout.addWidget(QLabel("Last Consignment:"))
        last_consignment_input = QLineEdit()
        last_consignment_input.setText(user_data.get('last_consignment') or '')
        last_consignment_input.setObjectName("READ_ONLY")
        last_consignment_input.setReadOnly(True)
        last_consignment_input.setMaxLength(30)
        last_consignment_input.setFixedWidth(265)
        line1_layout.addWidget(last_consignment_input)

        section_layout.addLayout(line1_layout)

        line2_layout = QHBoxLayout()
        line2_layout.addWidget(QLabel("First Name:"))
        first_name = QLineEdit()
        first_name.setText(str(user_data['first_name']))
        first_name.setObjectName("READ_ONLY")
        first_name.setReadOnly(True)
        first_name.setMaxLength(30)
        first_name.setFixedWidth(265)
        first_name.setValidator(alpha_validator)
        line2_layout.addWidget(first_name)

        # last name
        line2_layout.addWidget(QLabel("Last Name:"))
        last_name = QLineEdit()
        last_name.setText(str(user_data['last_name']))
        last_name.setObjectName("READ_ONLY")
        last_name.setReadOnly(True)
        last_name.setMaxLength(30)
        last_name.setFixedWidth(265)
        last_name.setValidator(alpha_validator)
        line2_layout.addWidget(last_name)

        line2_layout.addStretch()

        line2_layout.addWidget(QLabel("Admin:"))
        admin_field = QComboBox()
        admin_field.addItems(["True", "False"])
        admin_field.setObjectName("READ_ONLY")
        admin_field.setEnabled(False)
        current_index = 0 if user_data['admin'] == True else 1      # Set "Admin" value as True or False in GUI
        admin_field.setCurrentIndex(current_index)
        line2_layout.addWidget(admin_field)

        section_layout.addLayout(line2_layout)

        line3_layout = QHBoxLayout()

        view_btn = QPushButton("View")
        line3_layout.addWidget(view_btn)

        edit_btn = QPushButton("Edit")
        edit_btn.setObjectName("red_btn")
        line3_layout.addWidget(edit_btn)

        section_layout.addLayout(line3_layout)

        hr = QFrame()
        hr.setFrameShape(QFrame.Shape.HLine)
        hr.setFrameShadow(QFrame.Shadow.Sunken)
        hr.setObjectName("hr")
        section_layout.addWidget(hr)

        # Add to container
        self.users_layout.addWidget(section_widget)

    def remove_user_section(self):
        """
        :purpose: clears subtab widget that holds vendor items
        :author(s): Joe Lee
        """
        # Remove all widgets from the layout
        for i in reversed(range(self.users_layout.count())):
            widget = self.users_layout.itemAt(i).widget()
            if widget:
                self.users_layout.removeWidget(widget)
                widget.deleteLater()

        self.users_section.clear()

        # Update status
        status_bar_instance.send_message("All users cleared")

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
                self.add_user_section(user)

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
        alpha_validator = QRegularExpressionValidator(QRegularExpression("[A-Za-z ]+"))
        username_input.setValidator(alpha_validator)
        layout.addWidget(username_input)

        layout.addWidget(QLabel("First Name:"))
        first_name_input = QLineEdit()
        first_name_input.setObjectName("first_name_input")
        first_name_input.setValidator(alpha_validator)
        layout.addWidget(first_name_input)

        layout.addWidget(QLabel("Last Name:"))
        last_name_input = QLineEdit()
        last_name_input.setObjectName("last_name_input")
        last_name_input.setValidator(alpha_validator)
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

        hr2 = QFrame()
        hr2.setFrameShape(QFrame.Shape.HLine)
        hr2.setFrameShadow(QFrame.Shadow.Sunken)
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

        # Admin
        admin_q_label = QLabel("Admin")
        admin_q_label.setObjectName("label")
        layout.addWidget(admin_q_label)
        admin_question = QComboBox()
        admin_question.addItems(["True", "False"])
        admin_question.setObjectName("admin_question")
        admin_question.setCurrentIndex(-1)
        layout.addWidget(admin_question)


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
        self.clear_btn.clicked.connect(self.clear)
        self.search_btn.clicked.connect(self.build_and_search)
        self.create_btn.clicked.connect(self.create_new_user_prompt)

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
            "username": dialog.findChild(QLineEdit, "username_input").text().strip(),
            "first_name": dialog.findChild(QLineEdit, "first_name_input").text().strip(),
            "last_name": dialog.findChild(QLineEdit, "last_name_input").text().strip(),
            "password": hash_password(dialog.findChild(QLineEdit, "password_input").text().strip()),
            "q1_q": dialog.findChild(QComboBox, "question1").currentText().strip(),
            "q1_a": dialog.findChild(QLineEdit, "response1").text().strip(),
            "q2_q": dialog.findChild(QComboBox, "question2").currentText().strip(),
            "q2_a": dialog.findChild(QLineEdit, "response2").text().strip(),
            "admin": True if dialog.findChild(QComboBox, "admin_question").currentText().strip() == "True" else False,
            "type": "user"
        }
        return raw_user_data

    def generate_new_user_id(self):
        """
        :Purpose: generates new user_id incrementing max value of database property by 1
        :Author(s): Joe Lee
        """
        new_id = int(get_max_value("Entities", "user_id")) + 1
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
