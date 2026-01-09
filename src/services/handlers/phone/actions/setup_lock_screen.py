"""
Lock Screen Setup Action - UI Automator 2 Implementation
"""

import time
import uiautomator2 as u2
from utils.drive import (
    util_actions_click,
    util_actions_scroll,
    util_actions_get_elements,
    util_actions_redirect,
)


def setup_lock_screen(device: u2.Device) -> bool:
    """
    Setup lock screen to None (no lock)

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

        # Search for Lock screen
        search_field = device(
            resourceId="com.android.settings.intelligence:id/search_src_text"
        )
        if search_field.exists:
            search_field.set_text("Lock screen")
            time.sleep(1)

        # Click on Lock screen
        lock_screen_option = device(
            className="android.widget.TextView", text="Lock screen"
        )
        if lock_screen_option.exists:
            lock_screen_option.click()
            time.sleep(1)

        # Click on Screen lock type
        screen_lock_type = device(
            className="android.widget.TextView", text="Screen lock type"
        )
        if screen_lock_type.exists:
            screen_lock_type.click()

        # Click on None
        none_option = device(className="android.widget.TextView", text="None")
        if none_option.exists:
            none_option.click()

            # Confirm if prompted
            try:
                confirm_btn = device(resourceId="android:id/button1")
                if confirm_btn.exists:
                    confirm_btn.click()
            except:
                pass

        time.sleep(1)

        # Navigate back to main settings
        util_actions_redirect.move_back_until_find_element_by_description(
            device=device, description="Samsung account profile", timeout=3
        )

        return True

    except Exception as e:
        print(f"Error setting up lock screen: {e}")
        return False
