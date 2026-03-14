import pytest
from unittest.mock import MagicMock
from unittest.mock import patch

from src.user import current_user
from ui.prompts.login import LoginScreen

def test_attempt_login_valid(app):
    fake_theme = MagicMock()  # fake dependency
    login = LoginScreen(theme_manager=fake_theme)
    login.username_input.setText("user")  # integration test requires real data
    login.password_input.setText("asdf")  # integration test requires real data
    login.login_btn.click()  # trigger login button
    assert current_user.get_username() == "user", "Expected to be able to login with test user account"

def test_attempt_login_invalid(app):
    with patch('ui.prompts.login.QMessageBox.warning'):
        fake_theme = MagicMock()  # fake dependency
        login = LoginScreen(theme_manager=fake_theme)
        login.username_input.setText("blahblahasdf")  # integration test requires real data
        login.password_input.setText("asdf")  # integration test requires real data
        login.login_btn.click()  # trigger login button
        assert current_user.get_username() != "blahblahasdf", "Expected to be fail login with fake username"

