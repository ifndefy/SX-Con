from unittest.mock import MagicMock

from src.user import User
from src.user import current_user
from ui.prompts.login import LoginScreen


def test_only_one_user():
    user1 = User()
    user2 = User()
    assert user1 is user2

def test_set_user_returns_true():
    user = User()
    result = user.set_user("test", False)
    assert result == True

def test_get_username_after_set():
    user = User()
    user.set_user("test", False)
    assert user.get_username() == "test"

def test_is_admin_false():
    user = User()
    user.set_user("test", False)
    assert user.is_admin() == False

def test_is_admin_true():
    user = User()
    user.set_user("test", True)
    assert user.is_admin() == True

def test_clear_user():
    user = User()
    user.set_user("test", True)
    user.clear_user()
    assert user.get_username() is None
    assert user.is_admin() == False

def test_current_user_not_set_before_login():
    current_user.clear_user()
    assert current_user.get_username() is None
