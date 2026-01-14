"""
Auth Bridge - Handles authentication from React UI
Token stored securely in Python keyring
"""

import json
import keyring
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
        self._window = None
        print("🔐 AuthBridge initialized")

    def set_window(self, window):
        """Set window reference for maximizing after login"""
        self._window = window

    # ============================================
    # Login Handler - Called by React after successful login
    # ============================================

    def on_login_success(self, token: str, user: IUser) -> Dict[str, Any]:
        print("user::::", user)
        """
        Called by React after successful login API response
        Saves token and user data to keyring, then registers PC with server

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

            # Register PC with server
            try:
                from utils.util_system import (
                    get_computer_name,
                    get_machine_guid,
                    get_pc_ip,
                    get_os_info,
                )
                from apis import api_pc, CreatePCPhoneDto

                # Get PC information
                pc_name = get_computer_name()
                machine_guid = get_machine_guid()
                pc_ip = get_pc_ip()
                os_info = get_os_info()

                # Create payload
                payload: CreatePCPhoneDto = {
                    "name": pc_name,
                    "alias": pc_name,  # Default alias to name
                    "machineGUID": machine_guid,
                    "ip": pc_ip,
                    "os": os_info,
                }

                # Register PC
                print("🖥️ Registering PC with server...")
                pc_result = api_pc.create(payload)

                # Check if successful (statusCode 200 or 201)
                if pc_result.get("statusCode") in [200, 201]:
                    print("✅ PC registered successfully")
                else:
                    print(
                        f"⚠️ PC registration failed: {pc_result.get('reasonStatusCode')}"
                    )
                    # Don't block login on PC registration failure

            except Exception as pc_error:
                print(f"⚠️ PC registration error (non-blocking): {pc_error}")
                # Don't block login on PC registration failure

            # Maximize window after successful login
            if self._window:
                self._window.maximize()
                print("📐 Window maximized")

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

            return {"success": True, "message": "Logged out successfully"}
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
