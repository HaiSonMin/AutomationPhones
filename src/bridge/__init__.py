"""
Bridge Registry - Auto-discovers and exposes all bridge modules
Eliminates need for manual method declarations in main.py
"""

import os
import importlib
from pathlib import Path
from typing import Any, Dict


class BridgeRegistry:
    """
    Automatically discovers all bridge modules and exposes their methods
    to PyWebView's js_api without manual declarations.

    Usage in main.py:
        from bridge import BridgeRegistry
        bridge = BridgeRegistry()
        webview.create_window(..., js_api=bridge)

    React can then call:
        window.pywebview.api.auth_on_login_success(token, user)
        window.pywebview.api.auth_get_token()
        etc.
    """

    def __init__(self):
        """Initialize and auto-discover all bridge modules"""
        self._bridges: Dict[str, Any] = {}
        self._window = None

        print("🌉 BridgeRegistry initializing...")
        self._discover_bridges()
        print(f"✅ BridgeRegistry ready with {len(self._bridges)} bridge(s)")

    def set_window(self, window):
        """Set webview window reference"""
        self._window = window
        # Pass window to all bridges that need it
        for bridge in self._bridges.values():
            if hasattr(bridge, "set_window"):
                bridge.set_window(window)

    def _discover_bridges(self):
        """
        Auto-discover all bridge modules in src/bridge/
        Each subdirectory should contain a bridge instance
        """
        bridge_dir = Path(__file__).parent

        # Scan all subdirectories
        for item in bridge_dir.iterdir():
            if not item.is_dir():
                continue
            if item.name.startswith("_"):  # Skip __pycache__, etc.
                continue

            module_name = item.name
            try:
                # Try to import the bridge module
                # Expected: src/bridge/auth/auth.py exports 'auth_bridge'
                module_path = f"bridge.{module_name}.{module_name}"
                module = importlib.import_module(module_path)

                # Look for a bridge instance (convention: {module_name}_bridge)
                bridge_instance_name = f"{module_name}_bridge"
                if hasattr(module, bridge_instance_name):
                    bridge_instance = getattr(module, bridge_instance_name)
                    self._bridges[module_name] = bridge_instance

                    # Dynamically add all public methods from this bridge
                    self._expose_bridge_methods(module_name, bridge_instance)
                    print(f"  ✓ Loaded bridge: {module_name}")
                else:
                    print(
                        f"  ⚠ Skipped {module_name}: no '{bridge_instance_name}' found"
                    )

            except ImportError as e:
                print(f"  ⚠ Failed to import {module_name}: {e}")
            except Exception as e:
                print(f"  ⚠ Error loading {module_name}: {e}")

    def _expose_bridge_methods(self, module_name: str, bridge_instance: Any):
        """
        Dynamically expose all public methods from a bridge instance
        Methods are prefixed with module name to avoid conflicts

        Example:
            auth_bridge.on_login_success() -> self.auth_on_login_success()
        """
        for attr_name in dir(bridge_instance):
            # Skip private/magic methods
            if attr_name.startswith("_"):
                continue

            attr = getattr(bridge_instance, attr_name)

            # Only expose callable methods
            if callable(attr):
                # Create prefixed method name
                prefixed_name = f"{module_name}_{attr_name}"

                # Dynamically add method to this registry
                setattr(self, prefixed_name, attr)


# Convenience function for main.py
def create_bridge() -> BridgeRegistry:
    """Create and return a bridge registry instance"""
    return BridgeRegistry()
