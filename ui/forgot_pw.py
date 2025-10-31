from PyQt6.QtWidgets import QDialog, QComboBox
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtWidgets import QLabel
from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtCore import Qt


class ForgotPasswordScreen(QDialog):
    def __init__(self, theme_manager, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.theme_manager = theme_manager
        self.setWindowTitle("SX-Con - Password Reset")
        self.setFixedSize(500, 400)
        self.setModal(True)

        self.questionList = [
            "What is your mother's maiden name?",
            "What color was your first car?",
            "Who was your best friend in the third grade?"
            # todo: add 2 more questions
        ]

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

        hr1 = QLabel()
        hr1.setObjectName("hr")
        layout.addWidget(hr1)

        # Question 1
        prompt_label = QLabel("Security Question 1:")
        prompt_label.setObjectName("label")
        layout.addWidget(prompt_label)
        self.question1 = QComboBox()
        self.question1.addItems(self.questionList)
        self.question1.setObjectName("prompt_label")
        self.question1.setCurrentIndex(-1)
        layout.addWidget(self.question1)

        res1_label = QLabel("Response for Question 1:")
        res1_label.setObjectName("label")
        layout.addWidget(res1_label)
        self.question1_response = QLineEdit()
        self.question1_response.setPlaceholderText("test 1")
        self.question1_response.setObjectName("response_field")
        self.question1_response.setMaxLength(255)
        layout.addWidget(self.question1_response)

        hr2 = QLabel()
        hr2.setObjectName("hr")
        layout.addWidget(hr2)

        # Question 2
        prompt_label = QLabel("Security Question 2:")
        prompt_label.setObjectName("label")
        layout.addWidget(prompt_label)
        self.question2 = QComboBox()
        self.question2.addItems(self.questionList)
        self.question2.setObjectName("prompt_label")
        self.question2.setCurrentIndex(-1)
        layout.addWidget(self.question2)

        res2_label = QLabel("Response for Question 2:")
        res2_label.setObjectName("label")
        layout.addWidget(res2_label)
        self.question2_response = QLineEdit()
        self.question2_response.setPlaceholderText("test 2")
        self.question2_response.setObjectName("response_field")
        self.question2_response.setMaxLength(255)
        layout.addWidget(self.question2_response)

        layout.addStretch()

        # Forgot Password button
        forgot_pw_btn = QPushButton("Submit Responses")
        forgot_pw_btn.clicked.connect(self.forgot_pw_btn_action)
        layout.addWidget(forgot_pw_btn)

        self.setLayout(layout)

    def forgot_pw_btn_action(self):
        # Get all input values
        username = self.username_input.text().strip() # strip to remove white spaces at the beginning and end
        question1_index = self.question1.currentIndex() # currentIndex() method to get the selected question
        question1_response = self.question1_response.text().strip()
        question2_index = self.question2.currentIndex()
        question2_response = self.question2_response.text().strip()

        # todo: move validate to its own method
        # Validate that username has a value
        if not username:
            QMessageBox.warning(self, "Missing Information", "Please enter your username.")
            return

        # Validate that both security questoins are selected
        if question1_index == -1 or question2_index == -1:
            QMessageBox.warning(self, "Missing Information", "Please select both security questions.")
            return

        # Validate that security questions are different
        if question1_index == question2_index:
            QMessageBox.warning(self, "Invalid Selection", "Please select two different security questions.")
            return

        # Validate that response fields have input
        if not question1_response or not question2_response:
            QMessageBox.warning(self, "Missing Information", "Please provide responses for both security questions.")
            return

        # you can use the dictionary or the variables defined at the beginning of the method definition
        # the safer method is to use it from the dictionary sec_data because it is already validated
        sec_data = {
            'username': username,
            'question1': self.questionList[question1_index],
            'response1': question1_response,
            'question2': self.questionList[question2_index],
            'response2': question2_response
        }

        print("Data:", sec_data) # just for debugging purposes

        # todo: move pop up to its own method?
        QMessageBox.information(
            self,
            "Responses Submitted",
            "Your security responses have been submitted successfully.\n\n"
            "If successful,\nyou will be prompted to enter a new password"
        )
