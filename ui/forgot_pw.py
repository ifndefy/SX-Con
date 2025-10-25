from PyQt6.QtWidgets import QDialog, QComboBox
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtWidgets import QLabel
from PyQt6.QtWidgets import QLineEdit
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
        layout.addWidget(QLabel("Username"))
        self.question1 = QLineEdit()
        self.question1.setPlaceholderText("Enter username")
        self.question1.setMaxLength(30)
        layout.addWidget(self.question1)

        # Question 1
        layout.addWidget(QLabel("Security Question 1:"))
        self.question1 = QComboBox()
        self.question1.addItems(self.questionList)
        self.question1.setCurrentIndex(-1)
        layout.addWidget(self.question1)

        layout.addWidget(QLabel("Response for Question 1"))
        self.question1_response = QLineEdit()
        self.question1_response.setPlaceholderText("test 1")
        self.question1_response.setMaxLength(255)
        layout.addWidget(self.question1_response)

        # Question 2
        layout.addWidget(QLabel("Security Question 1:"))
        self.question2 = QComboBox()
        self.question2.addItems(self.questionList)
        self.question2.setCurrentIndex(-1)
        layout.addWidget(self.question2)

        layout.addWidget(QLabel("Response for Question 2"))
        self.question2_response = QLineEdit()
        self.question2_response.setPlaceholderText("test 2")
        self.question2_response.setMaxLength(255)
        layout.addWidget(self.question2_response)

        layout.addStretch()

        # Forgot Password button
        forgot_pw_btn = QPushButton("Submit Responses")
        # forgot_pw_btn.clicked.connect() # todo: verify that the responses are equal to the stored values
        layout.addWidget(forgot_pw_btn)

        self.setLayout(layout)

    # todo: validate responses