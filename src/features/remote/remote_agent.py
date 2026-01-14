"""
Remote Agent - Integrated SFU Agent with auth and system info

Provides a high-level interface to start SFU Agent using
stored authentication tokens and system information.
"""

from typing import Optional
import os

from src.bridge.auth import auth_bridge
from src.utils.util_system import get_machine_guid, get_computer_name
from src.features.remote.sfu_agent import SFUAgent, AgentConfig


class RemoteAgentManager:
    """
    Manager for Remote PC streaming with integrated auth.

    Automatically retrieves:
    - Auth token and user info from keyring (via auth_bridge)
    - PC_ID from Windows MachineGUID
    - PC_NAME from computer hostname
    """

    def __init__(self, sfu_url: Optional[str] = None):
        """
        Initialize Remote Agent Manager.

        Args:
            sfu_url: SFU server URL. If not provided, reads from SFU_URL env var.
        """
        self.sfu_url = sfu_url or os.getenv("SFU_URL", "http://localhost:9999")
        self._agent: Optional[SFUAgent] = None

    def create_config(self) -> Optional[AgentConfig]:
        """
        Create AgentConfig from stored auth and system info.

        Returns:
            AgentConfig if authenticated, None if no token found
        """
        # Get token from auth_bridge
        token_result = auth_bridge.get_token()
        if not token_result.get("success"):
            print("❌ No auth token found. Please login first.")
            return None

        token = token_result.get("token")

        # Get user info for user_id
        user_result = auth_bridge.get_current_user()
        user_id = None
        if user_result.get("success") and user_result.get("user"):
            user_id = user_result["user"].get("userId")

        # Get PC info from system
        pc_id = get_machine_guid()
        pc_name = get_computer_name()

        print(f"📡 Creating SFU Agent config:")
        print(f"   PC ID: {pc_id}")
        print(f"   PC Name: {pc_name}")
        print(f"   User ID: {user_id}")
        print(f"   SFU URL: {self.sfu_url}")

        return AgentConfig(
            sfu_url=self.sfu_url,
            pc_id=pc_id,
            pc_name=pc_name,
            auth_token=token,
            user_id=user_id,
        )

    async def start(self) -> bool:
        """
        Start the SFU Agent.

        Returns:
            True if started successfully, False if no auth token
        """
        config = self.create_config()
        if not config:
            return False

        print(f"🚀 Starting SFU Agent: {config.pc_name}")
        self._agent = SFUAgent(config)
        await self._agent.start()
        return True

    async def stop(self) -> None:
        """Stop the SFU Agent."""
        if self._agent:
            await self._agent.stop()
            self._agent = None
            print("🛑 SFU Agent stopped")

    @property
    def is_running(self) -> bool:
        """Check if agent is running."""
        return self._agent.is_running if self._agent else False

    @property
    def is_connected(self) -> bool:
        """Check if connected to SFU."""
        return self._agent.is_connected if self._agent else False


# Convenience function for quick start
async def start_remote_agent(sfu_url: Optional[str] = None) -> RemoteAgentManager:
    """
    Quick start a Remote Agent.

    Args:
        sfu_url: Optional SFU server URL

    Returns:
        RemoteAgentManager instance (may not be started if auth failed)
    """
    manager = RemoteAgentManager(sfu_url)
    await manager.start()
    return manager
