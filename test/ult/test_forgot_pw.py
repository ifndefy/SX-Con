import pytest
from unittest.mock import MagicMock
from unittest.mock import patch
from ui.prompts.forgot_pw import ForgotPasswordScreen

"""
Author: Kyle Valdez
Purpose: Flow of forgetting password is proper
"""

# define fake dependencies
@pytest.fixture
def fake_deps():
    with patch("src.SPOT") as fake_spot:
        fake_spot.QUESTIONS_LIST = ['q1', 'q2', 'q3']
        yield

# should pass
def test_dialog_opens(app):
    fake_theme = MagicMock()
    dialog = ForgotPasswordScreen(theme_manager=fake_theme)
    assert dialog is not None

# should pass, window title is correct
def test_dialog_title(app):
    fake_theme = MagicMock()
    dialog = ForgotPasswordScreen(theme_manager=fake_theme)
    assert dialog.windowTitle() == "SX-Con - Password Reset"

# should pass, username input exists
def test_dialog_username_input_exist(app):
    fake_theme = MagicMock()
    dialog = ForgotPasswordScreen(theme_manager=fake_theme)
    assert dialog.username_input is not None
