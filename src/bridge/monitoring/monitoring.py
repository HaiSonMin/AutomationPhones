"""
MonitoringBridge - PyWebView Bridge for Device Monitoring

Exposes device monitoring APIs to React UI.
Follows the existing bridge pattern for auto-discovery by BridgeRegistry.

React can call these methods via:
    window.pywebview.api.monitoring_get_devices()
    window.pywebview.api.monitoring_connect_device("abc123")
    etc.

Example usage:
    # In React
    const devices = await window.pywebview.api.monitoring_get_devices();
    await window.pywebview.api.monitoring_connect_device(deviceId);
    await window.pywebview.api.monitoring_set_fps(deviceId, 30);
"""

import json
import time
from typing import Optional, List
from features.monitoring import DeviceManager


class MonitoringBridge:
    """
    Bridge class for device monitoring

    Provides methods for:
    - Getting device list
    - Connecting/disconnecting devices
    - Changing FPS and size settings
    - Receiving device change events

    This class follows the existing bridge pattern:
    - Methods are auto-discovered by BridgeRegistry
    - Window reference is passed via set_window()
    - Events are pushed to React via window.evaluate_js()
    """

    def __init__(self):
        """Initialize the monitoring bridge"""
        self._window = None
        self._manager = DeviceManager()

        # Set up callback to push events to React
        self._manager.on_devices_changed = self._on_devices_changed

        print("[MonitoringBridge] Initialized")

    # =========================================================================
    # LIFECYCLE METHODS
    # =========================================================================

    def set_window(self, window):
        """
        Set pywebview window reference

        Called by BridgeRegistry when window is created.
        This is required for pushing events to React.

        Args:
            window: pywebview window instance
        """
        self._window = window

        # Start device manager when window is ready
        self._manager.start()
        print("[MonitoringBridge] Window set, device manager started")

    # =========================================================================
    # API METHODS - Device List
    # =========================================================================

    def get_devices(self) -> List[dict]:
        """
        Get all connected devices

        Returns:
            List of device dictionaries with:
            - device_id: str - ADB serial number
            - model: str - Device model name
            - state: str - Current state (online, streaming, error, etc.)
            - fps: int - Current FPS setting
            - max_size: int - Current max size setting
            - is_streaming: bool - Whether currently streaming
            - can_connect: bool - Whether can start streaming
            - error: str | None - Error message if any

        Example:
            >>> devices = await window.pywebview.api.monitoring_get_devices()
            >>> console.log(devices)
            [
                {
                    "device_id": "abc123",
                    "model": "SM-M205G",
                    "state": "online",
                    "fps": 30,
                    "max_size": 800,
                    "is_streaming": false,
                    "can_connect": true,
                    "error": null
                }
            ]
        """
        return self._manager.get_all_devices()

    def get_device(self, device_id: str) -> Optional[dict]:
        """
        Get a specific device by ID

        Args:
            device_id: ADB device serial number

        Returns:
            Device dictionary or None if not found
        """
        return self._manager.get_device(device_id)

    def refresh_devices(self) -> List[dict]:
        """
        Force refresh the device list

        Triggers a new ADB scan and returns updated list.

        Returns:
            Updated list of devices
        """
        return self._manager.refresh_devices()

    # =========================================================================
    # API METHODS - Device Control
    # =========================================================================

    def connect_device(self, device_id: str) -> dict:
        print(f"\n{'='*50}")
        print(f"[MonitoringBridge] connect_device called with device_id: {device_id}")
        print(f"[MonitoringBridge] Current time: {time.strftime('%H:%M:%S')}")
        print(f"{'='*50}\n")

        # Check if manager is running
        if not self._manager.is_running:
            print(f"[MonitoringBridge] ERROR: DeviceManager is not running!")
            return {"success": False, "error": "Device manager not running"}

        # Get device count
        print(f"[MonitoringBridge] Current device count: {self._manager.device_count}")
        print(
            f"[MonitoringBridge] Currently streaming: {self._manager.streaming_count}"
        )

        # Call manager's connect_device
        print(f"[MonitoringBridge] Calling manager.connect_device...")
        result = self._manager.connect_device(device_id)
        print(f"[MonitoringBridge] manager.connect_device returned: {result}")

        return result

    def disconnect_device(self, device_id: str) -> dict:
        """
        Stop streaming for a device

        Terminates the scrcpy process.

        Args:
            device_id: ADB device serial number

        Returns:
            Result dictionary:
            - success: bool
            - error: str (if failed)
        """
        print(f"[MonitoringBridge] disconnect_device({device_id})")
        return self._manager.disconnect_device(device_id)

    def disconnect_all(self) -> dict:
        """
        Disconnect all streaming devices

        Useful for cleanup or when closing the app.

        Returns:
            Result dictionary:
            - success: bool
            - count: int - Number of devices disconnected
        """
        print("[MonitoringBridge] disconnect_all()")
        return self._manager.disconnect_all()

    # =========================================================================
    # API METHODS - Settings
    # =========================================================================

    def set_fps(self, device_id: str, fps: int) -> dict:
        """
        Change FPS for a device

        If device is currently streaming, this will restart the stream
        with the new FPS setting.

        Args:
            device_id: ADB device serial number
            fps: New FPS value (1-120, recommended: 15, 30, 60)

        Returns:
            Result dictionary:
            - success: bool
            - fps: int - The actual FPS set (may be clamped)
            - error: str (if failed)

        Example:
            >>> await window.pywebview.api.monitoring_set_fps("abc123", 30)
        """
        print(f"[MonitoringBridge] set_fps({device_id}, {fps})")
        return self._manager.set_device_fps(device_id, fps)

    def set_size(self, device_id: str, max_size: int) -> dict:
        """
        Change max display size for a device

        If device is currently streaming, this will restart the stream
        with the new size setting.

        Args:
            device_id: ADB device serial number
            max_size: Max dimension in pixels (0=original, 480-2048)
                      Recommended values: 480, 720, 800, 1080, 1440

        Returns:
            Result dictionary:
            - success: bool
            - max_size: int - The actual size set
            - error: str (if failed)

        Example:
            >>> await window.pywebview.api.monitoring_set_size("abc123", 800)
        """
        print(f"[MonitoringBridge] set_size({device_id}, {max_size})")
        return self._manager.set_device_size(device_id, max_size)

    def set_settings(
        self, device_id: str, fps: int = None, max_size: int = None
    ) -> dict:
        """
        Update multiple settings at once

        More efficient than calling set_fps and set_size separately
        when changing both settings.

        Args:
            device_id: ADB device serial number
            fps: New FPS (optional, pass None to keep current)
            max_size: New max size (optional, pass None to keep current)

        Returns:
            Result dictionary with success/error and final values
        """
        print(
            f"[MonitoringBridge] set_settings({device_id}, fps={fps}, size={max_size})"
        )
        return self._manager.set_device_settings(device_id, fps, max_size)

    # =========================================================================
    # API METHODS - Stats
    # =========================================================================

    def get_stats(self) -> dict:
        """
        Get monitoring statistics

        Returns:
            Dictionary with:
            - device_count: int - Total devices tracked
            - streaming_count: int - Devices currently streaming
            - is_running: bool - Whether manager is active
        """
        return {
            "device_count": self._manager.device_count,
            "streaming_count": self._manager.streaming_count,
            "is_running": self._manager.is_running,
        }

    # =========================================================================
    # PRIVATE METHODS - Event Handling
    # =========================================================================

    def _on_devices_changed(self, devices: List[dict]):
        """
        Callback when device list changes

        Pushes event to React via window.evaluate_js()
        React should listen for 'monitoring-devices-changed' event.

        Args:
            devices: Updated list of device dictionaries
        """
        if not self._window:
            return

        try:
            # Convert to JSON string for JavaScript
            devices_json = json.dumps(devices)

            # Dispatch custom event in React
            js_code = f"""
                (function() {{
                    const event = new CustomEvent('monitoring-devices-changed', {{
                        detail: {{ devices: {devices_json} }}
                    }});
                    window.dispatchEvent(event);
                }})();
            """

            self._window.evaluate_js(js_code)

        except Exception as e:
            print(f"[MonitoringBridge] Error pushing event: {e}")

    # =========================================================================
    # CLEANUP
    # =========================================================================

    def cleanup(self):
        """
        Cleanup resources

        Call this when closing the application.
        """
        print("[MonitoringBridge] Cleaning up...")
        self._manager.stop()


# =============================================================================
# BRIDGE INSTANCE
# =============================================================================

# Singleton instance for auto-discovery by BridgeRegistry
# BridgeRegistry looks for {module_name}_bridge in each bridge module
monitoring_bridge = MonitoringBridge()
