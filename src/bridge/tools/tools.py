"""
Tools Bridge - Exposes tool management functions to React UI
"""

from features.tools.common import FeatureToolCommon


class ToolsBridge:
    def __init__(self):
        """Initialize tools bridge"""
        self.tool_common = FeatureToolCommon()
        print("🔧 ToolsBridge initialized")

    def check_health_server(self):
        """Check server health status"""
        return self.tool_common.check_health_server()

    def start_stop(self):
        """Start or stop the application"""
        return self.tool_common.start_stop()

    def get_app_state(self):
        """Get current application state"""
        return self.tool_common.get_app_state()


# Export bridge instance
tools_bridge = ToolsBridge()
