"""
Main SFU Agent class.

Orchestrates all components (signaling, WebRTC, screen capture, input)
to provide a complete remote PC streaming solution.
"""

import asyncio
import logging
import signal
from typing import Optional, Dict, Any

from .config import AgentConfig, QualityProfile
from .signaling import SignalingClient
from .webrtc import WebRTCManager
from .input_handler import InputHandler

logger = logging.getLogger(__name__)


class SFUAgent:
    """
    Main agent class for remote PC streaming.

    Connects to an SFU server and streams screen content while
    handling remote input events. Designed as a reusable module
    that can be integrated into various applications.

    Usage:
        from src.features.remote.sfu_agent import SFUAgent, AgentConfig

        config = AgentConfig(
            sfu_url="https://your-sfu.com",
            pc_id="unique-id",
            pc_name="My PC"
        )

        agent = SFUAgent(config)
        await agent.start()
    """

    def __init__(self, config: AgentConfig):
        """
        Initialize the SFU Agent.

        Args:
            config: Agent configuration
        """
        self._config = config
        self._running = False
        self._signaling: Optional[SignalingClient] = None
        self._webrtc: Optional[WebRTCManager] = None
        self._input_handler: Optional[InputHandler] = None

        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        )

    async def start(self) -> None:
        """
        Start the agent and connect to SFU.

        This method blocks until the agent is stopped or disconnected.
        """
        if self._running:
            logger.warning("Agent is already running")
            return

        self._running = True
        logger.info(
            f"Starting SFU Agent: {self._config.pc_name} ({self._config.pc_id})"
        )

        try:
            # Initialize signaling client
            self._signaling = SignalingClient(self._config)

            # Initialize WebRTC manager
            self._webrtc = WebRTCManager(
                config=self._config,
                on_ice_candidate=self._on_ice_candidate,
            )

            # Initialize input handler
            screen_size = self._webrtc.get_screen_size()
            quality = self._config.get_quality_profile()
            self._input_handler = InputHandler(
                screen_size=screen_size,
                stream_size=(quality.width, quality.height),
                enabled=self._config.enable_input,
            )

            # Register signaling event handlers
            self._setup_signaling_handlers()

            # Connect to SFU
            await self._signaling.connect()
            logger.info("Connected to SFU server successfully")

            # Setup signal handlers for graceful shutdown
            self._setup_signal_handlers()

            # Wait until disconnected
            await self._signaling.wait_until_disconnected()

        except asyncio.CancelledError:
            logger.info("Agent cancelled")
        except Exception as e:
            logger.error(f"Agent error: {e}")
            raise
        finally:
            await self.stop()

    async def stop(self) -> None:
        """Stop the agent and cleanup resources."""
        if not self._running:
            return

        self._running = False
        logger.info("Stopping SFU Agent...")

        # Release all pressed keys
        if self._input_handler:
            self._input_handler.release_all_keys()

        # Close all WebRTC connections
        if self._webrtc:
            await self._webrtc.close_all()

        # Disconnect from SFU
        if self._signaling:
            await self._signaling.disconnect()

        logger.info("SFU Agent stopped")

    def _setup_signaling_handlers(self) -> None:
        """Setup handlers for signaling events."""
        if not self._signaling:
            return

        self._signaling.on("create_offer", self._on_create_offer)
        self._signaling.on("answer", self._on_answer)
        self._signaling.on("ice_candidate", self._on_remote_ice_candidate)
        self._signaling.on("change_quality", self._on_change_quality)
        self._signaling.on("mouse_event", self._on_mouse_event)
        self._signaling.on("keyboard_event", self._on_keyboard_event)

    def _setup_signal_handlers(self) -> None:
        """Setup OS signal handlers for graceful shutdown."""
        loop = asyncio.get_event_loop()

        for sig in (signal.SIGINT, signal.SIGTERM):
            try:
                loop.add_signal_handler(
                    sig,
                    lambda: asyncio.create_task(self.stop()),
                )
            except NotImplementedError:
                # Windows doesn't support add_signal_handler
                pass

    async def _on_create_offer(self, data: Dict[str, Any]) -> None:
        """Handle create-offer request from viewer."""
        viewer_id = data.get("viewerId")
        quality = data.get("quality", "low")

        if not viewer_id or not self._webrtc or not self._signaling:
            return

        logger.info(f"Creating offer for viewer: {viewer_id} (quality: {quality})")

        try:
            # Create WebRTC offer
            sdp = await self._webrtc.create_offer(viewer_id, quality)

            # Send offer to viewer via signaling
            await self._signaling.emit_offer(viewer_id, sdp)

        except Exception as e:
            logger.error(f"Error creating offer: {e}")

    async def _on_answer(self, data: Dict[str, Any]) -> None:
        """Handle SDP answer from viewer."""
        viewer_id = data.get("viewerId")
        sdp = data.get("sdp")

        if not viewer_id or not sdp or not self._webrtc:
            return

        logger.debug(f"Received answer from viewer: {viewer_id}")
        await self._webrtc.handle_answer(viewer_id, sdp)

    async def _on_remote_ice_candidate(self, data: Dict[str, Any]) -> None:
        """Handle ICE candidate from viewer."""
        viewer_id = data.get("viewerId")
        candidate = data.get("candidate")

        if not viewer_id or not candidate or not self._webrtc:
            return

        await self._webrtc.handle_ice_candidate(viewer_id, candidate)

    async def _on_ice_candidate(
        self,
        viewer_id: str,
        candidate: Dict[str, Any],
    ) -> None:
        """Callback when local ICE candidate is generated."""
        if self._signaling:
            await self._signaling.emit_ice_candidate(viewer_id, candidate)

    async def _on_change_quality(self, data: Dict[str, Any]) -> None:
        """Handle quality change request."""
        viewer_id = data.get("viewerId")
        quality = data.get("quality", "low")
        width = data.get("width")
        height = data.get("height")
        fps = data.get("frameRate")
        bitrate = data.get("bitrate")

        if not viewer_id or not self._webrtc:
            return

        logger.info(f"Quality change for {viewer_id}: {quality}")

        await self._webrtc.change_quality(
            viewer_id=viewer_id,
            quality=quality,
            width=width,
            height=height,
            fps=fps,
            bitrate=bitrate,
        )

        # Update input handler stream size
        if self._input_handler:
            profile = QualityProfile.from_name(quality)
            if width and height:
                self._input_handler.set_stream_size(width, height)
            else:
                self._input_handler.set_stream_size(profile.width, profile.height)

    async def _on_mouse_event(self, data: Dict[str, Any]) -> None:
        """Handle mouse event from viewer."""
        if not self._input_handler:
            return

        self._input_handler.handle_mouse_event(
            event_type=data.get("type", ""),
            x=data.get("x", 0),
            y=data.get("y", 0),
            button=data.get("button", 0),
            delta_x=data.get("deltaX", 0),
            delta_y=data.get("deltaY", 0),
        )

    async def _on_keyboard_event(self, data: Dict[str, Any]) -> None:
        """Handle keyboard event from viewer."""
        if not self._input_handler:
            return

        self._input_handler.handle_keyboard_event(
            event_type=data.get("type", ""),
            key=data.get("key", ""),
            code=data.get("code", ""),
            modifiers=data.get("modifiers"),
        )

    @property
    def is_running(self) -> bool:
        """Check if agent is running."""
        return self._running

    @property
    def is_connected(self) -> bool:
        """Check if connected to SFU."""
        return self._signaling.is_connected if self._signaling else False
