import pytest
from unittest.mock import MagicMock
from unittest.mock import patch
from ui.prompts.answer_sec_q import AnsSecQDialog


@pytest.fixture
def fake_deps():
    with patch("ui.prompts.answer_sec_q.SPOT") as fake_spot:
        fake_spot.QUESTIONS_LIST = [
            "What was your first pet's name?",
            "What was your mother's maiden name?"
        ]
        yield

# integration: "user" responses are accepted:
def test_integration_qa_succeeds(app, fake_deps):
    fake_theme = MagicMock()
    dialog = AnsSecQDialog(theme_manager=fake_theme, user_id="2",
                           q_list=[
                               "What was your first pet's name?",
                               "What was your mother's maiden name?"
                           ])
    dialog.answer1_input.setText("asdf")
    dialog.answer2_input.setText("asdf")
    dialog.update_btn.click()
    result = dialog.val_responses()
    assert result == True

def test_integration_qa_fails(app, fake_deps):
    with patch("ui.prompts.answer_sec_q.QMessageBox.warning"):
        fake_theme = MagicMock()
        dialog = AnsSecQDialog(theme_manager=fake_theme, user_id="2",
                               q_list=[
                                   "What was your first pet's name?",
                                   "What was your mother's maiden name?"
                               ])
        dialog.answer1_input.setText("la;lkdsjfsa")
        dialog.answer2_input.setText("fnwoiedskl")
        dialog.update_btn.click()
        result = dialog.val_responses()
        assert result != True
