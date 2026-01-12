"""
DeviceManager - Device manager with scrcpy windows

Features:
- Auto-detect USB devices
- Scrcpy window for interactive control (35-70ms latency)
"""

import threading
import time
from dataclasses import dataclass
from typing import Dict, Optional, Callable, List
from enum import Enum

from .device_watcher import DeviceWatcher, DetectedDevice, AdbDeviceStatus
from .scrcpy_window_manager import ScrcpyWindowManager


class DeviceState(Enum):
    """Device state for UI"""

    OFFLINE = "offline"
    UNAUTHORIZED = "unauthorized"
    ONLINE = "online"
    INTERACTIVE = "interactive"
    ERROR = "error"


@dataclass
class ManagedDevice:
    """Device state for monitoring"""

    device_id: str
    model: str = "Unknown"
    adb_status: AdbDeviceStatus = AdbDeviceStatus.UNKNOWN
    state: DeviceState = DeviceState.OFFLINE
    has_window: bool = False
    error: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "device_id": self.device_id,
            "model": self.model,
            "adb_status": (
                self.adb_status.value
                if isinstance(self.adb_status, Enum)
                else self.adb_status
            ),
            "state": self.state.value if isinstance(self.state, Enum) else self.state,
            "is_online": self.adb_status == AdbDeviceStatus.ONLINE,
            "has_window": self.has_window,
            "error": self.error,
        }


# Callback types
DevicesChangedCallback = Callable[[List[dict]], None]


class DeviceManager:
    """
    Device manager with scrcpy windows

    Features:
    - Auto-detect USB devices via DeviceWatcher
    - Scrcpy window per device (interactive, 35-70ms latency)
    """

    def __init__(self, adb_path: str = "adb"):
        print("[DeviceManager] Initializing...")

        self._adb_path = adb_path
        DeviceWatcher.ADB_PATH = adb_path

        # Components
        self._watcher = DeviceWatcher()
        self._window_manager = ScrcpyWindowManager()

        # State
        self._devices: Dict[str, ManagedDevice] = {}
        self._lock = threading.Lock()
        self._running = False

        # Callbacks
        self._on_devices_changed: Optional[DevicesChangedCallback] = None

        # Setup callbacks
        self._watcher.on_device_added = self._on_device_added
        self._watcher.on_device_removed = self._on_device_removed
        self._watcher.on_device_changed = self._on_device_changed
        self._window_manager.set_on_state_changed(self._on_window_state_changed)

        print("[DeviceManager] Initialized")

    def set_on_devices_changed(self, callback: DevicesChangedCallback) -> None:
        self._on_devices_changed = callback

    # =========================================================================
    # PUBLIC API - Lifecycle
    # =========================================================================

    def start(self) -> None:
        if self._running:
            return
        print("[DeviceManager] Starting...")
        self._running = True
        self._watcher.start()
        print("[DeviceManager] Started")

    def stop(self) -> None:
        if not self._running:
            return
        print("[DeviceManager] Stopping...")
        self._running = False
        self._watcher.stop()
        self._window_manager.close_all()
        print("[DeviceManager] Stopped")

    # =========================================================================
    # PUBLIC API - Device Access
    # =========================================================================

    def get_all_devices(self, force_refresh: bool = False) -> List[dict]:
        """Get all devices, optionally force refresh"""
        if force_refresh:
            # Trigger immediate poll
            self._watcher._poll_devices()

        with self._lock:
            return [d.to_dict() for d in self._devices.values()]

    def get_device(self, device_id: str) -> Optional[dict]:
        with self._lock:
            if device_id in self._devices:
                return self._devices[device_id].to_dict()
            return None

    # =========================================================================
    # PUBLIC API - Window Control
    # =========================================================================

    def open_window(self, device_id: str) -> dict:
        """Open scrcpy window for a device"""
        with self._lock:
            if device_id not in self._devices:
                return {"success": False, "error": "Device not found"}
            device = self._devices[device_id]
            if device.adb_status != AdbDeviceStatus.ONLINE:
                return {"success": False, "error": "Device not online"}

        result = self._window_manager.open_window(device_id)
        return result

    def close_window(self, device_id: str) -> dict:
        """Close scrcpy window"""
        result = self._window_manager.close_window(device_id)

        with self._lock:
            if device_id in self._devices:
                device = self._devices[device_id]
                device.has_window = False
                if device.adb_status == AdbDeviceStatus.ONLINE:
                    device.state = DeviceState.ONLINE

        self._emit_devices_changed()
        return result

    def stop_all(self) -> dict:
        """Close all windows"""
        self._window_manager.close_all()

        with self._lock:
            for device in self._devices.values():
                device.has_window = False
                if device.adb_status == AdbDeviceStatus.ONLINE:
                    device.state = DeviceState.ONLINE

        self._emit_devices_changed()
        return {"success": True}

    # =========================================================================
    # PUBLIC API - Settings
    # =========================================================================

    def get_settings(self) -> dict:
        return self._window_manager.get_settings()

    def update_settings(self, **window_settings) -> dict:
        """Update settings"""
        self._window_manager.update_settings(**window_settings)
        return self.get_settings()

    @property
    def is_available(self) -> bool:
        return self._window_manager.is_available

    # =========================================================================
    # PRIVATE - Callbacks
    # =========================================================================

    def _on_device_added(self, detected: DetectedDevice) -> None:
        print(f"[DeviceManager] Device added: {detected.device_id}")

        device = ManagedDevice(
            device_id=detected.device_id,
            model=detected.model or "Unknown",
            adb_status=detected.status,
            state=self._status_to_state(detected.status),
        )

        with self._lock:
            self._devices[detected.device_id] = device

        self._emit_devices_changed()

    def _on_device_removed(self, device_id: str) -> None:
        print(f"[DeviceManager] Device removed: {device_id}")

        self._window_manager.close_window(device_id)

        with self._lock:
            self._devices.pop(device_id, None)

        self._emit_devices_changed()

    def _on_device_changed(self, detected: DetectedDevice) -> None:
        with self._lock:
            if detected.device_id in self._devices:
                device = self._devices[detected.device_id]
                device.adb_status = detected.status
                device.model = detected.model or device.model

                if not device.has_window:
                    device.state = self._status_to_state(detected.status)

        self._emit_devices_changed()

    def _on_window_state_changed(self, device_id: str, state: str) -> None:
        print(f"[DeviceManager] Window state: {device_id} -> {state}")

        with self._lock:
            if device_id in self._devices:
                device = self._devices[device_id]

                if state == "running":
                    device.has_window = True
                    device.state = DeviceState.INTERACTIVE
                elif state in ("closed", "error"):
                    device.has_window = False
                    if device.adb_status == AdbDeviceStatus.ONLINE:
                        device.state = DeviceState.ONLINE
                    else:
                        device.state = self._status_to_state(device.adb_status)

        self._emit_devices_changed()

    # =========================================================================
    # PRIVATE - Helpers
    # =========================================================================

    def _status_to_state(self, status: AdbDeviceStatus) -> DeviceState:
        if status == AdbDeviceStatus.ONLINE:
            return DeviceState.ONLINE
        elif status == AdbDeviceStatus.UNAUTHORIZED:
            return DeviceState.UNAUTHORIZED
        elif status == AdbDeviceStatus.OFFLINE:
            return DeviceState.OFFLINE
        else:
            return DeviceState.ERROR

    def _emit_devices_changed(self) -> None:
        if self._on_devices_changed:
            try:
                devices = self.get_all_devices()
                self._on_devices_changed(devices)
            except Exception as e:
                print(f"[DeviceManager] Error emitting devices changed: {e}")
