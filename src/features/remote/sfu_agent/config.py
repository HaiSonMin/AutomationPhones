"""
Configuration module for SFU Agent.

Contains dataclasses for agent configuration and quality profiles.
"""

from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any


@dataclass
class ICEServer:
    """STUN/TURN server configuration."""

    urls: List[str]
    username: Optional[str] = None
    credential: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for aiortc."""
        result = {"urls": self.urls}
        if self.username:
            result["username"] = self.username
        if self.credential:
            result["credential"] = self.credential
        return result


@dataclass
class QualityProfile:
    """Video quality profile settings."""

    name: str
    width: int
    height: int
    fps: int
    bitrate: int  # kbps

    @classmethod
    def low(cls) -> "QualityProfile":
        """Low quality for grid view - optimized for multiple streams."""
        return cls(name="low", width=854, height=480, fps=5, bitrate=500)

    @classmethod
    def high(cls) -> "QualityProfile":
        """High quality for focused view - full HD."""
        return cls(name="high", width=1920, height=1080, fps=30, bitrate=3000)

    @classmethod
    def from_name(cls, name: str) -> "QualityProfile":
        """Get profile by name."""
        if name == "high":
            return cls.high()
        return cls.low()


@dataclass
class AgentConfig:
    """
    Main configuration for SFU Agent.

    Attributes:
        sfu_url: WebSocket URL of the SFU server
        pc_id: Unique identifier for this PC
        pc_name: Friendly display name for this PC
        auth_token: Optional authentication token
        user_id: Optional user ID for authentication
        ice_servers: List of STUN/TURN servers
        initial_quality: Initial stream quality (low/high)
        reconnect_interval: Seconds between reconnection attempts
        capture_monitor: Monitor index to capture (0 = primary)
    """

    sfu_url: str
    pc_id: str
    pc_name: str = "Remote PC"
    auth_token: Optional[str] = None
    user_id: Optional[str] = None
    ice_servers: List[ICEServer] = field(
        default_factory=lambda: [
            ICEServer(urls=["stun:stun.l.google.com:19302"]),
            ICEServer(urls=["stun:stun1.l.google.com:19302"]),
            # Free TURN server for development (OpenRelay)
            ICEServer(
                urls=["turn:openrelay.metered.ca:80"],
                username="openrelayproject",
                credential="openrelayproject",
            ),
            ICEServer(
                urls=["turn:openrelay.metered.ca:443"],
                username="openrelayproject",
                credential="openrelayproject",
            ),
        ]
    )
    initial_quality: str = "low"
    reconnect_interval: float = 5.0
    capture_monitor: int = 0
    enable_input: bool = True

    def get_ice_servers(self) -> List[Dict[str, Any]]:
        """Get ICE servers as list of dictionaries."""
        return [server.to_dict() for server in self.ice_servers]

    def get_quality_profile(self) -> QualityProfile:
        """Get the initial quality profile."""
        return QualityProfile.from_name(self.initial_quality)
