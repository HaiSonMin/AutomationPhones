"""
Services Center - Main service coordinator
Integrates all services with user authentication
"""

from ..bridge.auth.auth import auth_bridge


class ServicesCenter:
    def __init__(self):
        self.display_user_info()

    def display_user_info(self):
        """Display current authenticated user information"""
        user_data = auth_bridge.get_current_user()

        if user_data:
            print(f"  - ID: {user_data.get('user_id', 'N/A')}")
            print(f"  - Họ và tên: {user_data.get('user_fullName', 'N/A')}")
            print(f"  - Email: {user_data.get('user_email', 'N/A')}")
            print(f"  - Tên đăng nhập: {user_data.get('user_name', 'N/A')}")
            print(f"  - Vai trò: {user_data.get('user_role', 'N/A')}")
            print(f"  - Điện thoại: {user_data.get('user_phone', 'N/A')}")

            # Store user_id for services
            self.user_id = str(user_data.get("user_id", ""))
            self.user_data = user_data
        else:
            print("  - Chưa đăng nhập")
            self.user_id = None
            self.user_data = None
