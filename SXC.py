import sys
import utils.logger as log

from PyQt6.QtWidgets import QApplication
from PyQt6.QtWidgets import QDialog
from ui.main_window import MainWindow
from ui.login import LoginScreen
from ui.core.theme_manager import ThemeManager

def main():
    app = QApplication(sys.argv)
    theme_manager = ThemeManager()

    while True:
        login_screen = LoginScreen(theme_manager)
        if login_screen.exec() != QDialog.DialogCode.Accepted:
            break

        window = MainWindow()
        window.show()
        app.exec()
        if hasattr(window, 'logout_requested') and window.logout_requested:
            continue
        else:
            break

    sys.exit(0)


if __name__ == '__main__':
    main()