"""
Auth Bridge - Handles authentication events from React UI
Token stored securely in Python keyring
"""

import keyring
import json
from typing import Dict, Any, Optional

# Keyring service configuration
SERVICE_NAME = "AutomationToolPhones"
TOKEN_KEY = "auth_token"
USER_KEY = "auth_user"


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

    def on_login_success(self, token: str, user: dict) -> Dict[str, Any]:
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

            user_name = user.get("user_fullName", "Unknown")
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

    def get_token(self) -> Optional[str]:
        """Get stored token"""
        try:
            return keyring.get_password(SERVICE_NAME, TOKEN_KEY)
        except Exception:
            return None

    def get_current_user(self) -> Optional[dict]:
        """Get stored user data"""
        try:
            user_json = keyring.get_password(SERVICE_NAME, USER_KEY)
            if user_json:
                return json.loads(user_json)
            return None
        except Exception:
            return None

    def is_authenticated(self) -> bool:
        """Check if user is authenticated"""
        token = self.get_token()
        return token is not None and token != ""


# Singleton instance
auth_bridge = AuthBridge()
