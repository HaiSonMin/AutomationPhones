"""
PyWebView Application - Main Entry Point
Opens React UI and provides Python bridge for token management
"""

import webview
import sys
from pathlib import Path

# Add src to Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from bridge import create_bridge


def main():
    """Main application entry point"""

    # Create bridge registry - auto-discovers all bridges
    bridge = create_bridge()

    # React UI URL
    ui_url = "http://localhost:3000"

    print("🚀 Starting Automation Tool...")
    print("📱 Phone Manager - Desktop Application")
    print(f"🌐 Loading UI from: {ui_url}")
    print("=" * 50)

    # Create window with Python bridge
    window = webview.create_window(
        title="Automation Tool - Phone Manager",
        url=ui_url,
        width=1400,
        height=900,
        resizable=True,
        frameless=False,
        easy_drag=True,
        js_api=bridge,
    )

    # Set window reference (passes to all bridges that need it)
    bridge.set_window(window)

    # Start application
    webview.start(debug=True)


if __name__ == "__main__":
    main()
