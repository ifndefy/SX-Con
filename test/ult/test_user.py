from src.user import User
from src.user import current_user


def test_only_one_user():
    user1 = User()
    user2 = User()
    assert user1 is user2, "Expected user1 to be equal user2 as only one user is allowed"

def test_set_user_returns_true():
    user = User()
    result = user.set_user("test", False)
    assert result == True, "Expected to be able to set new username to 'test'"

def test_get_username_after_set():
    user = User()
    user.set_user("test", False)
    assert user.get_username() == "test", "Expected to retrieve 'test' as username"

def test_is_admin_false():
    user = User()
    user.set_user("test", False)
    assert user.is_admin() == False, "Expected user 'test' to not have admin status'"

def test_is_admin_true():
    user = User()
    user.set_user("test", True)
    assert user.is_admin() == True, "Expected user 'test' to have admin status"

def test_clear_user():
    user = User()
    user.set_user("test", True)
    user.clear_user()
    assert user.get_username() is None, "Expected user to be cleared"
    assert user.is_admin() == False, "Expected user to be not admin after being cleared"

def test_current_user_not_set_before_login():
    current_user.clear_user()
    assert current_user.get_username() is None, "Expected user to be cleared"
