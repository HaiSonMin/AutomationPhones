"""
Timezone Setup Action - UI Automator 2 Implementation
"""

import time
import uiautomator2 as u2
from utils.drive import (
    util_actions_click,
    util_actions_scroll,
    util_actions_get_elements,
    util_actions_redirect,
)


def setup_timezone(device: u2.Device) -> bool:
    """
    Setup device timezone to Los Angeles (Pacific Time)

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

        # Search for General management
        search_field = device(
            resourceId="com.android.settings.intelligence:id/search_src_text"
        )
        if search_field.exists:
            search_field.set_text("General management")
            time.sleep(1)

        # Find and click on General management
        titles = device(
            className="android.widget.TextView", resourceId="android:id/title"
        )
        for title in titles:
            if title.info.get("text") == "General management":
                title.click()
                break

        # Click on Date and time
        date_time = device(className="android.widget.TextView", text="Date and time")
        if date_time.exists:
            date_time.click()

        # Turn off automatic date and time if it's on
        try:
            print("Checking automatic date and time...")
            auto_switch = device(resourceId="android:id/switch_widget")
            if auto_switch.exists and auto_switch.info.get("text") == "On":
                auto_switch.click()
                print("Turned off automatic date and time")
        except:
            pass

        # Click on Select time zone or Automatic date and time
        try:
            print("Looking for Select time zone...")
            select_timezone = device(
                className="android.widget.TextView", text="Select time zone"
            )
            if select_timezone.exists:
                select_timezone.click()
        except:
            # Alternative path
            try:
                auto_date_time = device(
                    className="android.widget.TextView", text="Automatic date and time"
                )
                if auto_date_time.exists:
                    auto_date_time.click()
            except:
                print("Could not find timezone options")
                return False

        # Click on Region
        print("Selecting region...")
        region = device(className="android.widget.TextView", text="Region")
        if region.exists:
            region.click()

        # Search for US
        search_input = device(resourceId="com.android.settings:id/search_src_text")
        if search_input.exists:
            search_input.set_text("US")
            time.sleep(1)

        # Click on first result (should be US)
        util_actions_click.click_on_loc(device=device, y_loc=360)

        # Select Los Angeles timezone
        print("Selecting Los Angeles timezone...")
        los_angeles = device(className="android.widget.TextView", text="Los Angeles")
        if los_angeles.exists:
            los_angeles.click()
        else:
            # Try scrolling to find it
            for _ in range(3):
                device.swipe(540, 1500, 540, 500, 0.5)
                time.sleep(1)
                los_angeles = device(
                    className="android.widget.TextView", text="Los Angeles"
                )
                if los_angeles.exists:
                    los_angeles.click()
                    break

        time.sleep(1)

        # Navigate back to main settings
        util_actions_redirect.move_back_until_find_element_by_description(
            device=device, description="Samsung account profile", timeout=3
        )

        return True

    except Exception as e:
        print(f"Error setting up timezone: {e}")
        return False
