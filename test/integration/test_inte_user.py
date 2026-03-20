from unittest.mock import MagicMock

from src.user import current_user
from ui.prompts.login import LoginScreen

"""
Author: Kyle Valdez
Purpose: Testing if username is set on successful login, not set if fail
"""

def test_current_user_set_after_login(app):
    fake_theme = MagicMock()
    dialog = LoginScreen(theme_manager=fake_theme)
    dialog.username_input.setText("user")
    dialog.password_input.setText("asdf")
    dialog.attempt_login()
    assert current_user.get_username() == "user", "Expected username to be set to user"