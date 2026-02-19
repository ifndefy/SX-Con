from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QComboBox
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtWidgets import QHBoxLayout
from PyQt6.QtWidgets import QLabel
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtWidgets import QScrollArea
from PyQt6.QtWidgets import QWidget

from ui.core.theme_manager import ThemeManager
from ui.tabs.base import BaseTab
import utils.logger.logger as log

class SettingsTab(BaseTab):
    def __init__(self, api_handler):
        self.save_btn = None
        self.load_btn = None
        self.theme_dropdown_menu = None
        self.ticket_counter = None
        self.tickets_layout = None

        self.theme_manager = ThemeManager()

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

        current_username_input = QLineEdit("test")
        current_username_input.setReadOnly(True)
        user_layout_line_0.addWidget(current_username_input)

        change_username_btn = QPushButton("Change Username")
        user_layout_line_0.addWidget(change_username_btn)

        layout.addLayout(user_layout_line_0)

        # HR Line
        hr1 = QLabel()
        hr1.setObjectName("hr")
        layout.addWidget(hr1)

        pw_layout_line_0 = QHBoxLayout()
        pw_title = QLabel("Password:")
        pw_title.setObjectName("post_title")
        pw_layout_line_0.addWidget(pw_title)

        view_pw_btn = QPushButton("View Password")
        pw_layout_line_0.addWidget(view_pw_btn)
        change_pw_btn = QPushButton("Change Password")
        pw_layout_line_0.addWidget(change_pw_btn)

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
        view_qa_btn = QPushButton("View Questions")
        q_line_5.addWidget(view_qa_btn)
        change_qa_btn = QPushButton("Change Questions")
        q_line_5.addWidget(change_qa_btn)

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
        :author(s): Joe Lee
        """
        # self.update_btn.clicked.connect(self.fetch_on_clicked)
        # self.view_btn.clicked.connect()
        # self.excel_btn.clicked.connect()
        # self.pdf_btn.clicked.connect()
        # self.print_btn.clicked.connect()

    def click_on_change_pw(self):
        pass
        # todo: add new pw line
        # todo: change current pw field to READONLY=FALSE
