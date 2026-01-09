"""
UI Automator 2 Actions - Redirect Operations
Converted from Appium to UI Automator 2
"""

import time
import subprocess
from typing import Optional
from uiautomator2 import Device
from constants import constant_phone


def move_back(device: Device, number_move: int) -> bool:
    """
    Move back specified number of times

    Args:
        device: UIAutomator2 Device instance
        number_move: Number of times to press back

    Returns:
        True if successful
    """
    count = 0
    while count < number_move:
        device.press("back")
        time.sleep(1)
        count += 1
    return True


def move_back_until_find_element_by_selector(
    device: Device, selector: str, timeout: int = 10
) -> bool:
    """
    Move back until element is found

    Args:
        device: UIAutomator2 Device instance
        selector: UIAutomator2 selector string
        timeout: Timeout for checking element existence

    Returns:
        True if element found, False otherwise
    """
    print(f"Move back for find element by selector: {selector}")
    max_attempts = 20  # Prevent infinite loop

    for _ in range(max_attempts):
        element = device(selector)
        if element.exists:
            print("Element found!")
            return True
        device.press("back")
        time.sleep(1)

    print("Element not found after maximum attempts")
    return False


def move_back_until_find_element_by_resource_id(
    device: Device, resource_id: str, timeout: int = 10
) -> bool:
    """
    Move back until element with resource ID is found

    Args:
        device: UIAutomator2 Device instance
        resource_id: Android resource ID
        timeout: Timeout for checking element existence

    Returns:
        True if element found, False otherwise
    """
    print(f"Move back for find element by resource ID: {resource_id}")
    max_attempts = 20

    for _ in range(max_attempts):
        element = device(resourceId=f'"{resource_id}"')
        if element.exists:
            print("Element found!")
            return True
        device.press("back")
        time.sleep(1)

    print("Element not found after maximum attempts")
    return False


def move_back_until_find_element_by_text(
    device: Device, text: str, timeout: int = 10, contains: bool = False
) -> bool:
    """
    Move back until element with text is found

    Args:
        device: UIAutomator2 Device instance
        text: Text to search for
        timeout: Timeout for checking element existence
        contains: If True, search for text containing the string

    Returns:
        True if element found, False otherwise
    """
    print(f"Move back for find element by text: {text}")
    max_attempts = 20

    for _ in range(max_attempts):
        if contains:
            element = device(textContains=f'"{text}"')
        else:
            element = device(text=f'"{text}"')

        if element.exists:
            print("Element found!")
            return True
        device.press("back")
        time.sleep(1)

    print("Element not found after maximum attempts")
    return False


def move_back_until_find_element_by_description(
    device: Device, description: str, timeout: int = 10, contains: bool = False
) -> bool:
    """
    Move back until element with description is found

    Args:
        device: UIAutomator2 Device instance
        description: Content description to search for
        timeout: Timeout for checking element existence
        contains: If True, search for description containing the string

    Returns:
        True if element found, False otherwise
    """
    print(f"Move back for find element by description: {description}")
    max_attempts = 20

    for _ in range(max_attempts):
        if contains:
            element = device(descriptionContains=f'"{description}"')
        else:
            element = device(description=f'"{description}"')

        if element.exists:
            print("Element found!")
            return True
        device.press("back")
        time.sleep(1)

    print("Element not found after maximum attempts")
    return False


def move_back_home_ig(
    device: Device, home_selector: str = None, logo_selector: str = None
) -> bool:
    """
    Move back until Instagram home is reached

    Args:
        device: UIAutomator2 Device instance
        home_selector: Custom selector for home button
        logo_selector: Custom selector for Instagram logo

    Returns:
        True if home reached, False otherwise
    """
    max_attempts = 20

    # Default selectors for Instagram
    if not home_selector:
        home_selector = (
            'description("Home")'  # or 'resourceId="com.instagram.android:id/tab_bar"'
        )
    if not logo_selector:
        logo_selector = 'description("Instagram")'  # or 'resourceId="com.instagram.android:id/action_bar_large_title"'

    for _ in range(max_attempts):
        try:
            time.sleep(1)
            # Try to click home button
            home_element = device(home_selector)
            if home_element.exists:
                home_element.click()
                time.sleep(1)

                # Check if logo is visible (confirming we're at home)
                logo_element = device(logo_selector)
                if logo_element.exists:
                    print("Reached Instagram home")
                    return True

            # If not at home, press back
            device.press("back")
            time.sleep(1)
        except Exception as e:
            print(f"Error in move_back_home_ig: {e}")
            device.press("back")
            time.sleep(1)

    print("Could not reach Instagram home after maximum attempts")
    return False


def redirect_to_link(device: Device, link_to: str) -> bool:
    """
    Redirect to a link using intent

    Args:
        device: UIAutomator2 Device instance
        link_to: URL to open

    Returns:
        True if redirect successful
    """
    try:
        # Open link with intent
        adb_command = f'adb shell am start -a android.intent.action.VIEW -d "{link_to}"'
        subprocess.run(adb_command, shell=True)
        time.sleep(3)

        # Handle app chooser if present
        print("Handling app chooser if present")

        # Try to find and click on "Always" button
        always_button = device(resourceId="android:id/button_always")
        if always_button.exists:
            print("Found 'Always' button, clicking...")
            always_button.click()
            time.sleep(2)

        # Try to find and click on "Just once" button
        just_once_button = device(resourceId="android:id/button_once")
        if just_once_button.exists:
            print("Found 'Just once' button, clicking...")
            just_once_button.click()
            time.sleep(2)

        return True
    except Exception as e:
        print(f"Failed to redirect to link: {e}")
        return False


def open_app(device: Device, app_package: str, app_activity: str = None) -> bool:
    """
    Open a specific app

    Args:
        device: UIAutomator2 Device instance
        app_package: Package name of the app
        app_activity: Activity name (optional)

    Returns:
        True if app opened successfully
    """
    try:
        if app_activity:
            device.app_start(app_package, app_activity)
        else:
            device.app_start(app_package)
        time.sleep(3)
        return True
    except Exception as e:
        print(f"Failed to open app: {e}")
        return False


def close_app(device: Device, app_package: str) -> bool:
    """
    Close a specific app

    Args:
        device: UIAutomator2 Device instance
        app_package: Package name of the app

    Returns:
        True if app closed successfully
    """
    try:
        device.app_stop(app_package)
        time.sleep(1)
        return True
    except Exception as e:
        print(f"Failed to close app: {e}")
        return False


def go_home(device: Device) -> bool:
    """
    Go to device home screen

    Args:
        device: UIAutomator2 Device instance

    Returns:
        True if successful
    """
    try:
        device.press("home")
        time.sleep(1)
        return True
    except Exception as e:
        print(f"Failed to go home: {e}")
        return False


def go_recent_apps(device: Device) -> bool:
    """
    Open recent apps screen

    Args:
        device: UIAutomator2 Device instance

    Returns:
        True if successful
    """
    try:
        device.press("recent")
        time.sleep(1)
        return True
    except Exception as e:
        print(f"Failed to open recent apps: {e}")
        return False


def open_notifications(device: Device) -> bool:
    """
    Open notification shade

    Args:
        device: UIAutomator2 Device instance

    Returns:
        True if successful
    """
    try:
        device.open_notification()
        time.sleep(1)
        return True
    except Exception as e:
        print(f"Failed to open notifications: {e}")
        return False


def close_notifications(device: Device) -> bool:
    """
    Close notification shade

    Args:
        device: UIAutomator2 Device instance

    Returns:
        True if successful
    """
    try:
        # Swipe down to close notifications or press back
        device.swipe(540, 100, 540, 1800, 0.5)
        time.sleep(1)
        return True
    except Exception as e:
        print(f"Failed to close notifications: {e}")
        return False


def lock_screen(device: Device) -> bool:
    """
    Lock the device screen

    Args:
        device: UIAutomator2 Device instance

    Returns:
        True if successful
    """
    try:
        device.screen_off()
        time.sleep(1)
        return True
    except Exception as e:
        print(f"Failed to lock screen: {e}")
        return False


def unlock_screen(device: Device) -> bool:
    """
    Unlock the device screen

    Args:
        device: UIAutomator2 Device instance

    Returns:
        True if successful
    """
    try:
        device.screen_on()
        device.unlock()
        time.sleep(1)
        return True
    except Exception as e:
        print(f"Failed to unlock screen: {e}")
        return False


# Helper functions for backward compatibility
def move_back_until_find_element_by_xpath(
    device: Device, xpath: str, timeout: int = 10
) -> bool:
    """Wrapper for backward compatibility"""
    selector = convert_xpath_to_uiautomator_selector(xpath)
    return move_back_until_find_element_by_selector(device, selector, timeout)


def move_back_until_find_element_by_id(
    device: Device, id: str, timeout: int = 10
) -> bool:
    """Wrapper for backward compatibility - maps to resource ID"""
    return move_back_until_find_element_by_resource_id(device, id, timeout)


def move_back_until_find_element_by_accessibility_id(
    device: Device, accessibility_id: str, timeout: int = 10
) -> bool:
    """Wrapper for backward compatibility - maps to description"""
    return move_back_until_find_element_by_description(
        device, accessibility_id, timeout
    )


def convert_xpath_to_uiautomator_selector(xpath: str) -> str:
    """
    Convert simple xpath to UIAutomator2 selector

    Args:
        xpath: XPath string

    Returns:
        UIAutomator2 selector string
    """
    import re

    # Handle resource-id
    if "@resource-id=" in xpath:
        match = re.search(r'@resource-id="([^"]+)"', xpath)
        if match:
            return f'resourceId("{match.group(1)}")'

    # Handle text
    if "@text=" in xpath:
        match = re.search(r'@text="([^"]+)"', xpath)
        if match:
            return f'text("{match.group(1)}")'

    # Handle class name
    if "android.widget." in xpath:
        match = re.search(r"android\.widget\.(\w+)", xpath)
        if match:
            return f'className("android.widget.{match.group(1)}")'

    # Default: return as is (UIAutomator2 supports some xpath)
    return xpath
