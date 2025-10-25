import sys
from PyQt6.QtWidgets import QApplication, QDialog
from ui.main_window import MainWindow
from ui.login import LoginScreen
from ui.core.theme_manager import ThemeManager


def main():
    app = QApplication(sys.argv)
    theme_manager = ThemeManager()

    login_screen = LoginScreen(theme_manager)

    if login_screen.exec() == QDialog.DialogCode.Accepted:
        window = MainWindow()
        window.show()
        sys.exit(app.exec())

    else:
        sys.exit(0)


if __name__ == '__main__':
    main()