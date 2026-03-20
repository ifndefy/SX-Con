import bcrypt

from PyQt6.QtWidgets import QDialog, QFrame
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtWidgets import QHBoxLayout
from PyQt6.QtWidgets import QLabel
from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtWidgets import QComboBox

from src import SPOT
from services.get_property import get_property
import utils.logger.logger as log


class AnsSecQDialog(QDialog):
    """
    purpose: Dialog for changing security questions and answers
    author(s): Alexander Bubienko, Joe Lee
    """

    def __init__(self, theme_manager, parent=None, user_id=None, q_list: list = None):
        super().__init__(parent)
        self.theme_manager = theme_manager
        self.setWindowTitle("Answer Security Questions")
        self.setFixedWidth(400)
        self.setModal(True)

        self.question_list = SPOT.QUESTIONS_LIST
        self.user_id = user_id
        self.user_q_1 = q_list[0]
        self.user_q_2 = q_list[1]

        self.uq1_idx, self.uq2_idx = self.get_user_qs_idxs()
        self.setup_ui()

        if self.theme_manager:
            self.theme_manager.apply_default_theme(self)

    def get_user_qs_idxs(self):
        indx1 = self.question_list.index(self.user_q_1)
        indx2 = self.question_list.index(self.user_q_2)
        return indx1, indx2

    def setup_ui(self):
        """
        purpose: Initialize the security questions UI
        author(s): Alexander Bubienko, Joe Lee
        """
        layout = QVBoxLayout()

        # Question 1
        layout.addWidget(QLabel("Security Question 1:"))
        self.question1_combo = QComboBox()
        self.question1_combo.addItems(self.question_list)
        self.question1_combo.setCurrentIndex(self.uq1_idx)
        self.question1_combo.setObjectName("READ_ONLY")
        self.question1_combo.setEnabled(False)
        layout.addWidget(self.question1_combo)

        layout.addWidget(QLabel("Answer 1:"))
        self.answer1_input = QLineEdit()
        self.answer1_input.setPlaceholderText("Enter answer for question 1")
        self.answer1_input.setMaxLength(255)
        layout.addWidget(self.answer1_input)

        # Separator
        hr1 = QFrame()
        hr1.setFrameShape(QFrame.Shape.HLine)
        hr1.setFrameShadow(QFrame.Shadow.Sunken)
        hr1.setObjectName("hr")
        layout.addWidget(hr1)

        # Question 2
        layout.addWidget(QLabel("Security Question 2:"))
        self.question2_combo = QComboBox()
        self.question2_combo.addItems(self.question_list)
        self.question2_combo.setCurrentIndex(self.uq2_idx)
        self.question2_combo.setObjectName("READ_ONLY")
        self.question2_combo.setEnabled(False)
        layout.addWidget(self.question2_combo)

        layout.addWidget(QLabel("Answer 2:"))
        self.answer2_input = QLineEdit()
        self.answer2_input.setPlaceholderText("Enter answer for question 2")
        self.answer2_input.setMaxLength(255)
        layout.addWidget(self.answer2_input)

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
        purpose: handles update clicked
        author(s): Joe Lee
        """
        if self.val_responses():
            self.accept()
        log.error("Invalid response")

    def val_responses(self):
        """
        purpose: verify responses are valid
        author(s): Joe Lee
        """
        if not bcrypt.checkpw(self.answer1_input.text().strip().encode('utf-8'),
                              get_property("Entities", "q1_a", "user", self.user_id).encode('utf-8')):
            QMessageBox.warning(self, "Question 1 Response", "Invalid Response")
            return False
        if not bcrypt.checkpw(self.answer2_input.text().strip().encode('utf-8'),
                              get_property("Entities", "q2_a", "user", self.user_id).encode('utf-8')):
            QMessageBox.warning(self, "Question 2 Response", "Invalid Response")
            return False
        return True
