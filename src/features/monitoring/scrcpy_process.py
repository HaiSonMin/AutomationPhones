"""
ScrcpyProcess - Wrapper for scrcpy binary process management

Handles spawning, configuring, and terminating scrcpy processes for individual devices.
Each device gets its own ScrcpyProcess instance.

Example usage:
    process = ScrcpyProcess(device_id="abc123", model="SM-M205G")
    process.start(fps=30, max_size=800)
    process.stop()
"""

import subprocess
import threading
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, List
import shutil
import base64

try:
    from .video_streamer import get_video_streamer
except ImportError:
    # Fallback if video streamer is not available
    def get_video_streamer():
        return None


# =============================================================================
# ENUMS - Device and process status definitions
# =============================================================================


class ProcessStatus(Enum):
    """
    Possible states of a scrcpy process

    STOPPED     - Process not running
    STARTING    - Process is starting up
    RUNNING     - Process is running and streaming
    STOPPING    - Process is shutting down
    ERROR       - Process encountered an error
    """

    STOPPED = "stopped"
    STARTING = "starting"
    RUNNING = "running"
    STOPPING = "stopping"
    ERROR = "error"


# =============================================================================
# DATA CLASSES - Configuration and state containers
# =============================================================================


@dataclass
class ScrcpyConfig:
    """
    Configuration options for scrcpy process

    Attributes:
        fps: Maximum frames per second (1-120, default 30)
        max_size: Maximum dimension in pixels (0=original, 480-2048)
        bitrate: Video bitrate in Mbps (1-100, default 8)
        buffer_ms: Display buffer in milliseconds (0-1000, default 0)
        stay_awake: Keep device screen awake during connection
        turn_screen_off: Turn off device screen (streaming continues)
        show_touches: Show touch indicators on stream
        window_title: Custom window title (None = auto-generate)
        window_x: Initial window X position (None = auto)
        window_y: Initial window Y position (None = auto)
        web_streaming: Stream to web UI instead of window (default False)
    """

    fps: int = 30
    max_size: int = 800
    bitrate: int = 8
    buffer_ms: int = 0
    stay_awake: bool = True
    turn_screen_off: bool = False
    show_touches: bool = False
    window_title: Optional[str] = None
    window_x: Optional[int] = None
    window_y: Optional[int] = None
    web_streaming: bool = False

    def validate(self) -> "ScrcpyConfig":
        """Validate and clamp values to acceptable ranges"""
        self.fps = max(1, min(120, self.fps))
        self.max_size = max(0, min(2048, self.max_size))
        self.bitrate = max(1, min(100, self.bitrate))
        self.buffer_ms = max(0, min(1000, self.buffer_ms))
        return self


# =============================================================================
# MAIN CLASS - ScrcpyProcess
# =============================================================================


class ScrcpyProcess:
    """
    Manages a single scrcpy process for one Android device

    This class handles:
    - Building command line arguments for scrcpy
    - Starting the scrcpy process
    - Monitoring process health
    - Graceful shutdown
    - Error handling and recovery

    Thread Safety:
    - All state modifications are protected by a lock
    - Safe to call from multiple threads

    Example:
        >>> scrcpy = ScrcpyProcess("abc123", "Galaxy S21")
        >>> scrcpy.start(ScrcpyConfig(fps=30, max_size=800))
        >>> scrcpy.is_running()
        True
        >>> scrcpy.stop()
    """

    # Path to scrcpy executable (can be overridden)
    SCRCPY_PATH = "scrcpy"

    # Timeout for graceful shutdown before force kill
    SHUTDOWN_TIMEOUT_SECONDS = 3

    def __init__(self, device_id: str, model: str = "Unknown"):
        """
        Initialize a new ScrcpyProcess

        Args:
            device_id: ADB device serial number (e.g., "abc123" or "192.168.1.1:5555")
            model: Device model name for display (e.g., "SM-M205G")
        """
        # Device identification
        self.device_id = device_id
        self.model = model

        # Process state
        self._process: Optional[subprocess.Popen] = None
        self._status = ProcessStatus.STOPPED
        self._error_message: Optional[str] = None
        self._config: Optional[ScrcpyConfig] = None

        # Thread safety
        self._lock = threading.Lock()

        # Monitoring thread
        self._monitor_thread: Optional[threading.Thread] = None
        self._should_monitor = False

    # =========================================================================
    # PUBLIC PROPERTIES
    # =========================================================================

    @property
    def status(self) -> ProcessStatus:
        """Current process status"""
        with self._lock:
            return self._status

    @property
    def error_message(self) -> Optional[str]:
        """Error message if status is ERROR, None otherwise"""
        with self._lock:
            return self._error_message

    @property
    def pid(self) -> Optional[int]:
        """Process ID if running, None otherwise"""
        with self._lock:
            if self._process and self._process.poll() is None:
                return self._process.pid
            return None

    @property
    def config(self) -> Optional[ScrcpyConfig]:
        """Current configuration"""
        with self._lock:
            return self._config

    def is_running(self) -> bool:
        """Check if scrcpy process is currently running"""
        with self._lock:
            return (
                self._status == ProcessStatus.RUNNING
                and self._process is not None
                and self._process.poll() is None
            )

    # =========================================================================
    # PUBLIC METHODS - Process Control
    # =========================================================================

    def start(self, config: Optional[ScrcpyConfig] = None) -> dict:
        """
        Start the scrcpy process with given configuration

        Args:
            config: ScrcpyConfig instance, or None for defaults

        Returns:
            dict with keys:
                - success: bool
                - pid: int (if successful)
                - error: str (if failed)
        """
        with self._lock:
            # Check if already running
            if self._status == ProcessStatus.RUNNING:
                return {"success": False, "error": "Already running"}

            # Use provided config or defaults
            self._config = (config or ScrcpyConfig()).validate()
            self._status = ProcessStatus.STARTING
            self._error_message = None

            try:
                # First verify scrcpy exists
                scrcpy_path = shutil.which(self.SCRCPY_PATH)
                if not scrcpy_path:
                    raise FileNotFoundError(
                        f"scrcpy not found at '{self.SCRCPY_PATH}'. "
                        "Please install scrcpy and ensure it's in your PATH."
                    )
                print(f"[ScrcpyProcess] Found scrcpy at: {scrcpy_path}")

                # Build command line
                cmd = self._build_command()

                # Log command for debugging
                print(f"[ScrcpyProcess] Starting: {' '.join(cmd)}")

                # Start process
                # CREATE_NO_WINDOW prevents console window on Windows
                creation_flags = 0
                if hasattr(subprocess, "CREATE_NO_WINDOW"):
                    creation_flags = subprocess.CREATE_NO_WINDOW

                self._process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    creationflags=creation_flags,
                )

                print(f"[ScrcpyProcess] Process started with PID: {self._process.pid}")

                # Start video capture thread if in web streaming mode
                if config.web_streaming:
                    self._start_video_capture()

                # Wait for process to start with timeout
                # Use a shorter timeout and non-blocking check
                start_time = time.time()
                timeout = 10.0  # 10 seconds timeout

                while time.time() - start_time < timeout:
                    if self._process.poll() is not None:
                        # Process exited - read error
                        _, stderr = self._process.communicate(timeout=1)
                        error_msg = stderr.decode("utf-8", errors="ignore").strip()
                        if not error_msg:
                            error_msg = (
                                f"Process exited with code {self._process.returncode}"
                            )
                        raise RuntimeError(f"Process exited: {error_msg}")

                    # Check if process is stable (running for at least 1 second)
                    if time.time() - start_time > 1.0:
                        break

                    time.sleep(0.1)

                # Final check - if process still not stable, treat as error
                if self._process.poll() is None:
                    # Process is running
                    self._status = ProcessStatus.RUNNING

                    # Start monitor thread
                    self._start_monitor()

                    print(
                        f"[ScrcpyProcess] Started {self.device_id} (PID: {self._process.pid})"
                    )
                    return {"success": True, "pid": self._process.pid}
                else:
                    raise RuntimeError("Process failed to start within timeout")

            except subprocess.TimeoutExpired:
                # Process is hanging - kill it
                if self._process:
                    self._process.kill()
                    self._process.wait(timeout=5)
                self._status = ProcessStatus.ERROR
                self._error_message = "Process start timed out"
                print(f"[ScrcpyProcess] Start timeout for {self.device_id}")
                return {"success": False, "error": "Process start timed out"}

            except Exception as e:
                self._status = ProcessStatus.ERROR
                self._error_message = str(e)
                print(f"[ScrcpyProcess] Error starting: {self._error_message}")
                return {"success": False, "error": self._error_message}

    def stop(self) -> dict:
        """
        Stop the scrcpy process gracefully

        First attempts SIGTERM, then SIGKILL after timeout.

        Returns:
            dict with keys:
                - success: bool
                - error: str (if failed)
        """
        with self._lock:
            if self._process is None:
                self._status = ProcessStatus.STOPPED
                return {"success": True}

            self._status = ProcessStatus.STOPPING
            self._should_monitor = False

            try:
                # Attempt graceful termination
                print(f"[ScrcpyProcess] Stopping {self.device_id}...")
                self._process.terminate()

                try:
                    # Wait for graceful exit
                    self._process.wait(timeout=self.SHUTDOWN_TIMEOUT_SECONDS)
                except subprocess.TimeoutExpired:
                    # Force kill if graceful failed
                    print(f"[ScrcpyProcess] Force killing {self.device_id}")
                    self._process.kill()
                    self._process.wait(timeout=1)

                self._process = None
                self._status = ProcessStatus.STOPPED
                print(f"[ScrcpyProcess] Stopped {self.device_id}")
                return {"success": True}

            except Exception as e:
                self._status = ProcessStatus.ERROR
                self._error_message = str(e)
                print(f"[ScrcpyProcess] Error stopping: {self._error_message}")
                return {"success": False, "error": self._error_message}

    def restart(self, config: Optional[ScrcpyConfig] = None) -> dict:
        """
        Restart the scrcpy process with optional new configuration

        Args:
            config: New configuration, or None to keep current

        Returns:
            dict from start() method
        """
        # Stop if running
        if self.is_running():
            stop_result = self.stop()
            if not stop_result.get("success"):
                return stop_result

            # Brief pause between stop and start
            time.sleep(0.2)

        # Start with new or existing config
        new_config = config or self._config
        return self.start(new_config)

    def update_fps(self, fps: int) -> dict:
        """
        Update FPS setting (requires restart)

        Args:
            fps: New FPS value (1-120)

        Returns:
            dict from restart() method
        """
        new_config = ScrcpyConfig(
            fps=fps,
            max_size=self._config.max_size if self._config else 800,
            bitrate=self._config.bitrate if self._config else 8,
            stay_awake=self._config.stay_awake if self._config else True,
            turn_screen_off=self._config.turn_screen_off if self._config else False,
        )
        return self.restart(new_config)

    def update_size(self, max_size: int) -> dict:
        """
        Update max size setting (requires restart)

        Args:
            max_size: New max size in pixels (0=original, 480-2048)

        Returns:
            dict from restart() method
        """
        new_config = ScrcpyConfig(
            fps=self._config.fps if self._config else 30,
            max_size=max_size,
            bitrate=self._config.bitrate if self._config else 8,
            stay_awake=self._config.stay_awake if self._config else True,
            turn_screen_off=self._config.turn_screen_off if self._config else False,
        )
        return self.restart(new_config)

    # =========================================================================
    # PUBLIC METHODS - Status and Info
    # =========================================================================

    def get_info(self) -> dict:
        """
        Get complete information about this process

        Returns:
            dict with all relevant process information
        """
        with self._lock:
            return {
                "device_id": self.device_id,
                "model": self.model,
                "status": self._status.value,
                "pid": (
                    self._process.pid
                    if self._process and self._process.poll() is None
                    else None
                ),
                "fps": self._config.fps if self._config else 30,
                "max_size": self._config.max_size if self._config else 800,
                "error": self._error_message,
            }

    # =========================================================================
    # PRIVATE METHODS
    # =========================================================================

    def _build_command(self) -> List[str]:
        """
        Build scrcpy command line arguments

        Returns:
            List of command line arguments
        """
        cmd = [
            self.SCRCPY_PATH,
            "-s",
            self.device_id,  # Target specific device
        ]

        config = self._config

        # Video settings
        cmd.extend(["--max-fps", str(config.fps)])

        if config.max_size > 0:
            cmd.extend(["--max-size", str(config.max_size)])

        cmd.extend(["--video-bit-rate", f"{config.bitrate}M"])

        if config.buffer_ms > 0:
            cmd.extend(["--display-buffer", str(config.buffer_ms)])

        # Behavior settings
        if config.stay_awake:
            cmd.append("--stay-awake")

        if config.turn_screen_off:
            cmd.append("--turn-screen-off")

        if config.show_touches:
            cmd.append("--show-touches")

        # Output settings - web streaming vs window
        if config.web_streaming:
            # Stream to stdout for web consumption
            cmd.extend(
                [
                    "--no-display",  # Don't open a window
                    "--raw-video-stream",  # Output raw video stream
                    "--video-codec",
                    "h264",  # Use H.264 for web compatibility
                ]
            )
        else:
            # Window settings (original behavior)
            title = config.window_title or f"{self.model} ({self.device_id})"
            cmd.extend(["--window-title", title])

            if config.window_x is not None:
                cmd.extend(["--window-x", str(config.window_x)])

            if config.window_y is not None:
                cmd.extend(["--window-y", str(config.window_y)])

        return cmd

    def _start_monitor(self):
        """Start background thread to monitor process health"""
        self._should_monitor = True
        self._monitor_thread = threading.Thread(
            target=self._monitor_process,
            daemon=True,
            name=f"scrcpy-monitor-{self.device_id}",
        )
        self._monitor_thread.start()

    def _start_video_capture(self):
        """Start background thread to capture video frames for web streaming"""
        streamer = get_video_streamer()
        if not streamer:
            print("[ScrcpyProcess] Video streamer not available")
            return

        def capture_video():
            """Capture video frames from scrcpy stdout"""
            try:
                print(f"[ScrcpyProcess] Starting video capture for {self.device_id}")

                # Simple frame buffer - in real implementation, this would need proper H.264 parsing
                frame_buffer = b""

                while self._process and self._process.poll() is None:
                    # Read data from stdout
                    data = self._process.stdout.read(4096)
                    if not data:
                        break

                    frame_buffer += data

                    # For demo purposes, send frames as base64 chunks
                    # In production, you'd want proper H.264 frame parsing
                    if len(frame_buffer) >= 1024:  # Send 1KB chunks
                        # Convert to base64 for JSON transport
                        frame_b64 = base64.b64encode(frame_buffer).decode("utf-8")
                        streamer.add_video_frame(self.device_id, frame_b64)
                        frame_buffer = b""

            except Exception as e:
                print(f"[ScrcpyProcess] Video capture error: {e}")
            finally:
                print(f"[ScrcpyProcess] Video capture ended for {self.device_id}")

        # Start capture thread
        capture_thread = threading.Thread(
            target=capture_video, daemon=True, name=f"scrcpy-capture-{self.device_id}"
        )
        capture_thread.start()

    def _monitor_process(self):
        """
        Background thread that monitors process health
        Updates status if process dies unexpectedly
        """
        while self._should_monitor:
            time.sleep(1)  # Check every second

            with self._lock:
                if not self._should_monitor:
                    break

                if self._process and self._process.poll() is not None:
                    # Process has exited
                    exit_code = self._process.returncode

                    if self._status == ProcessStatus.RUNNING:
                        # Unexpected exit
                        self._status = ProcessStatus.ERROR
                        self._error_message = (
                            f"Process exited unexpectedly (code: {exit_code})"
                        )
                        print(
                            f"[ScrcpyProcess] {self.device_id} crashed: {self._error_message}"
                        )

                    break

        print(f"[ScrcpyProcess] Monitor stopped for {self.device_id}")

    def __del__(self):
        """Cleanup on deletion"""
        self._should_monitor = False
        if self._process:
            try:
                self._process.kill()
            except:
                pass
