"""
Update Bridge - Exposes update management to React UI

This file exists to match BridgeRegistry naming convention:
- BridgeRegistry looks for bridge.{name}.{name} (bridge.update.update)
- Exports update_bridge for auto-discovery
"""

from .update_manager import UpdateManager

# Create singleton instance with convention name for BridgeRegistry
update_bridge = UpdateManager()
