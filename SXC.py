import sys
from PyQt6.QtWidgets import QApplication, QDialog
from ui.main_window import MainWindow
from ui.login import LoginScreen
from ui.core.theme_manager import ThemeManager


def main():
    app = QApplication(sys.argv)

    # Create theme manager
    theme_manager = ThemeManager()

    # Show login screen first
    login_screen = LoginScreen(theme_manager)

    # Check if login was successful
    if login_screen.exec() == QDialog.DialogCode.Accepted:
        # Only show main window if login succeeded
        window = MainWindow()
        window.show()
        sys.exit(app.exec())
    else:
        # Login failed or was cancelled - exit the application
        sys.exit(0)


if __name__ == '__main__':
    main()