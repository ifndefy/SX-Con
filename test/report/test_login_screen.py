import pytest
from unittest.mock import patch, MagicMock

from PyQt6.QtCore import Qt
from PyQt6.QtTest import QTest
from PyQt6.QtWidgets import QDialog

from ui.prompts.login import LoginScreen
from ui.core.theme_manager import ThemeManager


@pytest.fixture
def login_screen(app):
    theme_manager = ThemeManager()
    yield LoginScreen(theme_manager)


def test_login_screen_loads(login_screen):
    """
    :Purpose: verifies login screen loads correctly
    :Author(s): Kyle Valdez
    """
    screen = login_screen
    assert screen is not None, "Expected LoginScreen to instantiate"
    assert screen.username_input is not None, "Expected username input to exist"
    assert screen.password_input is not None, "Expected password input to exist"
    assert screen.login_btn is not None, "Expected login button to exist"
    assert screen.forgot_pw_btn is not None, "Expected forgot password button to exist"
    assert screen.login_btn.text() == "Login", "Expected default login button text"
    assert screen.forgot_pw_btn.text() == "Forgot Password", "Expected default forgot password button text"


def test_blank_credentials_rejected(login_screen):
    """
    :Purpose: verifies blank username and password are rejected without showing a warning
    :Author(s): Kyle Valdez
    """
    screen = login_screen

    with patch.object(screen, "authenticate", return_value=False) as mock_auth, \
         patch("ui.prompts.login.QMessageBox.warning") as mock_warning:
        screen.login_btn.click()

        mock_auth.assert_called_once_with("", ""), "Expected authenticate to be called with empty strings"
        assert not mock_warning.called, "Expected no warning for blank credentials (authenticate handles it)"


def test_invalid_credentials_show_warning(login_screen):
    """
    :Purpose: verifies invalid credentials show a warning message
    :Author(s): Kyle Valdez
    """
    screen = login_screen
    QTest.keyClicks(screen.username_input, "baduser")
    QTest.keyClicks(screen.password_input, "badpass")

    with patch.object(screen, "authenticate", return_value=False), \
         patch("ui.prompts.login.QMessageBox.warning") as mock_warning:
        screen.login_btn.click()

        assert mock_warning.called, "Expected warning popup for invalid credentials"
        call_args = mock_warning.call_args[0]
        assert "Invalid username or password" in str(call_args), "Expected invalid credentials error message"


def test_invalid_credentials_clear_password(login_screen):
    """
    :Purpose: verifies password field is cleared after a failed login attempt
    :Author(s): Kyle Valdez
    """
    screen = login_screen
    QTest.keyClicks(screen.username_input, "baduser")
    QTest.keyClicks(screen.password_input, "badpass")

    with patch.object(screen, "authenticate", return_value=False), \
         patch("ui.prompts.login.QMessageBox.warning"):
        screen.login_btn.click()

    assert screen.password_input.text() == "", "Expected password field to be cleared after failed login"


def test_valid_credentials_accept_dialog(login_screen):
    """
    :Purpose: verifies valid credentials cause the dialog to accept and set the username
    :Author(s): Kyle Valdez
    """
    screen = login_screen
    QTest.keyClicks(screen.username_input, "validuser")
    QTest.keyClicks(screen.password_input, "validpass")

    mock_user = {"username": "validuser", "admin": False}
    mock_container = MagicMock()
    mock_container.query_items.return_value = iter([mock_user])

    with patch.object(screen, "authenticate", return_value=True), \
         patch("ui.prompts.login.db_connection.connect", return_value=mock_container), \
         patch("ui.prompts.login.current_user") as mock_current_user, \
         patch.object(screen, "accept") as mock_accept:
        screen.attempt_login()

        assert mock_accept.called, "Expected dialog to accept on valid login"
        assert screen.username == "validuser", "Expected username to be set after successful login"


def test_valid_credentials_set_admin_status(login_screen):
    """
    :Purpose: verifies admin status is set correctly from the database on successful login
    :Author(s): Kyle Valdez
    """
    screen = login_screen
    QTest.keyClicks(screen.username_input, "adminuser")
    QTest.keyClicks(screen.password_input, "adminpass")

    mock_user = {"username": "adminuser", "admin": True}
    mock_container = MagicMock()
    mock_container.query_items.return_value = iter([mock_user])

    with patch.object(screen, "authenticate", return_value=True), \
         patch("ui.prompts.login.db_connection.connect", return_value=mock_container), \
         patch("ui.prompts.login.current_user") as mock_current_user, \
         patch.object(screen, "accept"):
        screen.attempt_login()

        mock_current_user.set_user.assert_called_once_with("adminuser", True), \
            "Expected current_user.set_user called with admin=True"


def test_valid_credentials_db_error_falls_back(login_screen):
    """
    :Purpose: verifies login still succeeds with non-admin fallback if DB query fails after auth
    :Author(s): Kyle Valdez
    """
    screen = login_screen
    QTest.keyClicks(screen.username_input, "validuser")
    QTest.keyClicks(screen.password_input, "validpass")

    with patch.object(screen, "authenticate", return_value=True), \
         patch("ui.prompts.login.db_connection.connect", side_effect=Exception("DB error")), \
         patch("ui.prompts.login.current_user") as mock_current_user, \
         patch.object(screen, "accept") as mock_accept:
        screen.attempt_login()

        mock_current_user.set_user.assert_called_once_with("validuser", False), \
            "Expected fallback to non-admin when DB query fails"
        assert mock_accept.called, "Expected dialog to still accept despite DB error"


def test_forgot_password_button_opens_screen(login_screen):
    """
    :Purpose: verifies forgot password button opens the ForgotPasswordScreen dialog
    :Author(s): Kyle Valdez
    """
    screen = login_screen

    with patch("ui.prompts.login.ForgotPasswordScreen") as mock_forgot_screen_class:
        mock_instance = MagicMock()
        mock_forgot_screen_class.return_value = mock_instance

        screen.forgot_pw_btn.click()

        assert mock_forgot_screen_class.called, "Expected ForgotPasswordScreen to be instantiated"
        assert mock_instance.exec.called, "Expected ForgotPasswordScreen exec to be called"


def test_password_field_echo_mode(login_screen):
    """
    :Purpose: verifies password field uses password echo mode to hide input
    :Author(s): Kyle Valdez
    """
    screen = login_screen
    from PyQt6.QtWidgets import QLineEdit
    assert screen.password_input.echoMode() == QLineEdit.EchoMode.Password, \
        "Expected password field to use Password echo mode"


def test_username_field_max_length(login_screen):
    """
    :Purpose: verifies username field enforces a maximum length of 30
    :Author(s): Kyle Valdez
    """
    screen = login_screen
    assert screen.username_input.maxLength() == 30, "Expected username input max length to be 30"


def test_password_field_max_length(login_screen):
    """
    :Purpose: verifies password field enforces a maximum length of 255
    :Author(s): Kyle Valdez
    """
    screen = login_screen
    assert screen.password_input.maxLength() == 255, "Expected password input max length to be 255"


def test_authenticate_returns_false_for_blank_username(login_screen):
    """
    :Purpose: verifies authenticate returns False when username is blank
    :Author(s): Kyle Valdez
    """
    screen = login_screen
    with patch("ui.prompts.login.db_connection.connect") as mock_connect:
        result = screen.authenticate("", "somepassword")
        assert result is False, "Expected False for blank username"
        assert not mock_connect.called, "Expected no DB connection attempt for blank username"


def test_authenticate_returns_false_for_blank_password(login_screen):
    """
    :Purpose: verifies authenticate returns False when password is blank
    :Author(s): Kyle Valdez
    """
    screen = login_screen
    with patch("ui.prompts.login.db_connection.connect") as mock_connect:
        result = screen.authenticate("someuser", "")
        assert result is False, "Expected False for blank password"
        assert not mock_connect.called, "Expected no DB connection attempt for blank password"


def test_authenticate_returns_false_for_unknown_user(login_screen):
    """
    :Purpose: verifies authenticate returns False when user is not found in the database
    :Author(s): Kyle Valdez
    """
    screen = login_screen
    mock_container = MagicMock()
    mock_container.query_items.return_value = iter([])

    with patch("ui.prompts.login.db_connection.connect", return_value=mock_container):
        result = screen.authenticate("unknownuser", "somepassword")
        assert result is False, "Expected False when user is not found"


def test_authenticate_returns_false_on_wrong_password(login_screen):
    """
    :Purpose: verifies authenticate returns False when password hash does not match
    :Author(s): Kyle Valdez
    """
    screen = login_screen
    mock_user = {"username": "validuser", "password": "stored_hash"}
    mock_container = MagicMock()
    mock_container.query_items.return_value = iter([mock_user])

    with patch("ui.prompts.login.db_connection.connect", return_value=mock_container), \
         patch("ui.prompts.login.authenticate_password", return_value="0"):
        result = screen.authenticate("validuser", "wrongpassword")
        assert result is False, "Expected False when password hash does not match"


def test_authenticate_returns_true_on_correct_password(login_screen):
    """
    :Purpose: verifies authenticate returns True when credentials are valid
    :Author(s): Kyle Valdez
    """
    screen = login_screen
    mock_user = {"username": "validuser", "password": "stored_hash"}
    mock_container = MagicMock()
    mock_container.query_items.return_value = iter([mock_user])

    with patch("ui.prompts.login.db_connection.connect", return_value=mock_container), \
         patch("ui.prompts.login.authenticate_password", return_value="1"):
        result = screen.authenticate("validuser", "correctpassword")
        assert result is True, "Expected True when credentials are valid"


def test_authenticate_returns_false_on_exception(login_screen):
    """
    :Purpose: verifies authenticate returns False when a database exception occurs
    :Author(s): Kyle Valdez
    """
    screen = login_screen
    with patch("ui.prompts.login.db_connection.connect", side_effect=Exception("Connection failed")):
        result = screen.authenticate("validuser", "somepassword")
        assert result is False, "Expected False when a database exception occurs"