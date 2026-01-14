"""
WebRTC Peer Connection management.

Handles creating and managing WebRTC peer connections for streaming
screen content to viewers via the SFU.
"""

import logging
from typing import Optional, Dict, Any, Callable, Awaitable

from aiortc import (
    RTCPeerConnection,
    RTCSessionDescription,
    RTCIceCandidate,
    RTCConfiguration,
    RTCIceServer,
)
from aiortc.contrib.media import MediaRelay

from .config import AgentConfig, QualityProfile
from .screen_capture import ScreenCaptureTrack, ScreenCaptureManager

logger = logging.getLogger(__name__)


class ViewerConnection:
    """Represents a WebRTC connection to a single viewer."""

    def __init__(
        self,
        viewer_id: str,
        pc: RTCPeerConnection,
        track: ScreenCaptureTrack,
    ):
        self.viewer_id = viewer_id
        self.pc = pc
        self.track = track
        self.quality = track._quality

    async def close(self) -> None:
        """Close the peer connection."""
        self.track.stop()
        await self.pc.close()


class WebRTCManager:
    """
    Manages WebRTC peer connections for all viewers.

    Creates peer connections, handles SDP exchange, and manages
    ICE candidates for streaming to multiple viewers.
    """

    def __init__(
        self,
        config: AgentConfig,
        on_ice_candidate: Callable[[str, Dict[str, Any]], Awaitable[None]],
    ):
        """
        Initialize WebRTC manager.

        Args:
            config: Agent configuration
            on_ice_candidate: Callback when ICE candidate is generated
        """
        self._config = config
        self._on_ice_candidate = on_ice_candidate
        self._connections: Dict[str, ViewerConnection] = {}
        self._capture_manager = ScreenCaptureManager(config.capture_monitor)
        self._relay = MediaRelay()

    async def create_offer(
        self,
        viewer_id: str,
        quality: str = "low",
    ) -> Dict[str, Any]:
        """
        Create a WebRTC offer for a viewer.

        Args:
            viewer_id: Viewer's socket ID
            quality: Quality level (low/high)

        Returns:
            SDP offer object
        """
        # Create peer connection with ICE servers
        ice_servers_config = self._config.get_ice_servers()

        # Convert to aiortc RTCIceServer objects
        rtc_ice_servers = []
        for ice_server in ice_servers_config:
            rtc_ice_servers.append(
                RTCIceServer(
                    urls=ice_server["urls"],
                    username=ice_server.get("username"),
                    credential=ice_server.get("credential"),
                )
            )

        # Create RTCConfiguration
        configuration = RTCConfiguration(iceServers=rtc_ice_servers)
        pc = RTCPeerConnection(configuration=configuration)

        # Create capture track with requested quality
        quality_profile = QualityProfile.from_name(quality)
        track = self._capture_manager.create_track(viewer_id, quality_profile)

        # Add track to peer connection
        pc.addTrack(track)

        # Handle ICE candidates
        @pc.on("icecandidate")
        async def on_ice(event):
            if event.candidate:
                candidate_dict = {
                    "candidate": event.candidate.candidate,
                    "sdpMid": event.candidate.sdpMid,
                    "sdpMLineIndex": event.candidate.sdpMLineIndex,
                }
                await self._on_ice_candidate(viewer_id, candidate_dict)

        # Handle connection state changes
        @pc.on("connectionstatechange")
        async def on_state_change():
            logger.info(f"Connection state for {viewer_id}: {pc.connectionState}")
            if pc.connectionState in ["failed", "closed", "disconnected"]:
                await self.close_connection(viewer_id)

        # Store connection
        self._connections[viewer_id] = ViewerConnection(
            viewer_id=viewer_id,
            pc=pc,
            track=track,
        )

        # Create offer
        offer = await pc.createOffer()
        await pc.setLocalDescription(offer)

        logger.info(f"Created offer for viewer: {viewer_id}")

        return {
            "type": offer.type,
            "sdp": offer.sdp,
        }

    async def handle_answer(
        self,
        viewer_id: str,
        sdp: Dict[str, Any],
    ) -> None:
        """
        Handle SDP answer from a viewer.

        Args:
            viewer_id: Viewer's socket ID
            sdp: SDP answer object
        """
        conn = self._connections.get(viewer_id)
        if not conn:
            logger.warning(f"No connection found for viewer: {viewer_id}")
            return

        answer = RTCSessionDescription(
            type=sdp.get("type", "answer"),
            sdp=sdp.get("sdp", ""),
        )
        await conn.pc.setRemoteDescription(answer)
        logger.info(f"Set remote description for viewer: {viewer_id}")

    async def handle_ice_candidate(
        self,
        viewer_id: str,
        candidate: Dict[str, Any],
    ) -> None:
        """
        Handle ICE candidate from a viewer.

        Args:
            viewer_id: Viewer's socket ID
            candidate: ICE candidate object with 'candidate' (SDP string), 'sdpMid', 'sdpMLineIndex'
        """
        conn = self._connections.get(viewer_id)
        if not conn:
            logger.warning(f"No connection found for viewer: {viewer_id}")
            return

        if candidate.get("candidate"):
            try:
                # Parse the SDP candidate string using aiortc's helper
                from aiortc.sdp import candidate_from_sdp

                candidate_str = candidate.get("candidate", "")
                sdp_mid = candidate.get("sdpMid")
                sdp_mline_index = candidate.get("sdpMLineIndex")

                # Parse the candidate string
                ice_candidate = candidate_from_sdp(candidate_str)
                ice_candidate.sdpMid = sdp_mid
                ice_candidate.sdpMLineIndex = sdp_mline_index

                await conn.pc.addIceCandidate(ice_candidate)
            except Exception as e:
                logger.error(f"Error adding ICE candidate: {e}")

    async def change_quality(
        self,
        viewer_id: str,
        quality: str,
        width: Optional[int] = None,
        height: Optional[int] = None,
        fps: Optional[int] = None,
        bitrate: Optional[int] = None,
    ) -> None:
        """
        Change stream quality for a viewer.

        Args:
            viewer_id: Viewer's socket ID
            quality: Quality level (low/high) or custom
            width: Custom width (optional)
            height: Custom height (optional)
            fps: Custom FPS (optional)
            bitrate: Custom bitrate in kbps (optional)
        """
        conn = self._connections.get(viewer_id)
        if not conn:
            logger.warning(f"No connection found for viewer: {viewer_id}")
            return

        # Create quality profile
        if width and height and fps and bitrate:
            profile = QualityProfile(
                name="custom",
                width=width,
                height=height,
                fps=fps,
                bitrate=bitrate,
            )
        else:
            profile = QualityProfile.from_name(quality)

        # Update track quality
        self._capture_manager.update_quality(viewer_id, profile)
        conn.quality = profile
        logger.info(f"Quality changed for {viewer_id}: {profile.name}")

    async def close_connection(self, viewer_id: str) -> None:
        """
        Close connection to a viewer.

        Args:
            viewer_id: Viewer's socket ID
        """
        conn = self._connections.pop(viewer_id, None)
        if conn:
            await conn.close()
            self._capture_manager.remove_track(viewer_id)
            logger.info(f"Closed connection for viewer: {viewer_id}")

    async def close_all(self) -> None:
        """Close all viewer connections."""
        for viewer_id in list(self._connections.keys()):
            await self.close_connection(viewer_id)
        self._capture_manager.stop_all()
        logger.info("All WebRTC connections closed")

    def get_screen_size(self) -> tuple[int, int]:
        """Get the actual screen size being captured."""
        # Create temporary track to get screen size
        temp_track = ScreenCaptureTrack(self._config.capture_monitor)
        size = temp_track.get_screen_size()
        temp_track.stop()
        return size
