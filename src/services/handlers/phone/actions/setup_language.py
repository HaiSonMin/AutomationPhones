"""
Language Setup Action - UI Automator 2 Implementation
"""

import time
import uiautomator2 as u2
from utils.drive import (
    util_actions_click,
    util_actions_scroll,
    util_actions_get_elements,
    util_actions_redirect,
)
from helpers import helper_phone


def setup_language(device: u2.Device, device_key: str) -> bool:
    """
    Setup device language to English (US)

    Args:
        device: UIAutomator2 Device instance
        device_key: Device identifier

    Returns:
        True if successful, False otherwise
    """
    try:
        device_language = helper_phone.get_device_language(device_key)

        if device_language and device_language.strip() == "en-US":
            print("Language is already English")
            return True

        time.sleep(1)
        device.press("home")

        # Open settings search
        print("Searching for Settings...")
        device.swipe(540, 2000, 540, 300, 0.5)
        time.sleep(1)

        # Click on search bar
        search_bar = device(
            resourceId="com.sec.android.app.launcher:id/app_search_edit_text"
        )
        if search_bar.exists:
            search_bar.click()

        # Handle Vietnamese UI
        try:
            # Check if device is in Vietnamese
            more_options = device(
                className="android.widget.LinearLayout",
                descriptionContains="Tùy chọn khác",
            )
            if more_options.exists:
                print("Device is in Vietnamese, switching to English...")

                # Search for Settings in Vietnamese
                search_input = device(
                    resourceId="com.samsung.android.app.galaxyfinder:id/edit_search"
                )
                if search_input.exists:
                    search_input.set_text("Cài đặt")
                    time.sleep(1)

                    # Click on Settings
                    settings_option = device(description="Cài đặt")
                    if settings_option.exists:
                        settings_option.click()

                # Search for General Management in Vietnamese
                profile_button = device(description="Hồ sơ Samsung account")
                if profile_button.exists:
                    util_actions_click.click_on_loc(
                        device=device,
                        x_loc=profile_button.info.get("bounds", {}).get("left", 540)
                        - 50,
                        y_loc=profile_button.info.get("bounds", {}).get("top", 100)
                        + 50,
                    )

                search_field = device(
                    resourceId="com.android.settings.intelligence:id/search_src_text"
                )
                if search_field.exists:
                    search_field.set_text("Quản lý chung")
                    time.sleep(1)

                    # Click on General Management
                    general_mgmt = device(
                        className="android.widget.TextView", text="Quản lý chung"
                    )
                    if general_mgmt.exists:
                        general_mgmt.click()

                # Click on Language and input
                lang_input = device(
                    className="android.widget.TextView", text="Ngôn ngữ và bàn phím"
                )
                if lang_input.exists:
                    lang_input.click()

                # Click on Language
                util_actions_click.click_on_loc(device=device, y_loc=370)

                # Try to find English US
                try:
                    english_us = device(description="Tiếng Anh (Hoa Kỳ)")
                    if english_us.exists:
                        english_us.click()

                        # Apply changes
                        apply_btn = device(
                            resourceId="com.android.settings:id/apply_button"
                        )
                        if apply_btn.exists:
                            apply_btn.click()

                        # Remove Vietnamese
                        vietnamese = device(description="Vietnamese (Vietnam)")
                        if vietnamese.exists:
                            device.long_click(vietnamese)

                            remove_btn = device(
                                className="android.widget.Button", text="Remove"
                            )
                            if remove_btn.exists:
                                remove_btn.click()

                                confirm_btn = device(
                                    resourceId="com.android.settings:id/button1"
                                )
                                if confirm_btn.exists:
                                    confirm_btn.click()

                except:
                    # Add English language
                    add_lang_btn = device(
                        resourceId="com.android.settings:id/add_language"
                    )
                    if add_lang_btn.exists:
                        add_lang_btn.click()

                        english = device(description="Tiếng Anh")
                        if english.exists:
                            english.click()

                        us_option = device(description="Hoa Kỳ")
                        if us_option.exists:
                            us_option.click()

                        set_default = device(resourceId="android:id/button1")
                        if set_default.exists:
                            set_default.click()

                # Remove Vietnamese if present
                try:
                    edit_btn = device(className="android.widget.Button", text="Edit")
                    if edit_btn.exists:
                        edit_btn.click()
                    else:
                        remove_btn = device(
                            className="android.widget.Button", text="Remove"
                        )
                        if remove_btn.exists:
                            remove_btn.click()

                    vietnamese = device(description="Vietnamese (Vietnam)")
                    if vietnamese.exists:
                        vietnamese.click()

                        remove_action = device(description="Remove")
                        if remove_action.exists:
                            remove_action.click()

                        confirm_remove = device(
                            resourceId="com.android.settings:id/button1"
                        )
                        if confirm_remove.exists:
                            confirm_remove.click()

                except:
                    pass

        except:
            # Device is already in English
            print("Device appears to be in English already")
            return True

        # Navigate back to main settings
        util_actions_redirect.move_back_until_find_element_by_description(
            device=device, description="Samsung account profile", timeout=3
        )

        return True

    except Exception as e:
        print(f"Error setting up language: {e}")
        return False
