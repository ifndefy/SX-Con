from PyQt6.QtWidgets import QApplication, QDialog

from ui.core.theme_manager import ThemeManager
from ui.prompts.answer_sec_q import AnsSecQDialog
from ui.prompts.forgot_pw import ForgotPasswordScreen
from ui.prompts.login import LoginScreen
from unittest.mock import patch

"""
Sequence:
    ### 1 - Open program and land on login screen
    ### 2 - Click the Forgot Password button
    ### 3 - Enter the username and click the "Request" button
    ### 4 - Find the real AnsSecQDialog and simulate rejection by entering wrong answers
    ### 5 - Assert the warning message WAS shown (wrong answers rejected)
    ### 6 - Assert the request button is still enabled (user can retry)
"""


"""
   purpose: implement a test for answering wrong answers on security questions to check it doesn't go through.
   return: none
   author: Kyle Valdez
"""

def test_e2e_fail_forgot_password_wrong_security_answer(app):

    ### 1 - Open program and land on login screen
    theme_manager = ThemeManager()
    login_screen = LoginScreen(theme_manager)

    with patch("ui.prompts.login.ForgotPasswordScreen.exec"), \
            patch("ui.prompts.forgot_pw.AnsSecQDialog.exec"), \
            patch("ui.prompts.answer_sec_q.QMessageBox.warning") as mock_question_warning:

        ### 2 - Click the Forgot Password button
        login_screen.forgot_pw_btn.click()
        QApplication.processEvents()

        # Find the "Password Reset" dialog that was just created
        forgot_password_screen = None
        for w in QApplication.topLevelWidgets():
            if isinstance(w, ForgotPasswordScreen):
                forgot_password_screen = w

        assert forgot_password_screen, "Expected the Password Reset dialog to appear"

        ### 3 - Enter the username and click the "Request" button
        forgot_password_screen.username_input.setText("user")
        forgot_password_screen.req_btn.click()

        # Find the "Answer Security Questions" dialog that was just created
        answer_security_q_dialog = None
        for w in QApplication.topLevelWidgets():
            if isinstance(w, AnsSecQDialog):
                answer_security_q_dialog = w

        assert answer_security_q_dialog, "Expected the Security Questions Dialog to appear"

        ### 4 - Enter WRONG security question answers and click the "Update" button
        answer_security_q_dialog.answer1_input.setText("wrong_answer")
        answer_security_q_dialog.answer2_input.setText("wrong_answer")
        answer_security_q_dialog.update_btn.click()
        QApplication.processEvents()

        ### 5 - Assert the warning WAS shown (wrong answers should trigger a warning)
        assert mock_question_warning.called, \
            "Expected a warning message to display for incorrect security question answers."

        ### 6 - Assert the request button is still enabled so the user can retry
        assert forgot_password_screen.req_btn.isEnabled(), \
            "Request button should remain enabled after a failed security answer attempt."
