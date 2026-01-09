"""
DeviceManager - Central manager for all connected Android devices

Coordinates between DeviceWatcher (detection) and ScrcpyProcess (streaming).
Provides high-level API for device operations.

Architecture:
    DeviceWatcher -> DeviceManager -> ScrcpyProcess(es)
                          |
                          v
                   MonitoringBridge -> React UI

Example usage:
    manager = DeviceManager()
    manager.start()  # Start watching for devices

    # Connect to a device (start streaming)
    manager.connect_device("abc123")

    # Change settings
    manager.set_device_fps("abc123", 30)

    # Cleanup
    manager.stop()
"""

import threading
import time
import sys
from dataclasses import dataclass, field
from typing import Dict, Optional, Callable, List
from enum import Enum

try:
    from .video_streamer import get_video_streamer
except ImportError:
    # Fallback if video streamer is not available
    def get_video_streamer():
        return None


from .device_watcher import DeviceWatcher, DetectedDevice, AdbDeviceStatus
from .scrcpy_process import ScrcpyProcess, ScrcpyConfig, ProcessStatus


# =============================================================================
# ENUMS - Combined device status for UI
# =============================================================================


class DeviceState(Enum):
    """
    Combined state for UI display

    Maps both ADB status and streaming status to a single UI-friendly state
    """

    # ADB states
    DISCONNECTED = "disconnected"  # Not connected via USB
    UNAUTHORIZED = "unauthorized"  # Connected but not authorized
    OFFLINE = "offline"  # Connected but offline

    # Streaming states
    ONLINE = "online"  # Ready to stream (not streaming)
    CONNECTING = "connecting"  # Starting scrcpy
    STREAMING = "streaming"  # Actively streaming
    ERROR = "error"  # Error occurred


# =============================================================================
# DATA CLASSES
# =============================================================================


@dataclass
class ManagedDevice:
    """
    Complete state for a managed device

    Combines ADB info with streaming state
    """

    # From DeviceWatcher
    device_id: str
    model: str = "Unknown"
    adb_status: AdbDeviceStatus = AdbDeviceStatus.UNKNOWN

    # Streaming state
    state: DeviceState = DeviceState.DISCONNECTED
    scrcpy: Optional[ScrcpyProcess] = None

    # Settings
    fps: int = 30
    max_size: int = 800

    # Error info
    error_message: Optional[str] = None

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization"""
        return {
            "device_id": self.device_id,
            "model": self.model,
            "adb_status": self.adb_status.name.lower(),
            "state": self.state.value,
            "fps": self.fps,
            "max_size": self.max_size,
            "is_streaming": self.state == DeviceState.STREAMING,
            "is_online": self.adb_status == AdbDeviceStatus.ONLINE,
            "can_connect": (
                self.adb_status == AdbDeviceStatus.ONLINE
                and self.state not in [DeviceState.STREAMING, DeviceState.CONNECTING]
            ),
            "error": self.error_message,
        }


# =============================================================================
# CALLBACK TYPES
# =============================================================================

# Callback when device list changes
DevicesChangedCallback = Callable[[List[dict]], None]

# Callback for individual device state change
DeviceStateChangedCallback = Callable[[str, str], None]  # device_id, new_state


# =============================================================================
# MAIN CLASS - DeviceManager
# =============================================================================


class DeviceManager:
    """
    Central manager for all Android devices

    Responsibilities:
    - Track all connected devices (via DeviceWatcher)
    - Manage scrcpy processes for streaming
    - Provide high-level API for UI
    - Handle errors and recovery

    Thread Safety:
    - All public methods are thread-safe
    - Callbacks are called from background threads

    Usage:
        >>> manager = DeviceManager()
        >>> manager.on_devices_changed = lambda devices: update_ui(devices)
        >>> manager.start()
        >>> manager.connect_device("abc123")
        >>> manager.set_device_fps("abc123", 60)
        >>> manager.disconnect_device("abc123")
        >>> manager.stop()
    """

    # Default settings for new devices
    DEFAULT_FPS = 30
    DEFAULT_MAX_SIZE = 800

    # Maximum concurrent streaming devices
    MAX_CONCURRENT_STREAMS = 50

    def __init__(self, scrcpy_path: str = "scrcpy"):
        """
        Initialize DeviceManager

        Args:
            scrcpy_path: Path to scrcpy executable
        """
        # Scrcpy configuration
        self._scrcpy_path = scrcpy_path
        ScrcpyProcess.SCRCPY_PATH = scrcpy_path

        # Device tracking
        self._devices: Dict[str, ManagedDevice] = {}
        self._lock = threading.RLock()  # Use RLock to allow reentrant locking

        # Device watcher
        self._watcher = DeviceWatcher()
        self._watcher.on_device_added = self._on_device_added
        self._watcher.on_device_removed = self._on_device_removed
        self._watcher.on_device_changed = self._on_device_changed

        # State
        self._running = False

        # Callbacks for UI
        self.on_devices_changed: Optional[DevicesChangedCallback] = None
        self.on_device_state_changed: Optional[DeviceStateChangedCallback] = None

        print("[DeviceManager] Initialized")

    # =========================================================================
    # PUBLIC PROPERTIES
    # =========================================================================

    @property
    def is_running(self) -> bool:
        """Check if manager is running"""
        return self._running

    @property
    def device_count(self) -> int:
        """Get number of tracked devices"""
        with self._lock:
            return len(self._devices)

    @property
    def streaming_count(self) -> int:
        """Get number of currently streaming devices"""
        with self._lock:
            return sum(
                1 for d in self._devices.values() if d.state == DeviceState.STREAMING
            )

    # =========================================================================
    # PUBLIC METHODS - Lifecycle
    # =========================================================================

    def start(self) -> bool:
        """
        Start the device manager

        Begins watching for devices and processing events.

        Returns:
            True if started successfully
        """
        if self._running:
            print("[DeviceManager] Already running")
            return True

        print("[DeviceManager] Starting...")
        self._running = True

        # Start video streaming server
        streamer = get_video_streamer()
        if streamer:
            streamer.start_server()
            print("[DeviceManager] Video streaming server started")
        else:
            print("[DeviceManager] Video streaming not available")

        # Start device watcher
        self._watcher.start()

        print("[DeviceManager] Started")
        return True

    def stop(self):
        """
        Stop the device manager

        Disconnects all devices and stops watching.
        """
        print("[DeviceManager] Stopping...")
        self._running = False

        # Disconnect all streaming devices
        with self._lock:
            for device in self._devices.values():
                if device.scrcpy:
                    device.scrcpy.stop()

            self._devices.clear()

        # Stop watcher
        self._watcher.stop()

        print("[DeviceManager] Stopped")

    # =========================================================================
    # PUBLIC METHODS - Device List
    # =========================================================================

    def get_all_devices(self) -> List[dict]:
        """
        Get all tracked devices as dictionaries

        Returns:
            List of device dictionaries for UI
        """
        with self._lock:
            return [d.to_dict() for d in self._devices.values()]

    def get_device(self, device_id: str) -> Optional[dict]:
        """
        Get a specific device by ID

        Args:
            device_id: ADB device serial

        Returns:
            Device dictionary or None if not found
        """
        with self._lock:
            device = self._devices.get(device_id)
            return device.to_dict() if device else None

    def refresh_devices(self) -> List[dict]:
        """
        Force refresh the device list

        Returns:
            Updated list of devices
        """
        self._watcher.refresh()
        return self.get_all_devices()

    # =========================================================================
    # PUBLIC METHODS - Device Control
    # =========================================================================

    def connect_device(self, device_id: str) -> dict:
        print(f"\n{'='*50}")
        print(f"[DeviceManager] connect_device called at {time.strftime('%H:%M:%S')}")
        print(f"[DeviceManager] device_id: {device_id}")
        print(f"[DeviceManager] _running: {self._running}")
        print(f"[DeviceManager] device_count: {self.device_count}")
        print(f"[DeviceManager] streaming_count: {self.streaming_count}")
        print(f"{'='*50}\n")

        """
        Start streaming for a device

        Args:
            device_id: ADB device serial

        Returns:
            Result dict with success/error
        """
        with self._lock:
            print(f"[DeviceManager] Acquired lock, looking for device...", flush=True)
            # Get device
            device = self._devices.get(device_id)
            print(f"Device: {device}", flush=True)
            if not device:
                print(f"[DeviceManager] ERROR: Device not found!", flush=True)
                return {"success": False, "error": "Device not found"}

            print(f"[DeviceManager] Device found, checking state...", flush=True)
            print(f"[DeviceManager] device.state = {device.state}", flush=True)
            print(
                f"[DeviceManager] device.state type = {type(device.state)}", flush=True
            )
            print(
                f"[DeviceManager] DeviceState.STREAMING = {DeviceState.STREAMING}",
                flush=True,
            )

            # Check if already streaming
            print(f"[DeviceManager] Checking if already streaming...", flush=True)
            is_streaming = device.state == DeviceState.STREAMING
            print(f"[DeviceManager] is_streaming = {is_streaming}", flush=True)
            if is_streaming:
                print(
                    f"[DeviceManager] ERROR: Already streaming: {device_id}", flush=True
                )
                return {"success": False, "error": "Already streaming"}

            print(f"[DeviceManager] Checking if device is online...", flush=True)
            print(
                f"[DeviceManager] device.adb_status = {device.adb_status}", flush=True
            )
            print(
                f"[DeviceManager] AdbDeviceStatus.ONLINE = {AdbDeviceStatus.ONLINE}",
                flush=True,
            )

            # Check if device is online
            is_online = device.adb_status == AdbDeviceStatus.ONLINE
            print(f"[DeviceManager] is_online = {is_online}", flush=True)
            if not is_online:
                print(
                    f"[DeviceManager] ERROR: Device not online: {device_id} - Status: {device.adb_status}",
                    flush=True,
                )
                return {
                    "success": False,
                    "error": f"Device is {device.adb_status.name}",
                }

            # Check concurrent limit
            if self.streaming_count >= self.MAX_CONCURRENT_STREAMS:
                print(f"[DeviceManager] ERROR: Max concurrent streams reached")
                return {
                    "success": False,
                    "error": f"Max concurrent streams reached ({self.MAX_CONCURRENT_STREAMS})",
                }

            # Update state
            print(f"[DeviceManager] Setting state to CONNECTING for: {device_id}")
            device.state = DeviceState.CONNECTING

            # Capture device info for the background thread
            device_model = device.model
            device_fps = device.fps
            device_max_size = device.max_size

        # Notify UI
        print(f"[DeviceManager] Emitting devices_changed event...")
        self._emit_devices_changed()
        print(f"[DeviceManager] Devices changed event emitted")

        # Create and start scrcpy process in background thread to prevent UI blocking
        print(f"[DeviceManager] Creating background thread for scrcpy...")

        def start_scrcpy_async():
            print(f"\n{'='*50}")
            print(
                f"[DeviceManager] Background thread started at {time.strftime('%H:%M:%S')}"
            )
            print(f"[DeviceManager] Thread name: {threading.current_thread().name}")
            print(f"{'='*50}\n")

            try:
                print(f"[DeviceManager] Starting scrcpy for {device_id}...")

                # Add a timeout event to prevent hanging
                timeout_event = threading.Event()

                def timeout_handler():
                    if not timeout_event.is_set():
                        print(
                            f"[DeviceManager] TIMEOUT! Connection timeout for {device_id}"
                        )
                        with self._lock:
                            device = self._devices.get(device_id)
                            if device and device.state == DeviceState.CONNECTING:
                                device.state = DeviceState.ERROR
                                device.error_message = "Connection timeout (10s)"
                        self._emit_devices_changed()

                # Start timeout timer
                print(f"[DeviceManager] Starting 10-second timeout timer...")
                timer = threading.Timer(10.0, timeout_handler)
                timer.start()

                print(f"[DeviceManager] Creating ScrcpyProcess instance...")
                scrcpy = ScrcpyProcess(device_id, device_model)
                config = ScrcpyConfig(
                    fps=device_fps,
                    max_size=device_max_size,
                    web_streaming=True,  # Enable web streaming mode
                )

                print(f"[DeviceManager] Calling scrcpy.start()...")
                result = scrcpy.start(config)
                print(f"[DeviceManager] scrcpy.start() returned: {result}")

                # Cancel timeout if we got a result
                print(f"[DeviceManager] Cancelling timeout timer...")
                timeout_event.set()
                timer.cancel()

                with self._lock:
                    device = self._devices.get(device_id)
                    if device:
                        if result.get("success"):
                            device.scrcpy = scrcpy
                            device.state = DeviceState.STREAMING
                            device.error_message = None
                            print(f"[DeviceManager] SUCCESS: Connected to {device_id}")
                        else:
                            device.state = DeviceState.ERROR
                            device.error_message = result.get("error")
                            print(
                                f"[DeviceManager] ERROR: Connect failed for {device_id} - {device.error_message}"
                            )

                print(f"[DeviceManager] Emitting final devices_changed event...")
                self._emit_devices_changed()
                print(f"[DeviceManager] Background thread completed successfully")

            except Exception as e:
                print(f"[DeviceManager] EXCEPTION in scrcpy thread: {e}")
                import traceback

                traceback.print_exc()
                with self._lock:
                    device = self._devices.get(device_id)
                    if device:
                        device.state = DeviceState.ERROR
                        device.error_message = str(e)
                self._emit_devices_changed()

            print(f"\n{'='*50}")
            print(
                f"[DeviceManager] Background thread ending at {time.strftime('%H:%M:%S')}"
            )
            print(f"{'='*50}\n")

        # Start in background thread
        print(f"[DeviceManager] Starting background thread...")
        thread = threading.Thread(
            target=start_scrcpy_async, daemon=True, name=f"scrcpy-connect-{device_id}"
        )
        thread.start()
        print(f"[DeviceManager] Background thread started, returning to caller")

        # Return immediately - UI will update via events
        print(f"\n{'='*50}")
        print(
            f"[DeviceManager] Returning to caller with: {{'success': True, 'message': 'Connecting...'}}"
        )
        print(
            f"[DeviceManager] The background thread will continue working independently"
        )
        print(f"{'='*50}\n")
        return {"success": True, "message": "Connecting..."}

    def disconnect_device(self, device_id: str) -> dict:
        """
        Stop streaming for a device

        Args:
            device_id: ADB device serial

        Returns:
            Result dict with success/error
        """
        with self._lock:
            device = self._devices.get(device_id)
            if not device:
                return {"success": False, "error": "Device not found"}

            if not device.scrcpy:
                device.state = (
                    DeviceState.ONLINE
                    if device.adb_status == AdbDeviceStatus.ONLINE
                    else DeviceState.DISCONNECTED
                )
                return {"success": True}

            # Stop scrcpy
            result = device.scrcpy.stop()

            device.scrcpy = None
            device.state = (
                DeviceState.ONLINE
                if device.adb_status == AdbDeviceStatus.ONLINE
                else DeviceState.DISCONNECTED
            )
            device.error_message = None

            print(f"[DeviceManager] Disconnected: {device_id}")

        self._emit_devices_changed()
        return {"success": True}

    def disconnect_all(self) -> dict:
        """
        Disconnect all streaming devices

        Returns:
            Result dict
        """
        with self._lock:
            device_ids = list(self._devices.keys())

        for device_id in device_ids:
            self.disconnect_device(device_id)

        return {"success": True, "count": len(device_ids)}

    # =========================================================================
    # PUBLIC METHODS - Settings
    # =========================================================================

    def set_device_fps(self, device_id: str, fps: int) -> dict:
        """
        Change FPS for a device

        If currently streaming, restarts the stream with new FPS.

        Args:
            device_id: ADB device serial
            fps: New FPS value (1-120)

        Returns:
            Result dict
        """
        # Validate FPS
        fps = max(1, min(120, fps))

        with self._lock:
            device = self._devices.get(device_id)
            if not device:
                return {"success": False, "error": "Device not found"}

            device.fps = fps

            # If streaming, restart with new FPS
            if device.scrcpy and device.state == DeviceState.STREAMING:
                result = device.scrcpy.update_fps(fps)
                if not result.get("success"):
                    return result

        self._emit_devices_changed()
        return {"success": True, "fps": fps}

    def set_device_size(self, device_id: str, max_size: int) -> dict:
        """
        Change max size for a device

        If currently streaming, restarts the stream with new size.

        Args:
            device_id: ADB device serial
            max_size: New max size (0=original, 480-2048)

        Returns:
            Result dict
        """
        # Validate size
        max_size = max(0, min(2048, max_size))

        with self._lock:
            device = self._devices.get(device_id)
            if not device:
                return {"success": False, "error": "Device not found"}

            device.max_size = max_size

            # If streaming, restart with new size
            if device.scrcpy and device.state == DeviceState.STREAMING:
                result = device.scrcpy.update_size(max_size)
                if not result.get("success"):
                    return result

        self._emit_devices_changed()
        return {"success": True, "max_size": max_size}

    def set_device_settings(
        self, device_id: str, fps: int = None, max_size: int = None
    ) -> dict:
        """
        Update multiple settings at once

        Args:
            device_id: ADB device serial
            fps: New FPS (optional)
            max_size: New max size (optional)

        Returns:
            Result dict
        """
        with self._lock:
            device = self._devices.get(device_id)
            if not device:
                return {"success": False, "error": "Device not found"}

            # Update settings
            if fps is not None:
                device.fps = max(1, min(120, fps))
            if max_size is not None:
                device.max_size = max(0, min(2048, max_size))

            # If streaming, restart with new settings
            if device.scrcpy and device.state == DeviceState.STREAMING:
                config = ScrcpyConfig(
                    fps=device.fps,
                    max_size=device.max_size,
                )
                result = device.scrcpy.restart(config)
                if not result.get("success"):
                    return result

        self._emit_devices_changed()
        return {"success": True, "fps": device.fps, "max_size": device.max_size}

    # =========================================================================
    # PRIVATE METHODS - Device Watcher Callbacks
    # =========================================================================

    def _on_device_added(self, detected: DetectedDevice):
        """Handle new device detected by watcher"""
        with self._lock:
            # Create managed device
            device = ManagedDevice(
                device_id=detected.device_id,
                model=detected.model,
                adb_status=detected.status,
                state=self._map_adb_status_to_state(detected.status),
                fps=self.DEFAULT_FPS,
                max_size=self.DEFAULT_MAX_SIZE,
            )

            self._devices[detected.device_id] = device
            print(
                f"[DeviceManager] Device added: {detected.device_id} ({detected.model})"
            )

        self._emit_devices_changed()

    def _on_device_removed(self, device_id: str):
        """Handle device removed detected by watcher"""
        with self._lock:
            device = self._devices.get(device_id)
            if device:
                # Stop streaming if active
                if device.scrcpy:
                    device.scrcpy.stop()

                del self._devices[device_id]
                print(f"[DeviceManager] Device removed: {device_id}")

        self._emit_devices_changed()

    def _on_device_changed(self, detected: DetectedDevice):
        """Handle device status change detected by watcher"""
        with self._lock:
            device = self._devices.get(detected.device_id)
            if device:
                old_status = device.adb_status
                device.adb_status = detected.status
                device.model = detected.model

                # Update state based on new ADB status
                if detected.status != AdbDeviceStatus.ONLINE:
                    # Device went offline - stop streaming
                    if device.scrcpy:
                        device.scrcpy.stop()
                        device.scrcpy = None

                    device.state = self._map_adb_status_to_state(detected.status)
                elif (
                    device.state == DeviceState.DISCONNECTED
                    or device.state == DeviceState.UNAUTHORIZED
                ):
                    # Device came online
                    device.state = DeviceState.ONLINE

                print(
                    f"[DeviceManager] Device changed: {detected.device_id} "
                    f"({old_status.name} -> {detected.status.name})"
                )

        self._emit_devices_changed()

    # =========================================================================
    # PRIVATE METHODS - Helpers
    # =========================================================================

    def _map_adb_status_to_state(self, adb_status: AdbDeviceStatus) -> DeviceState:
        """Map ADB status to device state"""
        mapping = {
            AdbDeviceStatus.ONLINE: DeviceState.ONLINE,
            AdbDeviceStatus.OFFLINE: DeviceState.OFFLINE,
            AdbDeviceStatus.UNAUTHORIZED: DeviceState.UNAUTHORIZED,
            AdbDeviceStatus.BOOTLOADER: DeviceState.OFFLINE,
            AdbDeviceStatus.RECOVERY: DeviceState.OFFLINE,
            AdbDeviceStatus.UNKNOWN: DeviceState.DISCONNECTED,
        }
        return mapping.get(adb_status, DeviceState.DISCONNECTED)

    def _emit_devices_changed(self):
        """Emit devices changed event to UI"""
        if self.on_devices_changed:
            try:
                devices = self.get_all_devices()
                self.on_devices_changed(devices)
            except Exception as e:
                print(f"[DeviceManager] Callback error: {e}")

    def __del__(self):
        """Cleanup on deletion"""
        if self._running:
            self.stop()


# =============================================================================
# SINGLETON INSTANCE
# =============================================================================

# Global instance for use by bridge
_manager_instance: Optional[DeviceManager] = None


def get_device_manager() -> DeviceManager:
    """
    Get the global DeviceManager instance

    Creates one if it doesn't exist.
    """
    global _manager_instance
    if _manager_instance is None:
        _manager_instance = DeviceManager()
    return _manager_instance


def cleanup_device_manager():
    """Cleanup the global DeviceManager instance"""
    global _manager_instance
    if _manager_instance:
        _manager_instance.stop()
        _manager_instance = None
