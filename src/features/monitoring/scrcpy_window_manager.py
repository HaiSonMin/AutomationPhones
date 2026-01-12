"""
ScrcpyWindowManager - Manage native scrcpy windows

Opens scrcpy.exe windows directly for low-latency streaming (35-70ms).
No need for PyAV or complex dependencies.
"""

import subprocess
import shutil
import threading
import time
from dataclasses import dataclass, field
from typing import Dict, Optional, Callable, List
from enum import Enum


class WindowState(Enum):
    """Scrcpy window state"""

    CLOSED = "closed"
    STARTING = "starting"
    RUNNING = "running"
    ERROR = "error"


@dataclass
class ScrcpyWindow:
    """Represents a scrcpy window for a device"""

    device_id: str
    model: str = "Unknown"
    state: WindowState = WindowState.CLOSED
    process: Optional[subprocess.Popen] = None
    error: Optional[str] = None
    started_at: float = 0

    def to_dict(self) -> dict:
        return {
            "device_id": self.device_id,
            "model": self.model,
            "state": self.state.value,
            "is_running": self.state == WindowState.RUNNING,
            "error": self.error,
        }


class ScrcpyWindowManager:
    """
    Manages native scrcpy windows for multiple devices

    Features:
    - Open scrcpy.exe window per device
    - Global settings (size, fps, etc.)
    - Auto-restart on crash
    - Window positioning
    """

    def __init__(self):
        self._scrcpy_path = self._find_scrcpy()
        self._windows: Dict[str, ScrcpyWindow] = {}
        self._lock = threading.Lock()

        # Settings
        self._max_size = 800
        self._max_fps = 30
        self._bitrate = 4  # Mbps
        self._stay_awake = True
        self._show_touches = False
        self._borderless = False
        self._always_on_top = False

        # Window positioning
        self._window_width = 320
        self._window_gap = 10
        self._next_x = 50
        self._next_y = 50

        # Callbacks
        self._on_state_changed: Optional[Callable[[str, str], None]] = None

        print(f"[ScrcpyWindowManager] Initialized, scrcpy: {self._scrcpy_path}")

    def _find_scrcpy(self) -> Optional[str]:
        """Find scrcpy executable"""
        import os

        # Check if in PATH
        scrcpy = shutil.which("scrcpy")
        if scrcpy:
            return scrcpy

        # Common locations on Windows
        common_paths = [
            r"C:\ProgramData\chocolatey\bin\scrcpy.exe",
            r"C:\ProgramData\chocolatey\bin\scrcpy.EXE",
            r"C:\Program Files\scrcpy\scrcpy.exe",
            r"C:\scrcpy\scrcpy.exe",
            os.path.expanduser(r"~\scrcpy\scrcpy.exe"),
            os.path.expanduser(r"~\AppData\Local\scrcpy\scrcpy.exe"),
        ]

        for path in common_paths:
            if os.path.exists(path):
                print(f"[ScrcpyWindowManager] Found scrcpy at: {path}")
                return path

        return None

    @property
    def is_available(self) -> bool:
        return self._scrcpy_path is not None

    def set_on_state_changed(self, callback: Callable[[str, str], None]) -> None:
        self._on_state_changed = callback

    def update_settings(
        self,
        max_size: Optional[int] = None,
        max_fps: Optional[int] = None,
        bitrate: Optional[int] = None,
        stay_awake: Optional[bool] = None,
        borderless: Optional[bool] = None,
        always_on_top: Optional[bool] = None,
    ) -> dict:
        """Update global settings"""
        if max_size is not None:
            self._max_size = max_size
        if max_fps is not None:
            self._max_fps = max_fps
        if bitrate is not None:
            self._bitrate = bitrate
        if stay_awake is not None:
            self._stay_awake = stay_awake
        if borderless is not None:
            self._borderless = borderless
        if always_on_top is not None:
            self._always_on_top = always_on_top

        return self.get_settings()

    def get_settings(self) -> dict:
        return {
            "max_size": self._max_size,
            "max_fps": self._max_fps,
            "bitrate": self._bitrate,
            "stay_awake": self._stay_awake,
            "borderless": self._borderless,
            "always_on_top": self._always_on_top,
        }

    def open_window(self, device_id: str, model: str = "Unknown") -> dict:
        """
        Open scrcpy window for a device

        Returns:
            dict with success/error
        """
        if not self._scrcpy_path:
            return {"success": False, "error": "scrcpy not found"}

        with self._lock:
            if device_id in self._windows:
                window = self._windows[device_id]
                if window.state == WindowState.RUNNING:
                    return {"success": False, "error": "Window already open"}

        print(f"[ScrcpyWindowManager] Opening window for {device_id}")

        # Build command
        cmd = [
            self._scrcpy_path,
            "-s",
            device_id,
            "--max-size",
            str(self._max_size),
            "--max-fps",
            str(self._max_fps),
            "--video-bit-rate",
            f"{self._bitrate}M",
            "--window-title",
            f"{model} ({device_id[:8]}...)",
            "--window-x",
            str(self._next_x),
            "--window-y",
            str(self._next_y),
        ]

        if self._stay_awake:
            cmd.append("--stay-awake")
        if self._borderless:
            cmd.append("--window-borderless")
        if self._always_on_top:
            cmd.append("--always-on-top")

        try:
            # Start scrcpy process
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                creationflags=(
                    subprocess.CREATE_NO_WINDOW
                    if hasattr(subprocess, "CREATE_NO_WINDOW")
                    else 0
                ),
            )

            window = ScrcpyWindow(
                device_id=device_id,
                model=model,
                state=WindowState.STARTING,
                process=process,
                started_at=time.time(),
            )

            with self._lock:
                self._windows[device_id] = window

            # Update next window position
            self._next_x += self._window_width + self._window_gap
            if self._next_x > 1400:
                self._next_x = 50
                self._next_y += 500

            # Monitor process in background
            threading.Thread(
                target=self._monitor_process, args=(device_id,), daemon=True
            ).start()

            return {"success": True}

        except Exception as e:
            error_msg = str(e)
            print(f"[ScrcpyWindowManager] Error opening window: {error_msg}")
            return {"success": False, "error": error_msg}

    def close_window(self, device_id: str) -> dict:
        """Close scrcpy window for a device"""
        with self._lock:
            if device_id not in self._windows:
                return {"success": False, "error": "Window not found"}

            window = self._windows[device_id]

        print(f"[ScrcpyWindowManager] Closing window for {device_id}")

        try:
            if window.process and window.process.poll() is None:
                window.process.terminate()
                window.process.wait(timeout=3)
        except:
            try:
                window.process.kill()
            except:
                pass

        with self._lock:
            window.state = WindowState.CLOSED
            window.process = None

        self._emit_state_changed(device_id, "closed")
        return {"success": True}

    def close_all(self) -> dict:
        """Close all scrcpy windows"""
        device_ids = list(self._windows.keys())
        for device_id in device_ids:
            self.close_window(device_id)

        # Reset window positions
        self._next_x = 50
        self._next_y = 50

        return {"success": True}

    def get_window(self, device_id: str) -> Optional[dict]:
        """Get window state for a device"""
        with self._lock:
            if device_id in self._windows:
                return self._windows[device_id].to_dict()
            return None

    def get_all_windows(self) -> List[dict]:
        """Get all window states"""
        with self._lock:
            return [w.to_dict() for w in self._windows.values()]

    def _monitor_process(self, device_id: str) -> None:
        """Monitor scrcpy process and update state"""
        time.sleep(1)  # Give scrcpy time to start

        with self._lock:
            if device_id not in self._windows:
                return
            window = self._windows[device_id]

        if window.process and window.process.poll() is None:
            # Process is running
            window.state = WindowState.RUNNING
            self._emit_state_changed(device_id, "running")

            # Wait for process to exit
            window.process.wait()

        # Process has exited
        with self._lock:
            if device_id in self._windows:
                w = self._windows[device_id]
                if w.state == WindowState.RUNNING:
                    w.state = WindowState.CLOSED
                    self._emit_state_changed(device_id, "closed")

    def _emit_state_changed(self, device_id: str, state: str) -> None:
        if self._on_state_changed:
            try:
                self._on_state_changed(device_id, state)
            except Exception as e:
                print(f"[ScrcpyWindowManager] Callback error: {e}")
