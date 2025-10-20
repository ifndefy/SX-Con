import os
from PyQt6.QtCore import QFile
from PyQt6.QtCore import QTextStream

class ThemeManager:
    def __init__(self):
        self.themes_dir = "ui/themes"
        self.current_theme = "super"

    def get_available_themes(self):
        """
        :author(s): Joe Lee
        :purpose: parses the themes file and returns the available themes
        :return: list of available themes
        """
        themes = []
        if os.path.exists(self.themes_dir):
            for file in os.listdir(self.themes_dir):
                if file.endswith('.qss'):
                    theme_name = file.replace('.qss', '')
                    themes.append(theme_name)

        if "super" in themes:
            themes.remove("super")
            themes.sort()
            themes.insert(0, "super")
        else:
            themes.sort()

        return themes

    def apply_theme(self, theme_name, widget=None):
        """
        :author(s): Joe Lee
        :purpose: applies the theme to the given theme name
        :return: boolean indicating if the theme was applied
        """
        if widget is None:
            return False

        theme_path = os.path.join(self.themes_dir, f"{theme_name}.qss")

        if not os.path.exists(theme_path):
            print(f"Theme not found: {theme_path}")
            return False

        style_file = QFile(theme_path)
        if style_file.open(QFile.OpenModeFlag.ReadOnly | QFile.OpenModeFlag.Text):
            stream = QTextStream(style_file)
            widget.setStyleSheet(stream.readAll())
            style_file.close()
            self.current_theme = theme_name
            print(f"Theme applied: {theme_name}")
            return True

        return False

    def apply_default_theme(self, widget):
        """
        :author(s): Joe Lee
        :purpose: applies "Super" theme by default
        :return: boolean indicating if the theme was applied
        """
        return self.apply_theme("Super", widget)

    def get_current_theme(self):
        """
        :author(s): Joe Lee
        :purpose: returns the current theme
        :return: current theme
        """
        return self.current_theme