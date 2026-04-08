import pytest
from unittest.mock import MagicMock
from unittest.mock import patch
from ui.prompts.forgot_pw import ForgotPasswordScreen

# define fake dependencies
@pytest.fixture
def fake_deps():
    with patch("src.SPOT") as fake_spot:
        fake_spot.QUESTIONS_LIST = ['q1', 'q2', 'q3']
        yield

# should pass, username not in db should not be able to find user_id
def test_fail_username_not_in_db(app, fake_deps):
    with patch("ui.prompts.forgot_pw.get_item_by_property", return_value=None), \
         patch("ui.prompts.forgot_pw.QMessageBox.critical"):
        fake_theme = MagicMock()
        dialog = ForgotPasswordScreen(theme_manager=fake_theme)
        dialog.username_input.setText("fake_user")
        dialog.req_btn.click()
        assert not hasattr(dialog, "user_id"), "Expected to not be able to find fake username"

# integration: "user" is found
def test_integration_user_found(app):
    with patch("ui.prompts.forgot_pw.AnsSecQDialog") as fake_qa:
        fake_qa.return_value.exec.return_value = 0
        fake_theme = MagicMock()
        dialog = ForgotPasswordScreen(theme_manager=fake_theme)
        dialog.username_input.setText("user")
        dialog.req_btn.click()
        assert hasattr(dialog, "user_id"), "Expected to be able to find real username"