"""
Location Setup Action - UI Automator 2 Implementation
"""

import time
import uiautomator2 as u2
from utils.drive import (
    util_actions_click,
    util_actions_scroll,
    util_actions_get_elements,
    util_actions_redirect,
)


def turn_off_location(device: u2.Device) -> bool:
    """
    Turn off location services on the device

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

        # Search for Location
        search_field = device(
            resourceId="com.android.settings.intelligence:id/search_src_text"
        )
        if search_field.exists:
            search_field.set_text("Location")
            time.sleep(1)

        # Click on Location
        location_option = device(className="android.widget.TextView", text="Location")
        if location_option.exists:
            location_option.click()
            time.sleep(1)

        # Handle any permission dialogs
        try:
            deny_btn = device(resourceId="android:id/button2")
            if deny_btn.exists:
                deny_btn.click()
        except:
            pass

        # Turn off Location
        location_switch = device(resourceId="com.android.settings:id/switch_widget")
        if location_switch.exists:
            if location_switch.info.get("text") == "Location, On":
                location_switch.click()
                print("Location turned off")

        # Handle additional permission dialogs
        try:
            deny_btn = device(resourceId="android:id/button2")
            if deny_btn.exists:
                deny_btn.click()
        except:
            pass

        # Scroll down to access additional location settings
        print("Scrolling down for more options...")
        device.swipe(540, 2100, 540, 200, 0.5)
        time.sleep(1)

        # Turn off Earthquake alerts
        try:
            print("Checking Earthquake alerts...")
            earthquake_alerts = device(
                className="android.widget.TextView", text="Earthquake alerts"
            )
            if earthquake_alerts.exists:
                earthquake_alerts.click()
                time.sleep(1)

                earthquake_switch = device(
                    resourceId="com.google.android.gms:id/toggle"
                )
                if (
                    earthquake_switch.exists
                    and earthquake_switch.info.get("text") == "On"
                ):
                    earthquake_switch.click()
                    print("Earthquake alerts turned off")

                # Go back
                back_btn = device(
                    className="android.widget.ImageButton", description="Navigate up"
                )
                if back_btn.exists:
                    back_btn.click()
                    time.sleep(1)
        except:
            pass

        # Turn off Emergency Location Service
        try:
            print("Checking Emergency Location Service...")
            emergency_loc = device(
                className="android.widget.TextView", text="Emergency Location Service"
            )
            if emergency_loc.exists:
                emergency_loc.click()
                time.sleep(1)

                emergency_switch = device(resourceId="android:id/switch_widget")
                if (
                    emergency_switch.exists
                    and emergency_switch.info.get("text") == "On"
                ):
                    emergency_switch.click()
                    print("Emergency Location Service turned off")

                # Go back
                back_btn = device(
                    className="android.widget.ImageButton", description="Navigate up"
                )
                if back_btn.exists:
                    back_btn.click()
                    time.sleep(1)
        except:
            pass

        # Turn off Location Accuracy
        try:
            print("Checking Location Accuracy...")
            loc_accuracy = device(
                className="android.widget.TextView", text="Location Accuracy"
            )
            if loc_accuracy.exists:
                loc_accuracy.click()
                time.sleep(1)

                accuracy_switch = device(resourceId="android:id/switch_widget")
                if accuracy_switch.exists and accuracy_switch.info.get("text") == "On":
                    accuracy_switch.click()
                    print("Location Accuracy turned off")
        except:
            pass

        # Navigate back to main settings
        util_actions_redirect.move_back_until_find_element_by_description(
            device=device, description="Samsung account profile", timeout=3
        )

        return True

    except Exception as e:
        print(f"Error turning off location: {e}")
        return False
