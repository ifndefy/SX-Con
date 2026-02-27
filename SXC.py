import sys
import traceback
import builtins  # also hook original print if needed

original_write = sys.stdout.write

def trace_write(text):
    if '8' in text:
        # Write to stderr to avoid recursion
        sys.stderr.write("=== 8 printed from ===\n")
        traceback.print_stack(file=sys.stderr)
    return original_write(text)

sys.stdout.write = trace_write

# Also hook the built-in print (calls sys.stdout.write, but just in case)
original_print = builtins.print
def trace_print(*args, **kwargs):
    if any('8' in str(arg) for arg in args):
        sys.stderr.write("=== print(8) called from ===\n")
        traceback.print_stack(file=sys.stderr)
    return original_print(*args, **kwargs)

builtins.print = trace_print

# Rest of your imports and code below...

import sys
import utils.logger as log

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