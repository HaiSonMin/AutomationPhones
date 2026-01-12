"""
DeviceWatcher - Monitor USB-connected Android devices via ADB

Detects device connect/disconnect and status changes.
"""

import subprocess
import threading
import time
import re
from dataclasses import dataclass
from typing import Optional, Callable, Dict
from enum import Enum


class AdbDeviceStatus(Enum):
    """ADB device status"""

    ONLINE = "device"
    OFFLINE = "offline"
    UNAUTHORIZED = "unauthorized"
    UNKNOWN = "unknown"


@dataclass
class DetectedDevice:
    """Detected device info"""

    device_id: str
    status: AdbDeviceStatus
    model: Optional[str] = None


# Callback types
DeviceAddedCallback = Callable[[DetectedDevice], None]
DeviceRemovedCallback = Callable[[str], None]
DeviceChangedCallback = Callable[[DetectedDevice], None]


class DeviceWatcher:
    """
    Watch for USB device connections using ADB

    Polls `adb devices` periodically to detect changes.
    """

    ADB_PATH: str = "adb"
    POLL_INTERVAL: float = 2.0

    def __init__(self):
        self._devices: Dict[str, DetectedDevice] = {}
        self._running = False
        self._thread: Optional[threading.Thread] = None
        self._lock = threading.Lock()

        # Callbacks
        self.on_device_added: Optional[DeviceAddedCallback] = None
        self.on_device_removed: Optional[DeviceRemovedCallback] = None
        self.on_device_changed: Optional[DeviceChangedCallback] = None

    def start(self) -> None:
        """Start watching for devices"""
        if self._running:
            return

        self._running = True
        self._thread = threading.Thread(target=self._watch_loop, daemon=True)
        self._thread.start()
        print("[DeviceWatcher] Started")

    def stop(self) -> None:
        """Stop watching"""
        self._running = False
        if self._thread:
            self._thread.join(timeout=3)
        print("[DeviceWatcher] Stopped")

    def get_devices(self) -> Dict[str, DetectedDevice]:
        """Get current devices"""
        with self._lock:
            return dict(self._devices)

    def _watch_loop(self) -> None:
        """Main polling loop"""
        while self._running:
            try:
                self._poll_devices()
            except Exception as e:
                print(f"[DeviceWatcher] Poll error: {e}")

            time.sleep(self.POLL_INTERVAL)

    def _poll_devices(self) -> None:
        """Poll ADB for device list"""
        try:
            result = subprocess.run(
                [self.ADB_PATH, "devices", "-l"],
                capture_output=True,
                text=True,
                timeout=5,
            )

            new_devices: Dict[str, DetectedDevice] = {}

            for line in result.stdout.strip().split("\n"):
                if not line or line.startswith("List of"):
                    continue

                # Parse line: "SERIAL device product:... model:... device:..."
                parts = line.split()
                if len(parts) < 2:
                    continue

                device_id = parts[0]
                status_str = parts[1]

                # Map status
                status_map = {
                    "device": AdbDeviceStatus.ONLINE,
                    "offline": AdbDeviceStatus.OFFLINE,
                    "unauthorized": AdbDeviceStatus.UNAUTHORIZED,
                }
                status = status_map.get(status_str, AdbDeviceStatus.UNKNOWN)

                # Extract model
                model = None
                for part in parts[2:]:
                    if part.startswith("model:"):
                        model = part.split(":")[1].replace("_", " ")
                        break

                new_devices[device_id] = DetectedDevice(
                    device_id=device_id,
                    status=status,
                    model=model,
                )

            # Compare with current devices
            self._compare_and_update(new_devices)

        except subprocess.TimeoutExpired:
            print("[DeviceWatcher] ADB timeout")
        except FileNotFoundError:
            print(f"[DeviceWatcher] ADB not found at: {self.ADB_PATH}")

    def _compare_and_update(self, new_devices: Dict[str, DetectedDevice]) -> None:
        """Compare new devices with current and emit callbacks"""
        with self._lock:
            old_ids = set(self._devices.keys())
            new_ids = set(new_devices.keys())

            # Added devices
            for device_id in new_ids - old_ids:
                device = new_devices[device_id]
                self._devices[device_id] = device
                if self.on_device_added:
                    try:
                        self.on_device_added(device)
                    except Exception as e:
                        print(f"[DeviceWatcher] Callback error: {e}")

            # Removed devices
            for device_id in old_ids - new_ids:
                del self._devices[device_id]
                if self.on_device_removed:
                    try:
                        self.on_device_removed(device_id)
                    except Exception as e:
                        print(f"[DeviceWatcher] Callback error: {e}")

            # Changed devices
            for device_id in old_ids & new_ids:
                old = self._devices[device_id]
                new = new_devices[device_id]

                if old.status != new.status or old.model != new.model:
                    self._devices[device_id] = new
                    if self.on_device_changed:
                        try:
                            self.on_device_changed(new)
                        except Exception as e:
                            print(f"[DeviceWatcher] Callback error: {e}")
