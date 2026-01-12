"""
MonitoringBridge - PyWebView Bridge for Device Monitoring

Features:
- Native scrcpy windows for interactive control (35-70ms latency)
"""

import json
from typing import Optional, List

from features.monitoring import DeviceManager


class MonitoringBridge:
    """
    Bridge for Monitoring with scrcpy windows
    """

    def __init__(self):
        self._window = None
        self._manager = DeviceManager()
        self._manager.set_on_devices_changed(self._on_devices_changed)
        print("[MonitoringBridge] Initialized")

    def set_window(self, window):
        """Set pywebview window reference"""
        self._window = window
        self._manager.start()
        print("[MonitoringBridge] Window set, device manager started")

    # =========================================================================
    # API METHODS - Device List
    # =========================================================================

    def get_devices(self, force_refresh: bool = False) -> List[dict]:
        """Get all connected devices"""
        return self._manager.get_all_devices(force_refresh=force_refresh)

    def refresh_devices(self) -> List[dict]:
        """Force refresh device list"""
        return self._manager.get_all_devices(force_refresh=True)

    def get_device(self, device_id: str) -> Optional[dict]:
        """Get a specific device by ID"""
        return self._manager.get_device(device_id)

    # =========================================================================
    # API METHODS - Window Control
    # =========================================================================

    def open_window(self, device_id: str) -> dict:
        """Open scrcpy window for interactive control"""
        print(f"[MonitoringBridge] open_window({device_id})")
        return self._manager.open_window(device_id)

    def close_window(self, device_id: str) -> dict:
        """Close scrcpy window"""
        print(f"[MonitoringBridge] close_window({device_id})")
        return self._manager.close_window(device_id)

    def stop_all(self) -> dict:
        """Close all windows"""
        print("[MonitoringBridge] stop_all()")
        return self._manager.stop_all()

    # =========================================================================
    # API METHODS - Settings
    # =========================================================================

    def get_settings(self) -> dict:
        """Get current settings"""
        return self._manager.get_settings()

    def update_settings(self, settings: dict = None, **kwargs) -> dict:
        """Update settings"""
        if settings:
            kwargs.update(settings)
        return self._manager.update_settings(**kwargs)

    # =========================================================================
    # API METHODS - Stats
    # =========================================================================

    def get_stats(self) -> dict:
        """Get monitoring statistics"""
        devices = self._manager.get_all_devices()
        windowed = [d for d in devices if d.get("has_window")]

        return {
            "device_count": len(devices),
            "window_count": len(windowed),
            "is_running": True,
            "is_available": self._manager.is_available,
        }

    def is_available(self) -> bool:
        """Check if scrcpy is installed"""
        return self._manager.is_available

    # =========================================================================
    # PRIVATE - Event Pushing
    # =========================================================================

    def _on_devices_changed(self, devices: List[dict]):
        """Push device changes to React"""
        if not self._window:
            return

        try:
            devices_json = json.dumps(devices)
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
            if "failed to start" not in str(e).lower():
                print(f"[MonitoringBridge] Error pushing devices: {e}")

    def cleanup(self):
        """Cleanup resources"""
        print("[MonitoringBridge] Cleaning up...")
        self._manager.stop()


# Singleton instance
monitoring_bridge = MonitoringBridge()
