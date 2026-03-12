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
    assert dialog is not None

# should pass
def test_dialog_title(app, fake_deps):
    dialog = SecurityQuestionsDialog(theme_manager=None)
    assert dialog.windowTitle() == "Change Security Questions"

# should fail, wrong title
def test_dialog_wrong_title(app, fake_deps):
    dialog = SecurityQuestionsDialog(theme_manager=None)
    assert dialog.windowTitle() != "Wrong Title"

# should pass
def test_dialog_has_two_questions(app, fake_deps):
    dialog = SecurityQuestionsDialog(theme_manager=None)
    assert dialog.question1_combo is not None
    assert dialog.question2_combo is not None

# should pass, theme_manager=None should not crash
def test_dialog_no_theme_manager(app, fake_deps):
    dialog = SecurityQuestionsDialog(theme_manager=None)
    assert dialog is not None