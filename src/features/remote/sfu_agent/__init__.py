"""
SFU Agent - Python WebRTC Agent for Remote PC Streaming

A reusable Python module that connects to a WebRTC SFU server
to stream screen content and handle remote input events.

Usage:
    from src.features.remote.sfu_agent import SFUAgent, AgentConfig

    config = AgentConfig(
        sfu_url="https://your-sfu-server.com",
        pc_id="unique-pc-id",
        pc_name="My PC"
    )

    agent = SFUAgent(config)
    await agent.start()
"""

from .config import AgentConfig, QualityProfile
from .agent import SFUAgent

__all__ = ["SFUAgent", "AgentConfig", "QualityProfile"]
__version__ = "1.0.0"
