import pytest
from unittest.mock import patch
from ui.prompts.security_dialog import SecurityQuestionsDialog

"""
Author: Kyle Valdez
Purpose: Test Security feature exist for user interaction
"""

@pytest.fixture
def fake_deps():
    with patch("src.SPOT") as fake_spot:
        fake_spot.QUESTIONS_LIST = ["fake question 1", "fake question 2", "fake question 3"]
        yield

# should pass
def test_dialog_opens(app, fake_deps):
    dialog = SecurityQuestionsDialog(theme_manager=None)
    assert dialog is not None, "Expected dialog to be opened"

# should pass
def test_dialog_title(app, fake_deps):
    dialog = SecurityQuestionsDialog(theme_manager=None)
    assert dialog.windowTitle() == "Change Security Questions", "Expected window title to be 'Change Security Questions'"

# should pass
def test_dialog_has_two_questions(app, fake_deps):
    dialog = SecurityQuestionsDialog(theme_manager=None)
    assert dialog.question1_combo is not None, "Expected there to be a question1 for qcombobox"
    assert dialog.question2_combo is not None, "Expected there to be a question2 for qcombobox"