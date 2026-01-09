import requests
import subprocess
import psutil
from datetime import datetime
from typing import Dict, Any

from constants.constant_value import CONST_VAL_SERVER_URL
from interfaces.interface_response import IResponse
from bridge.auth.auth import auth_bridge

# Global variable to track application state
app_running = False

# from concurrent.futures import ThreadPoolExecutor

# ThreadPoolExecutor
# MAX_WORKERS = 1
# with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
#     executor.submit(FeatureToolCommon().check_health_server)


class FeatureToolCommon:
    def __init__(self):
        user_result = auth_bridge.get_current_user()
        self.user = user_result.get("user") if user_result.get("success") else None
        print("User:::", self.user)

    def check_health_server(self) -> Dict[str, Any]:
        """
        Check server health status
        Returns:
            Dict with health status information
        """
        try:
            # Check server connectivity
            response = requests.get(f"{CONST_VAL_SERVER_URL}/health", timeout=5)
            result = response.json()
            # Handle both dict and object responses
            if isinstance(result, dict):
                server_ok = result.get("statusCode", response.status_code) == 200
            else:
                server_ok = getattr(result, "statusCode", response.status_code) == 200

            # Check database (simulate)
            database_ok = True  # TODO: Implement actual database check

            # Get connected devices count
            devices_count = self._get_connected_devices_count()

            return {
                "server": server_ok,
                "database": database_ok,
                "devices": devices_count,
                "lastCheck": datetime.now().strftime("%H:%M:%S"),
            }
        except Exception as e:
            print(f"Health check failed: {e}")
            return {
                "server": False,
                "database": False,
                "devices": 0,
                "lastCheck": datetime.now().strftime("%H:%M:%S"),
            }

    def start_stop(self) -> Dict[str, Any]:
        """
        Start or stop the application
        Returns:
            Dict with operation result
        """
        global app_running
        try:
            if not app_running:
                # Start the application
                print("Starting phone app...")
                # TODO: Implement actual phone app start logic
                app_running = True
                return {
                    "success": True,
                    "message": "Phone app started successfully",
                    "running": True,
                }
            else:
                # Stop the application
                print("Stopping phone app...")
                # TODO: Implement actual phone app stop logic
                app_running = False
                return {
                    "success": True,
                    "message": "Phone app stopped successfully",
                    "running": False,
                }
        except Exception as e:
            print(f"Start/stop failed: {e}")
            return {"success": False, "message": str(e), "running": app_running}

    def get_app_state(self) -> Dict[str, Any]:
        """
        Get current application state
        Returns:
            Dict with current app state
        """
        global app_running
        return {"running": app_running}

    def _get_connected_devices_count(self) -> int:
        """Get number of connected devices"""
        try:
            # Use adb to get connected devices
            result = subprocess.run(
                ["adb", "devices"], capture_output=True, text=True, timeout=5
            )

            # Parse output to count devices
            lines = result.stdout.strip().split("\n")[1:]  # Skip first line
            devices = [line for line in lines if line.strip() and "\tdevice" in line]
            return len(devices)
        except:
            return 0
