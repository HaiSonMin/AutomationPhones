"""
VideoStreamer - Handles streaming scrcpy video to web clients

Captures video output from scrcpy processes and serves it via WebSocket
to the React frontend for display.
"""

import asyncio
import threading
import queue
import time
from typing import Dict, Optional
import websockets
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class VideoStreamer:
    """
    Manages video streaming from scrcpy to web clients

    Each device has its own video stream that can be viewed by multiple clients.
    """

    def __init__(self):
        self._streams: Dict[str, queue.Queue] = {}
        self._clients: Dict[str, set] = {}  # device_id -> set of websockets
        self._server = None
        self._server_thread = None
        self._running = False

    async def register_client(self, websocket, device_id: str):
        """
        Register a new client for a device's video stream

        Args:
            websocket: WebSocket connection to the client
            device_id: ID of the device to stream
        """
        if device_id not in self._clients:
            self._clients[device_id] = set()

        self._clients[device_id].add(websocket)
        logger.info(f"Client registered for device {device_id}")

        try:
            # Send initial connection success message
            await websocket.send(
                json.dumps({"type": "connected", "device_id": device_id})
            )

            # Keep connection alive and send video frames
            while websocket in self._clients.get(device_id, set()):
                if device_id in self._streams:
                    try:
                        # Get frame from queue with timeout
                        frame = self._streams[device_id].get(timeout=1.0)

                        # Send frame to client
                        await websocket.send(
                            json.dumps(
                                {
                                    "type": "video_frame",
                                    "device_id": device_id,
                                    "data": frame,
                                }
                            )
                        )
                    except queue.Empty:
                        # Send keepalive
                        await websocket.ping()
                else:
                    await asyncio.sleep(0.1)

        except websockets.exceptions.ConnectionClosed:
            logger.info(f"Client disconnected from device {device_id}")
        finally:
            # Clean up
            if device_id in self._clients:
                self._clients[device_id].discard(websocket)

    def add_video_frame(self, device_id: str, frame_data: bytes):
        """
        Add a video frame to the stream queue

        Args:
            device_id: ID of the device
            frame_data: Raw video frame data
        """
        if device_id not in self._streams:
            self._streams[device_id] = queue.Queue(maxsize=30)  # Buffer 30 frames

        try:
            self._streams[device_id].put_nowait(frame_data)
        except queue.Full:
            # Drop frame if buffer is full
            pass

    def remove_device_stream(self, device_id: str):
        """
        Remove a device's video stream

        Args:
            device_id: ID of the device to remove
        """
        if device_id in self._streams:
            del self._streams[device_id]

        if device_id in self._clients:
            # Notify all clients that stream is ending
            for client in self._clients[device_id]:
                try:
                    asyncio.create_task(
                        client.send(
                            json.dumps({"type": "stream_ended", "device_id": device_id})
                        )
                    )
                except:
                    pass
            del self._clients[device_id]

    async def _handle_client(self, websocket, path):
        """
        Handle new WebSocket connection

        Expected message format:
        {
            "type": "subscribe",
            "device_id": "abc123"
        }
        """
        try:
            async for message in websocket:
                data = json.loads(message)

                if data.get("type") == "subscribe":
                    device_id = data.get("device_id")
                    if device_id:
                        await self.register_client(websocket, device_id)
                        break

        except json.JSONDecodeError:
            logger.error("Invalid JSON received from client")
        except Exception as e:
            logger.error(f"Error handling client: {e}")

    def start_server(self, port: int = 8765):
        """
        Start the WebSocket server

        Args:
            port: Port to listen on
        """
        if self._running:
            return

        self._running = True

        def run_server():
            asyncio.set_event_loop(asyncio.new_event_loop())

            start_server = websockets.serve(self._handle_client, "localhost", port)

            logger.info(f"Video streaming server started on ws://localhost:{port}")

            asyncio.get_event_loop().run_until_complete(start_server)
            asyncio.get_event_loop().run_forever()

        self._server_thread = threading.Thread(target=run_server, daemon=True)
        self._server_thread.start()

    def stop(self):
        """Stop the streaming server"""
        self._running = False
        if self._server:
            self._server.close()
        self._streams.clear()
        self._clients.clear()


# Global instance
_streamer: Optional[VideoStreamer] = None


def get_video_streamer() -> VideoStreamer:
    """Get the global video streamer instance"""
    global _streamer
    if _streamer is None:
        _streamer = VideoStreamer()
    return _streamer
