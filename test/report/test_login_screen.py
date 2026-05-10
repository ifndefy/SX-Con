import pytest
from unittest.mock import patch, MagicMock

from PyQt6.QtCore import Qt
from PyQt6.QtTest import QTest
from PyQt6.QtWidgets import QDialog
from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QApplication
from PyQt6.QtWidgets import QLabel
from unittest.mock import patch

from src import SPOT
from src.user import current_user
from ui.core.theme_manager import ThemeManager
from ui.prompts.login import LoginScreen
from ui.prompts.forgot_pw import ForgotPasswordScreen


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
    :Purpose: verifies blank username and password are rejected and showing a warning
    :Author(s): Kyle Valdez
    """
    screen = login_screen

    with patch.object(screen, "authenticate", return_value=False) as mock_auth, \
         patch("ui.prompts.login.QMessageBox.warning") as mock_warning:
        screen.login_btn.click()

        mock_auth.assert_called_once_with("", ""), "Expected authenticate to be called with empty strings"
        assert mock_warning.called, "Expected no warning for blank credentials (authenticate handles it)"


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

@pytest.fixture
def prompt_login(app):
    theme_manager = ThemeManager()
    yield LoginScreen(theme_manager)

def test_window_instantiates(prompt_login):
    """
    :Purpose: verifies the login prompt/dialog screen instantiates
    :Author(s): Kyle Valdez
    """
    window = prompt_login
    assert window is not None, "Expected LoginScreen to instantiate"

def test_title(prompt_login):
    """
    :Purpose: verifies the title of the login screen window is valid
    :Author(s): Kyle Valdez
    """
    window = prompt_login
    assert window.windowTitle() == "SX-Con - Login", "Expected window title to be 'SX-Con - Login'"

def test_theme(prompt_login):
    """
    :Purpose: verifies the login screen has the default theme applied
    :Author(s): Kyle Valdez
    """
    window = prompt_login
    assert window.theme_manager.get_current_theme() == "Super"

def test_logo_exists(prompt_login):
    """
    :Purpose: verifies the logo exists on the login screen
    :Author(s): Kyle Valdez
    """
    window = prompt_login
    assert window.logo is not None, "Expected 'logo' to exist"

def test_revision_exists(prompt_login):
    """
    :Purpose: verifies the revision is on the login screen
    :Author(s): Kyle Valdez
    """
    window = prompt_login
    rev = window.findChild(QLabel, "rev_label")
    assert rev is not None
    assert rev.text() == SPOT.APP_VERSION

def test_username_field(prompt_login):
    """
    :Purpose: verifies the functionality of the username field
    :Author(s): Kyle Valdez
    """
    window = prompt_login
    assert window.username_input is not None, "Expected 'username' input field to exist"

    QTest.keyClicks(window.username_input, "123./")
    assert window.username_input.text() == '', "Expected field validator to reject all entered characters"
    window.username_input.clear()
    QTest.keyClicks(window.username_input, "123./abc")
    assert window.username_input.text() == 'abc', "Expected only 'abc' to remain after validators restrict input characters"

def test_password_field(prompt_login):
    """
    :Purpose: verifies the functionality of the password field
    :Author(s): Kyle Valdez
    """
    window = prompt_login
    assert window.password_input is not None, "Expected 'password' input field to exist"
    QTest.keyClicks(window.password_input, "123./")
    assert window.password_input.text() == '123./', "Expected no character limitations for password input"
    window.password_input.clear()
    QTest.keyClicks(window.password_input, "123./abc")
    assert window.password_input.text() == '123./abc', "Expected no character limitations for password input"

def test_login_button_works(prompt_login):
    """
    :Purpose: verifies the functionality of the login button
    :Author(s): Kyle Valdez
    """
    window = prompt_login
    assert window.login_btn is not None, "Expected 'Login' button to exist"
    QTest.keyClicks(window.username_input, "user")
    assert window.username_input.text() == 'user', "Expected 'user' to be entered as input text"
    QTest.keyClicks(window.password_input, "asdf")
    assert window.password_input.text() == 'asdf', "Expected 'asdf' to be entered as input text"
    QTest.mouseClick(window.login_btn, Qt.MouseButton.LeftButton)
    assert current_user.get_username() == "user", "Expected to be able to login with test user account"

def test_login_fails_gracefully(prompt_login):
    window = prompt_login
    with patch('ui.prompts.login.QMessageBox.warning') as mock_warn:
        QTest.keyClicks(window.username_input, "doesnt")
        assert window.username_input.text() == 'doesnt', "Expected 'doesnt' to be entered as input text"
        QTest.keyClicks(window.password_input, "work")
        assert window.password_input.text() == 'work', "Expected 'work' to be entered as input text"
        QTest.mouseClick(window.login_btn, Qt.MouseButton.LeftButton)
        mock_warn.assert_called_once_with(window, 'Login Failed', 'Invalid username or password!')

def test_forgot_password_button(prompt_login):
    """
    :Purpose: verifies the functionality of the forgot password button
    :Author(s): Kyle Valdez
    """
    window = prompt_login
    assert window.forgot_pw_btn is not None

    def check_pw_dialog():
        """
        :Purpose: helper method to verify that the forgot password dialog window opens
        :Author(s): Kyle Valdez
        """
        dialog = QApplication.activeModalWidget()
        assert isinstance(dialog, ForgotPasswordScreen)
        dialog.close()

    QTimer.singleShot(0, check_pw_dialog)
    QTest.mouseClick(window.forgot_pw_btn, Qt.MouseButton.LeftButton)
