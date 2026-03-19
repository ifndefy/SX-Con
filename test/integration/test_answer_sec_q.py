import pytest
from unittest.mock import MagicMock
from unittest.mock import patch
from ui.prompts.answer_sec_q import AnsSecQDialog


# define fake dependencies
@pytest.fixture
def fake_deps():
    with patch("ui.prompts.answer_sec_q.SPOT") as fake_spot:
        fake_spot.QUESTIONS_LIST = ['q1', 'q2', 'q3']
        yield

# should pass
def test_dialog_opens(app, fake_deps):
    fake_theme = MagicMock()
    dialog = AnsSecQDialog(theme_manager=fake_theme, user_id="fake_user", q_list=['q1', 'q2'])
    assert dialog is not None, "Expected dialog to open"

# should pass, window title is correct
def test_dialog_title(app, fake_deps):
    fake_theme = MagicMock()
    dialog = AnsSecQDialog(theme_manager=fake_theme, user_id="fake_user", q_list=['q1', 'q2'])
    assert dialog.windowTitle() == "Answer Security Questions", "Expected window title to be 'Answer Security Questions'"


# should pass, 4 text fields exist
def test_text_fields_exist(app, fake_deps):
    fake_theme = MagicMock()
    dialog = AnsSecQDialog(theme_manager=fake_theme, user_id="fake_user", q_list=['q1', 'q2'])
    assert dialog.question1_combo is not None, "Expected qcombobox to exist for question 1"
    assert dialog.question2_combo is not None, "Expected qcombobox to exist for question 2"
    assert dialog.answer1_input is not None, "Expected answer input to be None on startup"
    assert dialog.answer2_input is not None, "Expected answer input to be None on startup"

# question fields are preselected
def test_question_fields_preselected(app, fake_deps):
    fake_theme = MagicMock()
    dialog = AnsSecQDialog(theme_manager=fake_theme, user_id="fake_user", q_list=['q1', 'q2'])
    assert dialog.question1_combo.currentText() == 'q1', "Expected q1 to be preselected on startup"
    assert dialog.question2_combo.currentText() == 'q2', "Expected q2 to be preselected on startup"

# question fields are locked
def test_question_fields_locked(app, fake_deps):
    fake_theme = MagicMock()
    dialog = AnsSecQDialog(theme_manager=fake_theme, user_id="fake_user", q_list=['q1', 'q2'])
    assert dialog.question1_combo.isEnabled() is False, "Expected "
    assert dialog.question2_combo.isEnabled() is False

# answer fields are empty
def test_answer_fields_are_empty(app, fake_deps):
    fake_theme = MagicMock()
    dialog = AnsSecQDialog(theme_manager=fake_theme, user_id="fake_user", q_list=['q1', 'q2'])
    assert dialog.answer1_input.text() == "", "Expected answer input to be empty on startup"
    assert dialog.answer2_input.text() == "", "Expected answer input to be empty on startup"

# answer fields are enabled
def test_answer_fields_are_enabled(app, fake_deps):
    fake_theme = MagicMock()
    dialog = AnsSecQDialog(theme_manager=fake_theme, user_id="fake_user", q_list=['q1', 'q2'])
    assert dialog.answer1_input.isEnabled() is True, "Expected answer input to be enabled on startup"
    assert dialog.answer2_input.isEnabled() is True, "Expected answer input to be enabled on startup"