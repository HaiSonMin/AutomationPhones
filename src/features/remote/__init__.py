"""
Remote PC Feature - SFU Agent integration

Provides remote PC streaming capabilities integrated with
authentication and system identification.
"""

from .remote_agent import RemoteAgentManager, start_remote_agent
from .sfu_agent import SFUAgent, AgentConfig, QualityProfile

__all__ = [
    # High-level integration
    "RemoteAgentManager",
    "start_remote_agent",
    # Low-level SFU Agent
    "SFUAgent",
    "AgentConfig",
    "QualityProfile",
]
