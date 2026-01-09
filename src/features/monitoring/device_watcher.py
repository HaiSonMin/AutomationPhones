"""
DeviceWatcher - USB Device Detection via ADB

Monitors for Android device connections/disconnections using ADB.
Runs in a background thread and emits events when devices change.

Architecture:
    DeviceWatcher runs `adb track-devices` which maintains a persistent
    connection to the ADB daemon. When devices connect/disconnect,
    ADB pushes updates through this connection.

Example usage:
    watcher = DeviceWatcher()
    watcher.on_device_added = lambda device: print(f"Added: {device}")
    watcher.on_device_removed = lambda device_id: print(f"Removed: {device_id}")
    watcher.start()
    # ... later
    watcher.stop()
"""

import subprocess
import threading
import time
from dataclasses import dataclass
from enum import Enum
from typing import Dict, Optional, Callable, List
import re


# =============================================================================
# ENUMS - Device status definitions
# =============================================================================


class AdbDeviceStatus(Enum):
    """
    ADB device connection states

    ONLINE       - Device connected and ready for commands
    OFFLINE      - Device connected but not responding
    UNAUTHORIZED - Device connected but USB debugging not authorized
    BOOTLOADER   - Device in bootloader/fastboot mode
    RECOVERY     - Device in recovery mode
    UNKNOWN      - Unknown state
    """

    ONLINE = "device"  # ADB reports "device" for online
    OFFLINE = "offline"
    UNAUTHORIZED = "unauthorized"
    BOOTLOADER = "bootloader"
    RECOVERY = "recovery"
    UNKNOWN = "unknown"

    @classmethod
    def from_adb_string(cls, status_str: str) -> "AdbDeviceStatus":
        """Convert ADB status string to enum"""
        status_map = {
            "device": cls.ONLINE,
            "offline": cls.OFFLINE,
            "unauthorized": cls.UNAUTHORIZED,
            "bootloader": cls.BOOTLOADER,
            "recovery": cls.RECOVERY,
        }
        return status_map.get(status_str.lower(), cls.UNKNOWN)


# =============================================================================
# DATA CLASSES
# =============================================================================


@dataclass
class DetectedDevice:
    """
    Information about a detected Android device

    Attributes:
        device_id: ADB serial number (USB or IP:port)
        status: Current connection status
        model: Device model name (e.g., "SM-M205G")
        product: Product code
        transport_id: ADB transport ID
    """

    device_id: str
    status: AdbDeviceStatus
    model: str = "Unknown"
    product: str = ""
    transport_id: str = ""

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization"""
        return {
            "device_id": self.device_id,
            "status": self.status.name.lower(),
            "model": self.model,
            "product": self.product,
            "transport_id": self.transport_id,
            "is_online": self.status == AdbDeviceStatus.ONLINE,
        }


# =============================================================================
# TYPE DEFINITIONS - Callback signatures
# =============================================================================

# Callback when a new device is detected
DeviceAddedCallback = Callable[[DetectedDevice], None]

# Callback when a device is removed
DeviceRemovedCallback = Callable[[str], None]  # device_id

# Callback when device status changes (e.g., unauthorized -> online)
DeviceChangedCallback = Callable[[DetectedDevice], None]


# =============================================================================
# MAIN CLASS - DeviceWatcher
# =============================================================================


class DeviceWatcher:
    """
    Watches for Android device connections/disconnections

    Uses ADB's track-devices command for real-time updates.
    Falls back to polling if track-devices fails.

    Thread Safety:
    - All callbacks are called from the watcher thread
    - Device list access is protected by a lock

    Example:
        >>> watcher = DeviceWatcher()
        >>> watcher.on_device_added = lambda d: print(f"New device: {d.model}")
        >>> watcher.start()
        >>> time.sleep(60)  # Watch for 60 seconds
        >>> watcher.stop()
    """

    # How often to poll for devices (fallback mode)
    POLL_INTERVAL_SECONDS = 2

    # ADB path (can be overridden)
    ADB_PATH = "adb"

    def __init__(self):
        """Initialize the device watcher"""
        # Current known devices
        self._devices: Dict[str, DetectedDevice] = {}
        self._lock = threading.Lock()

        # Watcher state
        self._running = False
        self._watcher_thread: Optional[threading.Thread] = None
        self._adb_process: Optional[subprocess.Popen] = None

        # Callbacks (set these before calling start())
        self.on_device_added: Optional[DeviceAddedCallback] = None
        self.on_device_removed: Optional[DeviceRemovedCallback] = None
        self.on_device_changed: Optional[DeviceChangedCallback] = None

    # =========================================================================
    # PUBLIC PROPERTIES
    # =========================================================================

    @property
    def is_running(self) -> bool:
        """Check if watcher is currently running"""
        return self._running

    @property
    def devices(self) -> List[DetectedDevice]:
        """Get list of currently connected devices"""
        with self._lock:
            return list(self._devices.values())

    def get_device(self, device_id: str) -> Optional[DetectedDevice]:
        """Get a specific device by ID"""
        with self._lock:
            return self._devices.get(device_id)

    def get_online_devices(self) -> List[DetectedDevice]:
        """Get list of online (ready) devices only"""
        with self._lock:
            return [
                d for d in self._devices.values() if d.status == AdbDeviceStatus.ONLINE
            ]

    # =========================================================================
    # PUBLIC METHODS - Lifecycle
    # =========================================================================

    def start(self) -> bool:
        """
        Start watching for device changes

        Returns:
            True if started successfully, False otherwise
        """
        if self._running:
            print("[DeviceWatcher] Already running")
            return True

        # Do initial device scan
        self._do_initial_scan()

        # Start watcher thread
        self._running = True
        self._watcher_thread = threading.Thread(
            target=self._watch_loop, daemon=True, name="device-watcher"
        )
        self._watcher_thread.start()

        print("[DeviceWatcher] Started")
        return True

    def stop(self):
        """Stop watching for device changes"""
        print("[DeviceWatcher] Stopping...")
        self._running = False

        # Kill ADB process if running
        if self._adb_process:
            try:
                self._adb_process.terminate()
                self._adb_process.wait(timeout=2)
            except:
                try:
                    self._adb_process.kill()
                except:
                    pass
            self._adb_process = None

        # Wait for thread to finish
        if self._watcher_thread:
            self._watcher_thread.join(timeout=3)
            self._watcher_thread = None

        print("[DeviceWatcher] Stopped")

    def refresh(self) -> List[DetectedDevice]:
        """
        Force a refresh of the device list

        Returns:
            Current list of devices
        """
        self._do_initial_scan()
        return self.devices

    # =========================================================================
    # PRIVATE METHODS - Initial Scan
    # =========================================================================

    def _do_initial_scan(self):
        """Perform initial device scan using adb devices -l"""
        try:
            result = subprocess.run(
                [self.ADB_PATH, "devices", "-l"],
                capture_output=True,
                text=True,
                timeout=10,
            )

            if result.returncode != 0:
                print(f"[DeviceWatcher] ADB error: {result.stderr}")
                return

            # Parse the output
            new_devices = self._parse_device_list(result.stdout)

            # Update device list and emit events
            self._update_devices(new_devices)

        except FileNotFoundError:
            print(
                "[DeviceWatcher] ADB not found. Please install Android SDK Platform Tools."
            )
        except subprocess.TimeoutExpired:
            print("[DeviceWatcher] ADB command timed out")
        except Exception as e:
            print(f"[DeviceWatcher] Error during scan: {e}")

    def _parse_device_list(self, output: str) -> Dict[str, DetectedDevice]:
        """
        Parse output of 'adb devices -l' command

        Example output:
            List of devices attached
            abc123           device usb:1-1 product:dream2lte model:SM_M205G device:dream2lte transport_id:1
            def456           offline

        Returns:
            Dict mapping device_id to DetectedDevice
        """
        devices = {}

        lines = output.strip().split("\n")

        for line in lines[1:]:  # Skip "List of devices attached"
            line = line.strip()
            if not line:
                continue

            # Split into parts
            parts = line.split()
            if len(parts) < 2:
                continue

            device_id = parts[0]
            status_str = parts[1]

            # Parse status
            status = AdbDeviceStatus.from_adb_string(status_str)

            # Parse additional info (model, product, etc.)
            model = "Unknown"
            product = ""
            transport_id = ""

            for part in parts[2:]:
                if part.startswith("model:"):
                    # model:SM_M205G -> SM-M205G
                    model = part.split(":")[1].replace("_", "-")
                elif part.startswith("product:"):
                    product = part.split(":")[1]
                elif part.startswith("transport_id:"):
                    transport_id = part.split(":")[1]

            devices[device_id] = DetectedDevice(
                device_id=device_id,
                status=status,
                model=model,
                product=product,
                transport_id=transport_id,
            )

        return devices

    # =========================================================================
    # PRIVATE METHODS - Watch Loop
    # =========================================================================

    def _watch_loop(self):
        """
        Main watch loop - tries track-devices, falls back to polling
        """
        # Try track-devices first for real-time updates
        if self._try_track_devices():
            return

        # Fall back to polling
        print("[DeviceWatcher] Falling back to polling mode")
        self._poll_loop()

    def _try_track_devices(self) -> bool:
        """
        Try to use 'adb track-devices' for real-time updates

        Returns:
            True if track-devices is working, False if failed
        """
        try:
            self._adb_process = subprocess.Popen(
                [self.ADB_PATH, "track-devices"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )

            print("[DeviceWatcher] Using track-devices mode")

            while self._running:
                # Read next update from ADB
                # Format: 4-digit hex length + device list
                line = self._adb_process.stdout.readline()

                if not line:
                    # ADB process died
                    print("[DeviceWatcher] ADB track-devices connection lost")
                    break

                # Check if process is still running
                if self._adb_process.poll() is not None:
                    break

                # Parse update and refresh device list
                # track-devices output is simpler, so we do a full scan
                self._do_initial_scan()

            return True

        except FileNotFoundError:
            print("[DeviceWatcher] ADB not found")
            return False
        except Exception as e:
            print(f"[DeviceWatcher] track-devices failed: {e}")
            return False

    def _poll_loop(self):
        """Fallback polling mode - check devices periodically"""
        while self._running:
            self._do_initial_scan()

            # Sleep in small increments for responsiveness
            for _ in range(int(self.POLL_INTERVAL_SECONDS * 10)):
                if not self._running:
                    break
                time.sleep(0.1)

    # =========================================================================
    # PRIVATE METHODS - Device State Management
    # =========================================================================

    def _update_devices(self, new_devices: Dict[str, DetectedDevice]):
        """
        Update internal device list and emit appropriate events

        Args:
            new_devices: Newly scanned device dictionary
        """
        with self._lock:
            old_ids = set(self._devices.keys())
            new_ids = set(new_devices.keys())

            # Find added devices
            added_ids = new_ids - old_ids
            for device_id in added_ids:
                device = new_devices[device_id]
                self._devices[device_id] = device
                print(f"[DeviceWatcher] Device added: {device_id} ({device.model})")

                if self.on_device_added:
                    try:
                        self.on_device_added(device)
                    except Exception as e:
                        print(f"[DeviceWatcher] Callback error: {e}")

            # Find removed devices
            removed_ids = old_ids - new_ids
            for device_id in removed_ids:
                del self._devices[device_id]
                print(f"[DeviceWatcher] Device removed: {device_id}")

                if self.on_device_removed:
                    try:
                        self.on_device_removed(device_id)
                    except Exception as e:
                        print(f"[DeviceWatcher] Callback error: {e}")

            # Find changed devices (status change)
            common_ids = old_ids & new_ids
            for device_id in common_ids:
                old_device = self._devices[device_id]
                new_device = new_devices[device_id]

                if old_device.status != new_device.status:
                    self._devices[device_id] = new_device
                    print(
                        f"[DeviceWatcher] Device changed: {device_id} "
                        f"({old_device.status.name} -> {new_device.status.name})"
                    )

                    if self.on_device_changed:
                        try:
                            self.on_device_changed(new_device)
                        except Exception as e:
                            print(f"[DeviceWatcher] Callback error: {e}")

    def __del__(self):
        """Cleanup on deletion"""
        if self._running:
            self.stop()
