from unittest.mock import patch

from ui.core.theme_manager import ThemeManager
from ui.prompts.login import LoginScreen
from src.user import current_user

"""
Sequence:
    ### 1 - open program
    ### 2 - populate login fields with invalid data
    ### 3 - attempt to login
    ### 4 - verify error message
    ### 5 - verify ability to login again
    ### 6 - verify the fields are unchanged
"""

def test_e2e_fail_login(app):

    #1 open program
    theme_manager = ThemeManager()
    login_screen = LoginScreen(theme_manager)

    assert isinstance(login_screen, LoginScreen), "Make sure we open the login screen"
    assert login_screen.login_btn.isEnabled(), "Make sure the login button is enabled"
    assert login_screen.forgot_pw_btn.isEnabled(), "Make sure the forgot password button is enabled"

    #2 populate fields with invalid data
    login_screen.username = "garbage"
    login_screen.password = "garbage"

    #3 attempt to login
    with patch("ui.prompts.login.QMessageBox.warning") as mock_warning:
        login_screen.login_btn.click()

        #4 verify error message sent
        assert mock_warning.called
        assert login_screen.login_btn.clicked

        args = mock_warning.call_args[0]
        text = str(args)

        #5 verify contents of the error message
        assert "Invalid username or password!" in text

        assert not current_user == "garbage", "We should not have logged in"

        # 6 verify ability to login again
        assert login_screen.login_btn.isEnabled(), "We should still be able to log in"
        assert login_screen.forgot_pw_btn.isEnabled(), "We should still be able to change password"

        #7 verify that the fields remain unchanged
        assert login_screen.username == "garbage"
        assert login_screen.password == "garbage"