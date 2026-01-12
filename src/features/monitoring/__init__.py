"""
Monitoring Package

Features:
- Device detection via ADB
- Native scrcpy windows for device control (35-70ms latency)
"""

from .device_watcher import DeviceWatcher, DetectedDevice, AdbDeviceStatus
from .scrcpy_window_manager import ScrcpyWindowManager
from .device_manager import DeviceManager

__all__ = [
    "DeviceWatcher",
    "DetectedDevice",
    "AdbDeviceStatus",
    "ScrcpyWindowManager",
    "DeviceManager",
]
