import pytest
from unittest.mock import MagicMock
from unittest.mock import patch
from ui.prompts.login import LoginScreen

# define fake dependencies
@pytest.fixture
def fake_deps():
    with patch("ui.prompts.login.img_helpers.get_login_logo_path", return_value=""), \
    patch("ui.prompts.login.db_connection", MagicMock()):
        yield

# should pass
def test_dialog_opens(app):
    fake_theme = MagicMock()
    dialog = LoginScreen(theme_manager=fake_theme)
    assert dialog is not None

# should pass, window title is correct
def test_dialog_title(app):
    fake_theme = MagicMock()
    dialog = LoginScreen(theme_manager=fake_theme)
    assert dialog.windowTitle() == "SX-Con - Login"

# should pass, there are inputs
def test_dialog_input_fields_exist(app):
    fake_theme = MagicMock()
    dialog = LoginScreen(theme_manager=fake_theme)
    assert dialog.username_input is not None
    assert dialog.password_input is not None

# should pass, tries to login with username
def test_login_flow_on_success(app, fake_deps):
    with patch.object(LoginScreen, "authenticate", return_value=True):
        fake_theme = MagicMock()
        dialog = LoginScreen(theme_manager=fake_theme)
        dialog.username_input.setText("username")
        dialog.attempt_login()
        assert dialog.username == "username"

# should pass, fails to login due to wrong pw
def test_authenticate_fails_to_login(app, fake_deps):
    fake_theme = MagicMock()
    dialog = LoginScreen(theme_manager=fake_theme)
    with patch("ui.prompts.login.db_connection") as fake_db:
        fake_db.connect.return_value.query_items.return_value = []
        result = dialog.authenticate("username", "wrongpw")
        assert result == False

# should pass, successfully logs in
def test_authenticate_successful_login(app, fake_deps):
    fake_theme = MagicMock()
    dialog = LoginScreen(theme_manager=fake_theme)
    with patch("ui.prompts.login.db_connection") as fake_db, \
         patch("ui.prompts.login.authenticate_password", return_value="1"):
        fake_db.connect.return_value.query_items.return_value = [
            {"username": "testuser", "password": "hashed_password"}
        ]
        result = dialog.authenticate("testuser", "correctpassword")
        assert result == True
