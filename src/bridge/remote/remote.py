"""
Remote Bridge - Provides SFU Agent control for React UI

Exposes methods to start/stop remote PC streaming agent.
"""

import asyncio
import threading
from typing import Dict, Any

from src.features.remote.remote_agent import RemoteAgentManager


class RemoteBridge:
    """
    Bridge for controlling Remote PC streaming agent.

    Provides methods callable from React UI to manage SFU agent.
    Auto-starts agent on app startup if user is logged in.
    """

    def __init__(self):
        self._manager: RemoteAgentManager | None = None
        self._auto_start_thread = None
        print("🖥️ RemoteBridge initialized")

        # Auto-start agent if user is already logged in
        self._auto_start_agent()

    def _auto_start_agent(self):
        """Auto-start agent in background if user has token."""

        def start_in_thread():
            try:
                # Lazy import to avoid circular import
                from src.bridge.auth import auth_bridge

                # Check if user has token
                token_result = auth_bridge.get_token()
                if not token_result.get("success"):
                    print("⏭️ Remote agent not started - no auth token")
                    return

                print("🚀 Auto-starting remote agent...")
                result = self.start_agent()
                if result.get("success"):
                    print("✅ Remote agent started successfully")
                else:
                    print(f"❌ Remote agent failed to start: {result.get('error')}")
            except Exception as e:
                print(f"❌ Auto-start error: {e}")

        # Start in background thread to not block app startup
        self._auto_start_thread = threading.Thread(target=start_in_thread, daemon=True)
        self._auto_start_thread.start()

    def start_agent(self, sfu_url: str = None) -> Dict[str, Any]:
        """
        Start the SFU Agent.

        Args:
            sfu_url: Optional SFU server URL

        Returns:
            Result dict with success status
        """
        try:
            if self._manager and self._manager.is_running:
                print("⚠️ Agent already running, skipping start")
                return {"success": True, "message": "Agent already running"}

            self._manager = RemoteAgentManager(sfu_url)

            # Run async start in new event loop
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                result = loop.run_until_complete(self._manager.start())
            finally:
                loop.close()

            if result:
                print("✅ Agent started and connected")
                return {"success": True, "message": "Agent started"}
            else:
                print("❌ Agent start failed - no auth token")
                self._manager = None
                return {"success": False, "error": "Failed to start - no auth token"}
        except Exception as e:
            print(f"❌ Agent start error: {e}")
            self._manager = None
            return {"success": False, "error": str(e)}

    def stop_agent(self) -> Dict[str, Any]:
        """Stop the SFU Agent."""
        try:
            if self._manager:
                print("🛑 Stopping SFU agent...")
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                try:
                    loop.run_until_complete(self._manager.stop())
                finally:
                    loop.close()
                self._manager = None
                print("✅ Agent stopped and disconnected")
                return {"success": True, "message": "Agent stopped"}
            print("⚠️ Agent not running, nothing to stop")
            return {"success": True, "message": "Agent not running"}
        except Exception as e:
            print(f"❌ Agent stop error: {e}")
            return {"success": False, "error": str(e)}

    def get_status(self) -> Dict[str, Any]:
        """Get agent status."""
        if not self._manager:
            return {
                "running": False,
                "connected": False,
            }
        return {
            "running": self._manager.is_running,
            "connected": self._manager.is_connected,
        }


# Bridge instance for auto-discovery
remote_bridge = RemoteBridge()
