"""
Auth Bridge - Handles authentication events from React UI
Token stored securely in Python keyring
"""

import keyring
import json
from typing import Dict, Any, TypedDict

# Keyring service configuration
SERVICE_NAME = "AutomationToolPhones"
TOKEN_KEY = "auth_token"
USER_KEY = "auth_user"


class IUser(TypedDict):
    userId: str
    userEmail: str
    userName: str
    userAvatar: str | None
    userIsRootAdmin: bool
    userIsSubAdmin: bool
    userIsLeader: bool
    userListRolesModule: Any | None


class AuthBridge:
    """
    Authentication Bridge between React UI and Python
    React calls these methods after successful API operations
    """

    def __init__(self):
        print("🔐 AuthBridge initialized")

    # ============================================
    # Login Handler - Called by React after successful login
    # ============================================

    def on_login_success(self, token: str, user: IUser) -> Dict[str, Any]:
        print("user::::", user)
        """
        Called by React after successful login API response
        Saves token and user data to keyring

        Args:
            token: JWT token from server
            user: User data from server

        Returns:
            Success/error response
        """
        try:
            # Save token to keyring
            keyring.set_password(SERVICE_NAME, TOKEN_KEY, token)

            # Save user data as JSON
            keyring.set_password(SERVICE_NAME, USER_KEY, json.dumps(user))

            user_name = user.get("userName", "Unknown")
            print(f"✅ Login successful - Token saved for: {user_name}")

            return {"success": True, "message": f"Token saved for {user_name}"}
        except Exception as e:
            print(f"❌ Error saving token: {e}")
            return {"success": False, "error": str(e)}

    # ============================================
    # Logout Handler - Called by React after logout
    # ============================================

    def on_logout(self) -> Dict[str, Any]:
        """
        Called by React when user logs out
        Clears token and user data from keyring

        Returns:
            Success/error response
        """
        try:
            # Clear token
            try:
                keyring.delete_password(SERVICE_NAME, TOKEN_KEY)
            except keyring.errors.PasswordDeleteError:
                pass  # Token doesn't exist

            # Clear user data
            try:
                keyring.delete_password(SERVICE_NAME, USER_KEY)
            except keyring.errors.PasswordDeleteError:
                pass  # User data doesn't exist

            print("✅ Logout successful - Token cleared")

            return {"success": True, "message": "Token cleared"}
        except Exception as e:
            print(f"❌ Error clearing token: {e}")
            return {"success": False, "error": str(e)}

    # ============================================
    # Token Getters - For Python to use internally
    # ============================================

    def get_token(self) -> Dict[str, Any]:
        """Get stored token"""
        try:
            token = keyring.get_password(SERVICE_NAME, TOKEN_KEY)
            if token:
                return {"success": True, "token": token}
            return {"success": False, "token": None}
        except Exception as e:
            return {"success": False, "token": None, "error": str(e)}

    def get_current_user(self) -> Dict[str, Any]:
        """Get stored user data"""
        try:
            user_json = keyring.get_password(SERVICE_NAME, USER_KEY)
            if user_json:
                return {"success": True, "user": json.loads(user_json)}
            return {"success": False, "user": None}
        except Exception as e:
            return {"success": False, "user": None, "error": str(e)}

    def is_authenticated(self) -> Dict[str, Any]:
        """Check if user is authenticated"""
        try:
            token = keyring.get_password(SERVICE_NAME, TOKEN_KEY)
            authenticated = token is not None and token != ""
            return {"authenticated": authenticated}
        except Exception:
            return {"authenticated": False}


# Singleton instance
auth_bridge = AuthBridge()
