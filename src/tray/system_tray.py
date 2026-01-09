"""
System Tray Manager - Handles system tray icon and menu
"""

import threading
import pystray
from PIL import Image, ImageDraw
from pathlib import Path


class SystemTrayManager:
    def __init__(self, bridge_registry):
        self.bridge_registry = bridge_registry
        self.tray = None
        self.window = None
        self.running = False

    def create_icon(self, icon_path=None, size=64):
        """Load custom icon or create a default one"""
        if icon_path and Path(icon_path).exists():
            # Load custom icon
            try:
                image = Image.open(icon_path)
                # Resize to appropriate size while maintaining aspect ratio
                image = image.resize((size, size), Image.Resampling.LANCZOS)
                return image
            except Exception as e:
                print(f"Error loading icon: {e}")
                # Fall back to default icon

        # Create a simple icon with phone symbol (fallback)
        image = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)

        # Draw phone outline
        phone_margin = size // 8
        phone_rect = [
            phone_margin,
            phone_margin * 2,
            size - phone_margin,
            size - phone_margin,
        ]
        draw.rounded_rectangle(phone_rect, radius=size // 8, fill="#1890ff")

        # Draw screen
        screen_margin = size // 10
        screen_rect = [
            phone_rect[0] + screen_margin,
            phone_rect[1] + screen_margin,
            phone_rect[2] - screen_margin,
            phone_rect[3] - screen_margin,
        ]
        draw.rounded_rectangle(screen_rect, radius=size // 16, fill="white")

        return image

    def setup_menu(self):
        """Setup the system tray menu"""
        return pystray.Menu(
            pystray.MenuItem(
                "Start Tool" if not self.get_app_state() else "Stop Tool",
                self.toggle_start_stop,
                checked=lambda item: self.get_app_state(),
            ),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Open Application", self.show_window),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Exit Application", self.exit_application),
        )

    def get_app_state(self):
        """Get current application state"""
        try:
            from features.tools.common import app_running

            return app_running
        except:
            return False

    def toggle_start_stop(self, icon, item):
        """Toggle start/stop application"""
        try:
            tools_bridge = self.bridge_registry.get_bridge("tools")
            if tools_bridge:
                result = tools_bridge.start_stop()
                print(result.get("message", ""))
                # Update menu
                self.update_menu()
        except Exception as e:
            print(f"Error toggling start/stop: {e}")

    def show_window(self, icon, item):
        """Show the main window"""
        if self.window:
            self.window.show()
            self.window.restore()

    def exit_application(self, icon, item):
        """Exit the application completely"""
        import os
        import sys

        self.running = False
        if self.tray:
            self.tray.stop()
        if self.window:
            self.window.destroy()

        # Force exit the application
        os._exit(0)

    def update_menu(self):
        """Update the system tray menu"""
        if self.tray:
            self.tray.menu = self.setup_menu()

    def start(self, window):
        """Start the system tray"""
        self.window = window
        self.running = True

        # Get icon path - security.png in the same directory
        icon_path = Path(__file__).parent / "security.png"

        # Create icon
        icon_image = self.create_icon(str(icon_path))

        # Create tray icon
        self.tray = pystray.Icon(
            "phone_manager", icon_image, "Phone Manager", self.setup_menu()
        )

        # Run in separate thread
        threading.Thread(target=self.tray.run, daemon=True).start()

    def stop(self):
        """Stop the system tray"""
        self.running = False
        if self.tray:
            self.tray.stop()
