from PyQt6.QtWidgets import QDialog
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtWidgets import QHBoxLayout
from PyQt6.QtWidgets import QLabel
from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtWidgets import QComboBox
from PyQt6.QtCore import Qt

from src import SPOT
from src.core.hash_qa import hash_security_question_answer
import utils.logger.logger as log

class SecurityQuestionsDialog(QDialog):
    """
    purpose: Dialog for changing security questions and answers
    author(s): Alexander Bubienko
    """
    def __init__(self, theme_manager, parent=None):
        super().__init__(parent)
        self.theme_manager = theme_manager
        self.setWindowTitle("Change Security Questions")
        self.setFixedWidth(400)
        self.setModal(True)
        
        self.question_list = SPOT.QUESTIONS_LIST
        
        self.hashed_questions_answers = None
        self.setup_ui()
        
        if self.theme_manager:
            self.theme_manager.apply_default_theme(self)
    
    def setup_ui(self):
        """
        purpose: Initialize the security questions UI
        author(s): Alexander Bubienko
        """
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("Set New Security Questions and Answers")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setObjectName("dialog_title")
        layout.addWidget(title)
        
        layout.addStretch()
        
        # Question 1
        layout.addWidget(QLabel("Security Question 1:"))
        self.question1_combo = QComboBox()
        self.question1_combo.addItems(self.question_list)
        self.question1_combo.setCurrentIndex(-1)
        layout.addWidget(self.question1_combo)
        
        layout.addWidget(QLabel("Answer 1:"))
        self.answer1_input = QLineEdit()
        self.answer1_input.setPlaceholderText("Enter answer for question 1")
        self.answer1_input.setMaxLength(255)
        layout.addWidget(self.answer1_input)
        
        # Separator
        hr1 = QLabel()
        hr1.setObjectName("hr")
        layout.addWidget(hr1)
        
        # Question 2
        layout.addWidget(QLabel("Security Question 2:"))
        self.question2_combo = QComboBox()
        self.question2_combo.addItems(self.question_list)
        self.question2_combo.setCurrentIndex(-1)
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
        purpose: Validate and hash the security questions and answers
        author(s): Alexander Bubienko, Joe Lee
        """
        q1 = self.question1_combo.currentText()
        a1 = self.answer1_input.text().strip()
        q2 = self.question2_combo.currentText()
        a2 = self.answer2_input.text().strip()
        
        # Validation
        if self.question1_combo.currentIndex() == -1:
            QMessageBox.warning(self, "Invalid Input", "Please select Question 1")
            return
            
        if not a1:
            QMessageBox.warning(self, "Invalid Input", "Answer 1 cannot be empty")
            return
            
        if self.question2_combo.currentIndex() == -1:
            QMessageBox.warning(self, "Invalid Input", "Please select Question 2")
            return
            
        if not a2:
            QMessageBox.warning(self, "Invalid Input", "Answer 2 cannot be empty")
            return
        
        # Create dictionary of questions and answers
        qa_dict = {
            q1: a1,
            q2: a2
        }
        
        # Hash the questions and answers using the existing function
        try:
            hashed_qa = hash_security_question_answer(qa_dict)
            
            if self.hashed_questions_answers == -1:
                QMessageBox.critical(self, "Error", "Failed to hash security questions")
                return

            items = list(hashed_qa.items())
            hashed_q1, hashed_a1 = items[0]
            hashed_q2, hashed_a2 = items[1]

            self.hashed_questions_answers = {
                'q1_q': hashed_q1,
                'q1_a': hashed_a1,
                'q2_q': hashed_q2,
                'q2_a': hashed_a2
            }
            self.accept()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")
            log.error(f"Security questions hashing error: {e}")