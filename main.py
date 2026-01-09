"""
PyWebView Application - Main Entry Point
Opens React UI and provides Python bridge for token management
"""

import webview
import sys
import os
import signal
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add src to Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from bridge import create_bridge
from tray.system_tray import SystemTrayManager
from constants.constant_value import CONST_VAL_UI_URL


def main():
    # Global reference for cleanup
    global tray_manager

    def signal_handler(sig, frame):
        """Handle Ctrl+C signal"""
        if "tray_manager" in globals():
            tray_manager.stop()
        os._exit(0)

    # Register signal handler
    signal.signal(signal.SIGINT, signal_handler)

    # Create bridge registry - auto-discovers all bridges
    bridgeRegistry = create_bridge()

    print("🚀 Starting Automation Tool...")
    print("=" * 50)

    # Create system tray manager
    tray_manager = SystemTrayManager(bridgeRegistry)

    def hide_window():
        """Hide window to system tray instead of closing"""
        window.hide()
        return False  # Prevent window from closing

    # Create window with Python bridge
    window = webview.create_window(
        title="Automation Tool - Phone Manager",
        url=CONST_VAL_UI_URL,
        width=1400,
        height=900,
        resizable=True,
        frameless=False,
        easy_drag=True,
        js_api=bridgeRegistry,
        confirm_close=False,
    )

    # Set window reference (passes to all bridges that need it)
    bridgeRegistry.set_window(window)
    tray_manager.window = window

    # Register event handler to hide window instead of closing
    window.events.closing += hide_window

    # Start system tray
    tray_manager.start(window)

    # Start application
    try:
        webview.start(debug=True)
    except KeyboardInterrupt:
        print("\n🛑 Application interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
    finally:
        # Clean up system tray
        if "tray_manager" in globals():
            tray_manager.stop()


if __name__ == "__main__":
    main()
