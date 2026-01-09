"""
Auto Update Setup Action - UI Automator 2 Implementation
"""

import time
import uiautomator2 as u2
from utils.drive import (
    util_actions_click,
    util_actions_scroll,
    util_actions_get_elements,
    util_actions_redirect,
)


def turnoff_auto_update(device: u2.Device) -> bool:
    """
    Turn off automatic software updates

    Args:
        device: UIAutomator2 Device instance

    Returns:
        True if successful, False otherwise
    """
    try:
        print("Opening Settings search...")
        profile_button = device(description="Samsung account profile")
        if profile_button.exists:
            util_actions_click.click_on_loc(
                device=device,
                x_loc=profile_button.info.get("bounds", {}).get("left", 540) - 50,
                y_loc=profile_button.info.get("bounds", {}).get("top", 100) + 50,
            )

        # Search for Software update
        search_field = device(
            resourceId="com.android.settings.intelligence:id/search_src_text"
        )
        if search_field.exists:
            search_field.set_text("Software update")
            time.sleep(1)

        # Find and click on Software update
        titles = device(
            className="android.widget.TextView", resourceId="android:id/title"
        )
        for title in titles:
            if title.info.get("text") == "Software update":
                title.click()
                break

        # Turn off auto download over WiFi
        print("Turning off auto download over WiFi...")
        auto_update_switch = device(resourceId="android:id/switch_widget")
        if auto_update_switch.exists:
            if auto_update_switch.info.get("text") == "On":
                auto_update_switch.click()
                print("Auto download over WiFi turned off")
            else:
                print("Auto download over WiFi is already off")

        time.sleep(1)

        # Navigate back to main settings
        util_actions_redirect.move_back_until_find_element_by_description(
            device=device, description="Samsung account profile", timeout=3
        )

        return True

    except Exception as e:
        print(f"Error turning off auto update: {e}")
        return False
