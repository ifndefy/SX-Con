from PyQt6.QtWidgets import QApplication, QDialog

from ui.core.theme_manager import ThemeManager
from ui.prompts.forgot_pw import ForgotPasswordScreen

from unittest.mock import patch

"""
Sequence:
    ### 1 - Open Forgot Password screen
    ### 2 - Enter valid username
    ### 3 - Request username lookup
    ### 4 - Security questions dialog appears
    ### 5 - Simulate WRONG answers (dialog rejected)
    ### 6 - Verify password change does NOT occur
    ### 7 - Verify no success message shown
    ### 8 - Verify user can retry
"""

def test_e2e_fail_forgot_password_wrong_security_answer(app):
    theme_manager = ThemeManager()
    forgot_screen = ForgotPasswordScreen(theme_manager)

    with patch("ui.prompts.forgot_pw.get_item_by_property") as mock_get_user, \
         patch.object(ForgotPasswordScreen, "get_sec_questions", return_value=["Q1", "Q2"]), \
         patch("ui.prompts.forgot_pw.AnsSecQDialog") as mock_ans_dialog_cls, \
         patch("ui.prompts.forgot_pw.PasswordChangeDialog") as mock_pwd_dialog_cls, \
         patch("ui.prompts.forgot_pw.QMessageBox.information") as mock_success, \
         patch("ui.prompts.forgot_pw.QMessageBox.critical") as mock_critical:

        mock_get_user.return_value = {"user_id": "123"}

        mock_ans_dialog = mock_ans_dialog_cls.return_value
        mock_ans_dialog.exec.return_value = QDialog.DialogCode.Rejected

        forgot_screen.username_input.setText("user")
        forgot_screen.req_btn.click()
        QApplication.processEvents()

        assert mock_get_user.called, "Expected user lookup to be called"
        assert mock_ans_dialog_cls.called, "Expected security question dialog to be opened"

        assert not mock_pwd_dialog_cls.called, \
            "Password change dialog should not open when security answers fail"

        assert not mock_success.called, \
            "Success message should not appear"

        assert forgot_screen.req_btn.isEnabled(), \
            "Request button should be re-enabled after failed flow"