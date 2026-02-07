from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QVBoxLayout, QTabWidget
from PyQt6.QtWidgets import QHBoxLayout
from PyQt6.QtWidgets import QLabel
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtWidgets import QScrollArea
from PyQt6.QtWidgets import QWidget

from services.connect_database import db_connection
from ui.tabs.base import BaseTab

class UsersTab(BaseTab):
    def __init__(self, api_handler, db_connection):
        self.tickets_section = []
        self.db_connection = db_connection
        super().__init__(api_handler, "users")

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
        self.status_label.setText("All tickets cleared")

    def fetch_on_clicked(self):
        """
        :purpose: calls fetch method and adds ticket sections
        :return: None
        :author(s): Joe Lee
        """
        self.remove_ticket_section()
        users = self.fetch()
        if not users:
            self.status_label.setText("No users found")
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

    def setup_button_connections(self):
        """
        :purpose: links buttons with methods
        :return: None
        :author(s): Joe Lee
        """
        self.update_btn.clicked.connect(self.fetch_on_clicked)