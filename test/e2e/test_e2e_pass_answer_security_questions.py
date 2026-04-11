from PyQt6.QtWidgets import QApplication

from ui.core.theme_manager import ThemeManager
from ui.prompts.answer_sec_q import AnsSecQDialog
from ui.prompts.forgot_pw import ForgotPasswordScreen
from ui.prompts.login import LoginScreen
from unittest.mock import patch

"""
Sequence:
    ### 1 - Open program and land on login screen
    ### 2 - Click the Forgot Password button
    ### 3 - Enter the username and click the "Request for username" button
    ### 4 - Enter the new security question answers and click the "Update" button
    ### 5 - Assert no warning was called
"""

def test_e2e_pass_answer_security_questions(app):
    """
    :purpose: Serves as a simple test to check that correct security answers can be verified through UI
    :return: None
    :author(s): Colin Heinselman
    """

    ### 1 - Open program and land on login screen
    theme_manager = ThemeManager()
    login_screen = LoginScreen(theme_manager)

    with patch("ui.tabs.settings.QMessageBox.critical") as mock_warning, \
            patch('ui.tabs.settings.QMessageBox.warning') as mock_login_warning, \
            patch("ui.tabs.settings.SecurityQuestionsDialog.exec"), \
            patch("ui.prompts.login.ForgotPasswordScreen.exec"), \
            patch("ui.prompts.forgot_pw.AnsSecQDialog.exec"), \
            patch("ui.prompts.answer_sec_q.QMessageBox.warning") as mock_question_warning:

        ### 2 - Click the Forgot Password button
        login_screen.forgot_pw_btn.click()
        QApplication.processEvents()

        # Find the "Password Reset" dialog that was just created
        for w in QApplication.topLevelWidgets():
            if isinstance(w, ForgotPasswordScreen):
                forgot_password_screen = w

        assert forgot_password_screen, "Expected the Password Reset dialog to appear"

        ### 3 - Enter the username and click the "Request for username" button
        forgot_password_screen.username_input.setText("user")
        forgot_password_screen.req_btn.click()

        # Find the "Answer Security Questions" dialog that was just created
        for w in QApplication.topLevelWidgets():
            if isinstance(w, AnsSecQDialog):
                answer_security_q_dialog = w

        assert answer_security_q_dialog, "Expected the Security Questions Dialog to appear"


        ### 4 - Enter the new security question answers and click the "Update" button
        answer_security_q_dialog.answer1_input.setText("asdf")
        answer_security_q_dialog.answer2_input.setText("asdf")
        answer_security_q_dialog.update_btn.click()
        QApplication.processEvents()

        ### 5 - Assert no warning was called
        assert not mock_question_warning.called, "Expected no warning message to display for correct security question answers."