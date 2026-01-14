"""
Socket.IO Signaling Client for SFU communication.

Handles all signaling events between the agent and SFU server.
"""

import asyncio
import logging
from typing import Callable, Optional, Dict, Any, Awaitable

import socketio

from .config import AgentConfig

logger = logging.getLogger(__name__)


class SignalingClient:
    """
    Socket.IO client for WebRTC signaling.

    Manages connection to SFU server and handles signaling events
    for WebRTC peer connection establishment.
    """

    def __init__(self, config: AgentConfig):
        self.config = config
        self._sio = socketio.AsyncClient(
            reconnection=True,
            reconnection_attempts=0,  # Infinite
            reconnection_delay=config.reconnect_interval,
            logger=False,
            engineio_logger=False,
        )
        self._connected = False
        self._callbacks: Dict[str, Callable[..., Awaitable[None]]] = {}
        self._setup_handlers()

    def _setup_handlers(self) -> None:
        """Setup Socket.IO event handlers."""

        @self._sio.event
        async def connect():
            self._connected = True
            logger.info(f"Connected to SFU server: {self.config.sfu_url}")

        @self._sio.event
        async def disconnect():
            self._connected = False
            logger.info("Disconnected from SFU server")

        @self._sio.event
        async def error(data: Dict[str, Any]):
            logger.error(f"SFU error: {data.get('message', 'Unknown error')}")

        @self._sio.on("create-offer")
        async def on_create_offer(data: Dict[str, Any]):
            await self._invoke_callback("create_offer", data)

        @self._sio.on("answer")
        async def on_answer(data: Dict[str, Any]):
            await self._invoke_callback("answer", data)

        @self._sio.on("ice-candidate")
        async def on_ice_candidate(data: Dict[str, Any]):
            await self._invoke_callback("ice_candidate", data)

        @self._sio.on("change-quality")
        async def on_change_quality(data: Dict[str, Any]):
            await self._invoke_callback("change_quality", data)

        @self._sio.on("mouse-event")
        async def on_mouse_event(data: Dict[str, Any]):
            await self._invoke_callback("mouse_event", data)

        @self._sio.on("keyboard-event")
        async def on_keyboard_event(data: Dict[str, Any]):
            await self._invoke_callback("keyboard_event", data)

    async def _invoke_callback(self, event: str, data: Dict[str, Any]) -> None:
        """Invoke registered callback for an event."""
        if event in self._callbacks:
            try:
                await self._callbacks[event](data)
            except Exception as e:
                logger.error(f"Error in callback for {event}: {e}")

    def on(self, event: str, callback: Callable[..., Awaitable[None]]) -> None:
        """
        Register a callback for a signaling event.

        Args:
            event: Event name (create_offer, answer, ice_candidate, etc.)
            callback: Async callback function
        """
        self._callbacks[event] = callback

    async def connect(self) -> None:
        """Connect to the SFU server."""
        # Pass all params via auth dict for compatibility with SFU server
        auth = {
            "token": self.config.auth_token if self.config.auth_token else "",
            "type": "agent",
            "pcId": self.config.pc_id,
            "pcName": self.config.pc_name,
        }
        if self.config.user_id:
            auth["userId"] = self.config.user_id

        logger.info(
            f"Connecting to SFU: {self.config.sfu_url} as agent (pcId: {self.config.pc_id})"
        )

        try:
            await self._sio.connect(
                self.config.sfu_url,
                auth=auth,
                transports=["websocket"],
                headers={},
                socketio_path="/socket.io",
                wait_timeout=10,
            )
        except Exception as e:
            logger.error(f"Connection failed: {e}")
            raise ConnectionError(f"Failed to connect to SFU server: {e}")

        # Wait for connection
        for _ in range(50):  # 5 seconds timeout
            if self._connected:
                break
            await asyncio.sleep(0.1)

        if not self._connected:
            raise ConnectionError("Connection timeout - server did not respond")

    async def disconnect(self) -> None:
        """Disconnect from the SFU server."""
        if self._sio.connected:
            await self._sio.disconnect()
        self._connected = False

    async def emit_offer(self, viewer_id: str, sdp: Dict[str, Any]) -> None:
        """
        Send SDP offer to a viewer.

        Args:
            viewer_id: Target viewer's socket ID
            sdp: SDP offer object
        """
        await self._sio.emit(
            "offer",
            {
                "viewerId": viewer_id,
                "sdp": sdp,
            },
        )
        logger.debug(f"Sent offer to viewer: {viewer_id}")

    async def emit_ice_candidate(
        self, viewer_id: str, candidate: Dict[str, Any]
    ) -> None:
        """
        Send ICE candidate to a viewer.

        Args:
            viewer_id: Target viewer's socket ID
            candidate: ICE candidate object
        """
        await self._sio.emit(
            "ice-candidate",
            {
                "viewerId": viewer_id,
                "candidate": candidate,
            },
        )

    @property
    def is_connected(self) -> bool:
        """Check if connected to SFU server."""
        return self._connected

    async def wait_until_disconnected(self) -> None:
        """Wait until the client is disconnected."""
        await self._sio.wait()
