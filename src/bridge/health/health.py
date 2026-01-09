"""
Health Bridge - Exposes health check functions to React UI
"""

from features.tools.common import FeatureToolCommon


class HealthBridge:
    def __init__(self):
        """Initialize health bridge"""
        self.tool_common = FeatureToolCommon()
        print("❤️ HealthBridge initialized")

    def check_health_server(self):
        """Check server health status"""
        return self.tool_common.check_health_server()


# Export bridge instance
health_bridge = HealthBridge()
