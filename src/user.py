import bcrypt
from typing import Optional, Tuple

from dulwich.porcelain import fetch

from services.get_item_by_property import get_item_by_property
from services.get_property import get_property


class User:
    """
    purpose: Global user object to store authenticated user information
    author(s): Alexander Bubienko
    """
    
    # Class-level variables to store the current user
    _instance = None
    _hashed_username = None
    _hashed_admin = None
    _raw_username = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    @staticmethod
    def _hash_value(value: str) -> str:
        """
        purpose: Hash a string value using bcrypt
        author(s): Alexander Bubienko
        return: Hashed string or "-1" on error
        """
        try:
            if not isinstance(value, str) or not value:
                return "-1"
            
            salt = bcrypt.gensalt(rounds=12)
            hashed = bcrypt.hashpw(value.encode("utf-8"), salt)
            return hashed.decode("utf-8")
        except Exception:
            return "-1"
    
    def set_user(self, username: str, admin_status: bool) -> bool:
        """
        purpose: Store logged-in user information (hashed)
        author(s): Alexander Bubienko
        return: True if successful, False otherwise
        """
        try:
            self._raw_username = username
            self._hashed_username = self._hash_value(username)
            self._hashed_admin = self._hash_value(str(admin_status))
            self._admin_status = admin_status
            
            return (self._hashed_username != "-1" and 
                    self._hashed_admin != "-1")
        except Exception:
            return False
    
    def get_username(self) -> Optional[str]:
        """
        purpose: Return the unhashed username
        author(s): Alexander Bubienko
        return: Raw username string or None if not set
        """
        return self._raw_username
    
    def get_hashed_username(self) -> Optional[str]:
        """
        purpose: Return the hashed username (for internal use)
        author(s): Alexander Bubienko
        return: Hashed username string or None if not set
        """
        return self._hashed_username
    
    def get_hashed_admin(self) -> Optional[str]:
        """
        purpose: Return the hashed admin status (for internal use)
        author(s): Alexander Bubienko
        return: Hashed admin status string or None if not set
        """
        return self._hashed_admin

    def fetch_user_data(self):
        """
        purpose: Fetch user data from database
        author(s): Joe Lee
        """
        user_data = get_item_by_property("Entities", "user", "username", self.get_username())
        return user_data

    def get_user_id(self):
        """
        purpose: Return user id or None if offline
        author(s): Joe Lee
        """
        if not self._raw_username:
            return ""
        try:
            user_data = self.fetch_user_data()
            if not user_data:
                return ""
            return user_data["user_id"]
        except Exception:
            return ""

    def get_user_full_name(self):
        """
        purpose: Return the user's full name or empty string if offline
        author(s): Joe Lee
        """
        if not self._raw_username:
            return ""
        try:
            user_data = self.fetch_user_data()
            if not user_data:
                return ""
            return " ".join([user_data["first_name"], user_data["last_name"]])
        except Exception:
            return ""

    def is_admin(self) -> bool:
        """
        purpose: Check if current user is an admin
        author(s): Alexander Bubienko
        return: True if admin, False otherwise
        """
        # Note: This is a convenience method
        # The actual admin status would need to be verified against the database
        # For now, we'll store and verify against the stored raw value
        return self._raw_username is not None and hasattr(self, '_admin_status') and self._admin_status
    
    def clear_user(self):
        """
        purpose: Clear user data on logout
        author(s): Alexander Bubienko
        """
        self._hashed_username = None
        self._hashed_admin = None
        self._raw_username = None
        self._admin_status = False


# Create a global instance for easy import
current_user = User()