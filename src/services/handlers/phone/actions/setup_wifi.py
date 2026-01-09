"""
WiFi Setup Action - UI Automator 2 Implementation
"""

import time
import uiautomator2 as u2
from utils.drive import (
    util_actions_click,
    util_actions_scroll,
    util_actions_get_elements,
    util_actions_redirect,
)


def setup_wifi(device: u2.Device) -> bool:
    """
    Connect device to WiFi

    Args:
        device: UIAutomator2 Device instance

    Returns:
        True if successful, False otherwise
    """
    try:
        wifi_networks = [
            {"name": "MyzenQ9", "password": "0906708345"},
            {"name": "Sea Dragon IT", "password": "@seadragonit99"},
            {"name": "Canh-A19.16", "password": "Canh56789"},
            {"name": "Canh-A19.16- 5G", "password": "Canh56789"},
        ]

        print("Opening Settings search...")
        profile_button = device(description="Samsung account profile")
        if profile_button.exists:
            util_actions_click.click_on_loc(
                device=device,
                x_loc=profile_button.info.get("bounds", {}).get("left", 540) - 50,
                y_loc=profile_button.info.get("bounds", {}).get("top", 100) + 50,
            )

        # Search for Connections
        search_field = device(
            resourceId="com.android.settings.intelligence:id/search_src_text"
        )
        if search_field.exists:
            search_field.set_text("Connections")
            time.sleep(1)

        # Click on Connections
        connections = device(className="android.widget.TextView", text="Connections")
        if connections.exists:
            connections.click()

        # Click on Wi-Fi
        wifi_option = device(className="android.widget.TextView", text="Wi-Fi")
        if wifi_option.exists:
            wifi_option.click()

        # Turn on WiFi if it's off
        wifi_switch = device(resourceId="com.android.settings:id/switch_widget")
        if wifi_switch.exists and wifi_switch.info.get("text") == "Wi-Fi, Off":
            wifi_switch.click()
            print("Turning on WiFi...")
            time.sleep(8)

        # Try to connect to each network
        for network in wifi_networks:
            print(f"Trying to connect to {network['name']}...")

            # Scroll to find the network
            max_scrolls = 3
            for _ in range(max_scrolls):
                try:
                    wifi_item = device(
                        resourceId="com.android.settings:id/title", text=network["name"]
                    )
                    if wifi_item.exists:

                        # Check if already connected
                        try:
                            status = device(
                                resourceId="com.android.settings:id/summary"
                            )
                            if status.exists and status.info.get("text") == "Connected":
                                print(f"Already connected to {network['name']}")
                                return True
                        except:
                            pass

                        # Click on the network
                        wifi_item.click()

                        # Enter password if needed
                        password_field = device(
                            resourceId="com.android.settings:id/edittext"
                        )
                        if password_field.exists:
                            password_field.set_text(network["password"])

                        # Click connect
                        connect_btn = device(
                            resourceId="com.android.settings:id/button"
                        )
                        if connect_btn.exists:
                            connect_btn.click()

                        # Wait for connection
                        time.sleep(3)

                        # Check if connected successfully
                        try:
                            status = device(
                                resourceId="com.android.settings:id/summary",
                                text="Connected",
                            )
                            if status.exists:
                                print(f"Successfully connected to {network['name']}")
                                return True
                        except:
                            pass

                        # Handle connection error
                        try:
                            error_msg = device(
                                className="android.widget.TextView",
                                text="Couldn't connect to network.",
                            )
                            if error_msg.exists:
                                ok_btn = device(resourceId="android:id/button1")
                                if ok_btn.exists:
                                    ok_btn.click()
                                    time.sleep(1)
                        except:
                            pass

                        break
                    else:
                        # Network not found, scroll down
                        device.swipe(540, 1500, 540, 500, 0.5)
                        time.sleep(1)

                except:
                    # Network not found, try scrolling
                    device.swipe(540, 1500, 540, 500, 0.5)
                    time.sleep(1)

        print("Could not connect to any WiFi network")
        return False

    except Exception as e:
        print(f"Error setting up WiFi: {e}")
        return False
