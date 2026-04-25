import pytest
from unittest.mock import patch, MagicMock

from PyQt6.QtCore import Qt
from PyQt6.QtTest import QTest
from PyQt6.QtWidgets import QDialog

from ui.prompts.forgot_pw import ForgotPasswordScreen
from ui.core.theme_manager import ThemeManager


@pytest.fixture
def forgot_pw_screen(app):
    theme_manager = ThemeManager()
    yield ForgotPasswordScreen(theme_manager)


def test_forgot_pw_screen_loads(forgot_pw_screen):
    """
    :Purpose: verifies forgot password screen loads correctly
    :Author(s): Colin Henderson
    """
    screen = forgot_pw_screen
    assert screen is not None, "Expected ForgotPasswordScreen to instantiate"
    assert screen.username_input is not None, "Expected username input to exist"
    assert screen.req_btn is not None, "Expected request button to exist"
    assert screen.req_btn.text() == "Request for Username", "Expected default request button text"


def test_blank_username_shows_error(forgot_pw_screen):
    """
    :Purpose: verifies blank username is rejected
    :Author(s): Colin Henderson
    """
    screen = forgot_pw_screen

    with patch("ui.prompts.forgot_pw.QMessageBox.critical") as mock_critical:
        screen.req_btn.click()

        assert mock_critical.called, "Expected error popup for blank username"
        call_args = mock_critical.call_args[0]
        assert "Please enter a username" in str(call_args), "Expected blank username error message"

    assert screen.req_btn.isEnabled(), "Expected request button to remain enabled"
    assert screen.req_btn.text() == "Request for Username", "Expected request button text to reset"


def test_invalid_username_shows_error(forgot_pw_screen):
    """
    :Purpose: verifies invalid username is rejected
    :Author(s): Colin Henderson
    """
    screen = forgot_pw_screen
    QTest.keyClicks(screen.username_input, "not_a_real_user")

    with patch("ui.prompts.forgot_pw.get_item_by_property", return_value=None), \
         patch("ui.prompts.forgot_pw.QMessageBox.critical") as mock_critical:
        screen.req_btn.click()

        assert mock_critical.called, "Expected error popup for invalid username"
        call_args = mock_critical.call_args[0]
        assert "Username not found" in str(call_args), "Expected invalid username error message"

    assert screen.req_btn.isEnabled(), "Expected request button to be re-enabled"
    assert screen.req_btn.text() == "Request for Username", "Expected button text to reset"


def test_valid_username_opens_security_questions(forgot_pw_screen):
    """
    :Purpose: verifies valid username opens security question dialog
    :Author(s): Colin Henderson
    """
    screen = forgot_pw_screen
    QTest.keyClicks(screen.username_input, "user")

    mock_user = {"user_id": 1, "username": "user"}

    with patch("ui.prompts.forgot_pw.get_item_by_property", return_value=mock_user), \
         patch.object(screen, "get_sec_questions", return_value=["Q1", "Q2"]), \
         patch("ui.prompts.forgot_pw.AnsSecQDialog") as mock_qa_dialog:

        mock_dialog_instance = MagicMock()
        mock_dialog_instance.exec.return_value = QDialog.DialogCode.Rejected
        mock_qa_dialog.return_value = mock_dialog_instance

        screen.req_btn.click()

        assert mock_qa_dialog.called, "Expected security question dialog to open"
        assert screen.user_id == 1, "Expected user_id to be set from found user"


def test_correct_security_answers_open_password_dialog(forgot_pw_screen):
    """
    :Purpose: verifies correct security answers lead to password change dialog
    :Author(s): Colin Henderson
    """
    screen = forgot_pw_screen
    QTest.keyClicks(screen.username_input, "user")

    mock_user = {"user_id": 1, "username": "user"}

    with patch("ui.prompts.forgot_pw.get_item_by_property", return_value=mock_user), \
         patch.object(screen, "get_sec_questions", return_value=["Q1", "Q2"]), \
         patch("ui.prompts.forgot_pw.AnsSecQDialog") as mock_qa_dialog, \
         patch.object(screen, "show_password_change_dialog") as mock_pw_dialog:

        mock_dialog_instance = MagicMock()
        mock_dialog_instance.exec.return_value = QDialog.DialogCode.Accepted
        mock_qa_dialog.return_value = mock_dialog_instance

        screen.req_btn.click()

        assert mock_qa_dialog.called, "Expected security question dialog to open"
        assert mock_pw_dialog.called, "Expected password change dialog to open after correct answers"


def test_incorrect_security_answers_do_not_open_password_dialog(forgot_pw_screen):
    """
    :Purpose: verifies incorrect security answers do not lead to password change dialog
    :Author(s): Colin Henderson
    """
    screen = forgot_pw_screen
    QTest.keyClicks(screen.username_input, "user")

    mock_user = {"user_id": 1, "username": "user"}

    with patch("ui.prompts.forgot_pw.get_item_by_property", return_value=mock_user), \
         patch.object(screen, "get_sec_questions", return_value=["Q1", "Q2"]), \
         patch("ui.prompts.forgot_pw.AnsSecQDialog") as mock_qa_dialog, \
         patch.object(screen, "show_password_change_dialog") as mock_pw_dialog:

        mock_dialog_instance = MagicMock()
        mock_dialog_instance.exec.return_value = QDialog.DialogCode.Rejected
        mock_qa_dialog.return_value = mock_dialog_instance

        screen.req_btn.click()

        assert mock_qa_dialog.called, "Expected security question dialog to open"
        assert not mock_pw_dialog.called, "Expected password change dialog to remain closed after incorrect answers"


def test_request_button_locks_and_resets_on_lookup(forgot_pw_screen):
    """
    :Purpose: verifies request button changes state during username lookup and resets after
    :Author(s): Colin Henderson
    """
    screen = forgot_pw_screen
    QTest.keyClicks(screen.username_input, "user")

    with patch("ui.prompts.forgot_pw.get_item_by_property", return_value=None), \
         patch("ui.prompts.forgot_pw.QMessageBox.critical"):
        screen.req_btn.click()

    assert screen.req_btn.isEnabled(), "Expected request button to be enabled after lookup"
    assert screen.req_btn.text() == "Request for Username", "Expected request button text to reset"


def test_perform_password_update_success(forgot_pw_screen):
    """
    :Purpose: verifies successful password update flow
    :Author(s): Colin Henderson
    """
    screen = forgot_pw_screen
    QTest.keyClicks(screen.username_input, "user")
    screen.user_id = 1

    with patch("ui.prompts.forgot_pw.hash_password", return_value="hashed_pw"), \
         patch("ui.prompts.forgot_pw.update_property", return_value=0), \
         patch("ui.prompts.forgot_pw.QMessageBox.information") as mock_info, \
         patch.object(screen, "close") as mock_close:

        screen.perform_password_update("qwer")

        assert mock_info.called, "Expected success message on password update"
        assert mock_close.called, "Expected dialog to close after successful password change"


def test_perform_password_update_no_username(forgot_pw_screen):
    """
    :Purpose: verifies password update fails if no username is present
    :Author(s): Colin Henderson
    """
    screen = forgot_pw_screen
    screen.user_id = 1

    with patch("ui.prompts.forgot_pw.QMessageBox.critical") as mock_critical:
        screen.perform_password_update("qwer")

        assert mock_critical.called, "Expected error popup when no username is present"
        call_args = mock_critical.call_args[0]
        assert "No user logged in" in str(call_args), "Expected no user logged in error message"


def test_perform_password_update_hash_failure(forgot_pw_screen):
    """
    :Purpose: verifies password update fails if hashing fails
    :Author(s): Colin Henderson
    """
    screen = forgot_pw_screen
    QTest.keyClicks(screen.username_input, "user")
    screen.user_id = 1

    with patch("ui.prompts.forgot_pw.hash_password", return_value="-1"), \
         patch("ui.prompts.forgot_pw.QMessageBox.critical") as mock_critical:

        screen.perform_password_update("qwer")

        assert mock_critical.called, "Expected error popup when hashing fails"
        call_args = mock_critical.call_args[0]
        assert "Failed to hash password" in str(call_args), "Expected hashing failure error message"


def test_perform_password_update_missing_user_id(forgot_pw_screen):
    """
    :Purpose: verifies password update fails if user_id is missing
    :Author(s): Colin Henderson
    """
    screen = forgot_pw_screen
    QTest.keyClicks(screen.username_input, "user")
    screen.user_id = None

    with patch("ui.prompts.forgot_pw.hash_password", return_value="hashed_pw"), \
         patch("ui.prompts.forgot_pw.QMessageBox.critical") as mock_critical:

        screen.perform_password_update("qwer")

        assert mock_critical.called, "Expected error popup when user_id is missing"
        call_args = mock_critical.call_args[0]
        assert "Could not determine user ID" in str(call_args), "Expected missing user_id error message"

def test_empty_security_answers_do_not_advance(forgot_pw_screen):
    """
    :Purpose: verifies empty security question answers do not allow password reset flow to continue
    :Author(s): Colin Henderson
    """
    screen = forgot_pw_screen
    QTest.keyClicks(screen.username_input, "user")

    mock_user = {"user_id": 1, "username": "user"}

    with patch("ui.prompts.forgot_pw.get_item_by_property", return_value=mock_user), \
         patch.object(screen, "get_sec_questions", return_value=["Q1", "Q2"]), \
         patch("ui.prompts.forgot_pw.AnsSecQDialog") as mock_qa_dialog, \
         patch.object(screen, "show_password_change_dialog") as mock_pw_dialog:

        mock_dialog_instance = MagicMock()

        # Simulate user leaving answers blank and dialog rejecting
        mock_dialog_instance.exec.return_value = QDialog.DialogCode.Rejected
        mock_qa_dialog.return_value = mock_dialog_instance

        screen.req_btn.click()

        assert mock_qa_dialog.called, "Expected security question dialog to open"
        assert not mock_pw_dialog.called, "Expected password change dialog to remain closed on blank answers"


def test_blank_new_password_does_not_update(forgot_pw_screen):
    """
    :Purpose: verifies blank new password does not proceed with update
    :Author(s): Colin Henderson
    """
    screen = forgot_pw_screen
    QTest.keyClicks(screen.username_input, "user")
    screen.user_id = 1

    with patch("ui.prompts.forgot_pw.PasswordChangeDialog") as mock_pw_dialog_class, \
         patch.object(screen, "perform_password_update") as mock_update:

        mock_dialog = MagicMock()
        mock_dialog.exec.return_value = QDialog.DialogCode.Accepted
        mock_dialog.new_password = ""
        mock_pw_dialog_class.return_value = mock_dialog

        screen.show_password_change_dialog()

        assert mock_pw_dialog_class.called, "Expected password dialog to open"
        assert not mock_update.called, "Expected blank password to block update"


def test_mismatched_new_password_does_not_update(forgot_pw_screen):
    """
    :Purpose: verifies mismatched password inputs do not proceed with update
    :Author(s): Colin Henderson
    """
    screen = forgot_pw_screen
    QTest.keyClicks(screen.username_input, "user")
    screen.user_id = 1

    with patch("ui.prompts.forgot_pw.PasswordChangeDialog") as mock_pw_dialog_class, \
         patch.object(screen, "perform_password_update") as mock_update:

        mock_dialog = MagicMock()

        # Simulate mismatch causing dialog rejection
        mock_dialog.exec.return_value = QDialog.DialogCode.Rejected
        mock_dialog.new_password = None
        mock_pw_dialog_class.return_value = mock_dialog

        screen.show_password_change_dialog()

        assert mock_pw_dialog_class.called, "Expected password dialog to open"
        assert not mock_update.called, "Expected mismatched passwords to block update"