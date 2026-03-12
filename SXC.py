import sys

from PyQt6.QtWidgets import QApplication
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtWidgets import QDialog

from ui.main_window import MainWindow
from ui.prompts.login import LoginScreen
from ui.core.theme_manager import ThemeManager

from services.connect_database import db_connection
from src.user import current_user

def main():
    app = QApplication(sys.argv)
    theme_manager = ThemeManager()

    while True:
        db_connection.__init__()
        if db_connection.connect("Consignments"):
            login_screen = LoginScreen(theme_manager)
            if login_screen.exec() != QDialog.DialogCode.Accepted:
                break
            window = MainWindow()
        else:
            QMessageBox.information(None, "Error", "Failed to connect to database\n"
                                                   "Initializing in OFFLINE Mode")
            current_user.set_user("offline", False)
            window = MainWindow(offline_mode=True)

        window.show()
        app.exec()
        if hasattr(window, 'logout_requested') and window.logout_requested:
            continue
        else:
            break

    sys.exit(0)


if __name__ == '__main__':
    main()