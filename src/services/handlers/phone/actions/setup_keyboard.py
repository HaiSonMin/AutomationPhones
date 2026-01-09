"""
Keyboard Setup Action - UI Automator 2 Implementation
"""

import time
import uiautomator2 as u2
from utils.drive import (
    util_actions_click,
    util_actions_scroll,
    util_actions_get_elements,
    util_actions_redirect,
)


def setup_keyboard(device: u2.Device) -> bool:
    """
    Setup keyboard to use Samsung Keyboard with English only

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

        # Click on Language and input
        lang_input = device(
            className="android.widget.TextView", text="Language and input"
        )
        if lang_input.exists:
            lang_input.click()

        # Click on On-screen keyboard
        onscreen_keyboard = device(
            className="android.widget.TextView", text="On-screen keyboard"
        )
        if onscreen_keyboard.exists:
            onscreen_keyboard.click()
            time.sleep(4)

        # Click on Samsung Keyboard
        try:
            samsung_keyboard = device(
                className="android.widget.TextView", text="Samsung Keyboard"
            )
            if samsung_keyboard.exists:
                samsung_keyboard.click()
        except:
            # Fallback: click at a specific location
            util_actions_click.click_on_loc(device=device, y_loc=400)

        # Click on Languages and types
        try:
            lang_types = device(
                className="android.widget.TextView", text="Languages and types"
            )
            if lang_types.exists:
                lang_types.click()
        except:
            raise Exception("Could not find Languages and types option")

        # Remove Vietnamese language
        print("Removing Vietnamese language...")
        more_options = device(description="More options")
        if more_options.exists:
            more_options.click()

        try:
            # Click on Remove
            remove_option = device(
                resourceId="com.sec.android.inputmethod:id/title", text="Remove"
            )
            if remove_option.exists:
                remove_option.click()

            # Click Select All
            select_all = device(
                resourceId="com.sec.android.inputmethod:id/select_all_checkbox"
            )
            if select_all.exists:
                select_all.click()

            # Uncheck English (US) to keep it
            english_us = device(
                resourceId="com.sec.android.inputmethod:id/tv_language",
                text="English (US)",
            )
            if english_us.exists:
                english_us.click()

            # Click Remove
            remove_btn = device(resourceId="com.sec.android.inputmethod:id/remove_menu")
            if remove_btn.exists:
                remove_btn.click()

        except:
            pass

        finally:
            # Navigate back
            util_actions_click.click_on_loc(device=device, y_loc=2000)
            time.sleep(1)

            util_actions_redirect.move_back_until_find_element_by_text(
                device=device, text="Default keyboard", timeout=3
            )

        # Set Samsung Keyboard as default
        print("Setting Samsung Keyboard as default...")
        default_keyboard = device(
            className="android.widget.TextView", text="Default keyboard"
        )
        if default_keyboard.exists:
            default_keyboard.click()

            time.sleep(1)
            samsung_option = device(
                className="android.widget.TextView", text="Samsung Keyboard"
            )
            if samsung_option.exists:
                samsung_option.click()

        time.sleep(1)

        # Navigate back to main settings
        util_actions_redirect.move_back_until_find_element_by_description(
            device=device, description="Samsung account profile", timeout=3
        )

        return True

    except Exception as e:
        print(f"Error setting up keyboard: {e}")
        return False
