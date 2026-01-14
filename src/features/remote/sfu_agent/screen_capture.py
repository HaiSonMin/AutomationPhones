"""
Screen Capture module for WebRTC streaming.

Provides a high-performance screen capture VideoStreamTrack
optimized for low latency streaming.
"""

import asyncio
import logging
import threading
import time
from typing import Optional, Tuple

import cv2
import numpy as np
import mss
from av import VideoFrame
from aiortc import VideoStreamTrack

from .config import QualityProfile

logger = logging.getLogger(__name__)

# Thread-local storage for mss instances
_thread_local = threading.local()


def get_mss():
    """Get thread-local mss instance."""
    if not hasattr(_thread_local, "sct"):
        _thread_local.sct = mss.mss()
    return _thread_local.sct


class ScreenCaptureTrack(VideoStreamTrack):
    """
    WebRTC VideoStreamTrack that captures screen content.

    Optimized for low latency with configurable quality profiles.
    Uses mss for fast screen capture and av for frame encoding.
    """

    kind = "video"

    def __init__(
        self, monitor_index: int = 0, quality: Optional[QualityProfile] = None
    ):
        """
        Initialize screen capture track.

        Args:
            monitor_index: Monitor to capture (0 = primary)
            quality: Quality profile (defaults to low)
        """
        super().__init__()
        self._monitor_index = monitor_index
        self._quality = quality or QualityProfile.low()
        self._frame_count = 0
        self._start_time = time.time()
        self._last_frame_time = 0.0
        self._frame_interval = 1.0 / self._quality.fps
        self._running = True

        # Get initial screen dimensions (in main thread)
        with mss.mss() as sct:
            monitor = sct.monitors[monitor_index + 1]  # 0 is "all monitors"
            self._src_width = monitor["width"]
            self._src_height = monitor["height"]
            self._monitor_dict = dict(monitor)  # Copy monitor dict for thread use

        logger.info(
            f"Screen capture initialized: {self._src_width}x{self._src_height} "
            f"-> {self._quality.width}x{self._quality.height} @ {self._quality.fps}fps"
        )

    def set_quality(self, quality: QualityProfile) -> None:
        """
        Update quality profile.

        Args:
            quality: New quality profile
        """
        self._quality = quality
        self._frame_interval = 1.0 / self._quality.fps
        logger.info(
            f"Quality changed to: {quality.width}x{quality.height} @ {quality.fps}fps"
        )

    def get_screen_size(self) -> Tuple[int, int]:
        """Get the actual screen size being captured."""
        return (self._src_width, self._src_height)

    def _capture_frame(self) -> np.ndarray:
        """Capture and process a single frame (called in thread pool)."""
        # Get thread-local mss instance
        sct = get_mss()

        # Capture screen
        img = sct.grab(self._monitor_dict)
        frame = np.array(img, dtype=np.uint8)

        # Convert BGRA to BGR (remove alpha channel)
        frame = frame[:, :, :3]

        # Resize if needed (for quality scaling)
        if (
            frame.shape[1] != self._quality.width
            or frame.shape[0] != self._quality.height
        ):
            frame = cv2.resize(
                frame,
                (self._quality.width, self._quality.height),
                interpolation=cv2.INTER_LINEAR,  # Fast interpolation
            )

        # Convert BGR to RGB for WebRTC
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        return frame

    async def recv(self) -> VideoFrame:
        """
        Receive the next video frame.

        This method is called by aiortc to get frames for streaming.
        Implements frame rate limiting for consistent FPS.
        """
        if not self._running:
            raise Exception("Track stopped")

        # Frame rate limiting
        current_time = time.time()
        elapsed = current_time - self._last_frame_time
        if elapsed < self._frame_interval:
            await asyncio.sleep(self._frame_interval - elapsed)

        self._last_frame_time = time.time()

        # Capture frame in thread pool to avoid blocking
        loop = asyncio.get_event_loop()
        frame_data = await loop.run_in_executor(None, self._capture_frame)

        # Create VideoFrame
        frame = VideoFrame.from_ndarray(frame_data, format="rgb24")
        frame.pts = self._frame_count
        frame.time_base = self._quality.fps

        self._frame_count += 1

        return frame

    def stop(self) -> None:
        """Stop the screen capture track."""
        self._running = False
        super().stop()
        logger.info("Screen capture track stopped")


class ScreenCaptureManager:
    """
    Manager for screen capture tracks.

    Handles creating and managing capture tracks for multiple viewers
    with different quality requirements.
    """

    def __init__(self, monitor_index: int = 0):
        self._monitor_index = monitor_index
        self._tracks: dict[str, ScreenCaptureTrack] = {}

    def create_track(
        self, viewer_id: str, quality: Optional[QualityProfile] = None
    ) -> ScreenCaptureTrack:
        """
        Create a new capture track for a viewer.

        Args:
            viewer_id: Viewer identifier
            quality: Quality profile for the track

        Returns:
            New ScreenCaptureTrack instance
        """
        track = ScreenCaptureTrack(
            monitor_index=self._monitor_index,
            quality=quality,
        )
        self._tracks[viewer_id] = track
        logger.info(f"Created capture track for viewer: {viewer_id}")
        return track

    def get_track(self, viewer_id: str) -> Optional[ScreenCaptureTrack]:
        """Get existing track for a viewer."""
        return self._tracks.get(viewer_id)

    def remove_track(self, viewer_id: str) -> None:
        """Remove and stop a track for a viewer."""
        if viewer_id in self._tracks:
            self._tracks[viewer_id].stop()
            del self._tracks[viewer_id]
            logger.info(f"Removed capture track for viewer: {viewer_id}")

    def update_quality(self, viewer_id: str, quality: QualityProfile) -> None:
        """Update quality for a viewer's track."""
        if viewer_id in self._tracks:
            self._tracks[viewer_id].set_quality(quality)

    def stop_all(self) -> None:
        """Stop all capture tracks."""
        for track in self._tracks.values():
            track.stop()
        self._tracks.clear()
        logger.info("All capture tracks stopped")
