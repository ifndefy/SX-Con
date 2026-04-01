from PyQt6.QtWidgets import QApplication

from ui.core.theme_manager import ThemeManager
from ui.prompts.login import LoginScreen
from ui.prompts.forgot_pw import ForgotPasswordScreen
from ui.prompts.answer_sec_q import AnsSecQDialog
from ui.prompts.password_dialog import PasswordChangeDialog

from unittest.mock import patch


"""
Sequence:
    1 - Open login screen
    2 - Click Forgot Password
    3 - Forgot Password screen appears
    4 - Enter a real existing username
    5 - Click Request for Username
    6 - Real security question dialog appears
    7 - Enter intentionally wrong answers
    8 - Click Update
    9 - Verify invalid-response warning shown
    10 - Verify security dialog remains open
    11 - Verify password change dialog does not appear
    12 - Cancel and verify forgot-password flow recovers
"""


def test_e2e_fail_forgot_password_wrong_security_answer(app):
    theme_manager = ThemeManager()

    with patch("ui.prompts.answer_sec_q.QMessageBox.warning") as mock_sq_warning, \
         patch("ui.prompts.forgot_pw.QMessageBox.information") as mock_success, \
         patch("ui.prompts.forgot_pw.QMessageBox.critical") as mock_critical:

        # 1 - Open login screen
        login_screen = LoginScreen(theme_manager)
        assert isinstance(login_screen, LoginScreen), "Expected login screen to open"

        # 2 - Click Forgot Password
        login_screen.forgot_pw_btn.click()
        QApplication.processEvents()

        # 3 - Forgot Password screen appears
        forgot_screen = None
        for w in QApplication.topLevelWidgets():
            if isinstance(w, ForgotPasswordScreen):
                forgot_screen = w
                break

        assert isinstance(forgot_screen, ForgotPasswordScreen), \
            "Expected Forgot Password screen to appear after clicking Forgot Password"

        # 4 - Enter a real existing username
        # Replace 'user' with a known username that already exists in your test/dev data
        forgot_screen.username_input.setText("user")

        # 5 - Click Request for Username
        forgot_screen.req_btn.click()
        QApplication.processEvents()

        # 6 - Real security question dialog appears
        security_dialog = None
        for w in QApplication.topLevelWidgets():
            if isinstance(w, AnsSecQDialog):
                security_dialog = w
                break

        assert isinstance(security_dialog, AnsSecQDialog), \
            "Expected security question dialog to appear for a valid username"

        # 7 - Enter intentionally wrong answers
        security_dialog.answer1_input.setText("wrong1")
        security_dialog.answer2_input.setText("wrong2")

        # 8 - Click Update
        security_dialog.update_btn.click()
        QApplication.processEvents()

        # 9 - Verify invalid-response warning shown
        assert mock_sq_warning.called, \
            "Expected invalid-response warning when security answers are wrong"

        # 10 - Verify security dialog remains open
        assert security_dialog.isVisible(), \
            "Expected security dialog to remain open after invalid answers"

        # 11 - Verify password change dialog does not appear
        password_dialog_found = any(
            isinstance(w, PasswordChangeDialog)
            for w in QApplication.topLevelWidgets()
        )
        assert not password_dialog_found, \
            "Password change dialog should not open when security answers are wrong"

        # Also verify no success/reset occurred
        assert not mock_success.called, \
            "Success message should not appear when security answers are wrong"

        # 12 - Cancel and verify forgot-password flow recovers
        security_dialog.cancel_btn.click()
        QApplication.processEvents()

        assert forgot_screen.isVisible(), \
            "Expected Forgot Password screen to still be visible after cancelling security dialog"

        assert forgot_screen.req_btn.isEnabled(), \
            "Expected Request for Username button to be re-enabled after failed security flow"

        assert forgot_screen.req_btn.text() == "Request for Username", \
            "Expected Request button text to reset after failed security flow"