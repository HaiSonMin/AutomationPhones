"""
UI Automator 2 Actions - Click Operations
Converted from Appium to UI Automator 2
"""

import time
import subprocess
from typing import Optional, Dict, Any
from uiautomator2 import Device
from constants import ConstantPhone


def click_on_element_wait_by_selector(
    device: Device,
    selector: str,
    x_loc_replace: int = 540,
    y_loc_replace: int = None,
    timeout: int = 30,
    text_contains: str = None,
    is_check_hidden: bool = False,
) -> bool:
    """
    Click on element with wait using UI Automator 2 selector

    Args:
        device: UIAutomator2 Device instance
        selector: UIAutomator2 selector string
        x_loc_replace: Default x coordinate if element not found
        y_loc_replace: Default y coordinate if element not found
        timeout: Timeout in seconds
        text_contains: Text to filter elements
        is_check_hidden: Check if element becomes hidden after click

    Returns:
        True if click successful, False otherwise
    """
    time.sleep(1)

    # Build selector with text filter
    if text_contains:
        selector = f'{selector}[contains(@text, "{text_contains}")]'

    if y_loc_replace:
        print(f"Click on location of element x:{x_loc_replace}-y:{y_loc_replace}")
        try:
            while True:
                element = device(selector)
                if element.exists:
                    loc = element.info.get("bounds", {})
                    if loc:
                        x_loc = loc["left"] + 10
                        y_loc = loc["top"] + 10
                        click_on_loc(device=device, x_loc=x_loc, y_loc=y_loc)

                        if is_check_hidden:
                            try:
                                print("--------> Have check hidden:", selector)
                                if device(selector).wait_gone(timeout=3000):
                                    print("Element is hidden as expected")
                                    return True
                            except Exception as e:
                                print(f"Check hidden failed: {e}")
                                return False
                        else:
                            return True
                else:
                    # Element not found, click on default location
                    click_on_loc(
                        device=device, x_loc=x_loc_replace, y_loc=y_loc_replace
                    )
                    return True
        except Exception as e:
            print(f"Error clicking element: {e}")
            click_on_loc(device=device, x_loc=x_loc_replace, y_loc=y_loc_replace)
            return False
    else:
        try:
            while True:
                element = device(selector)
                if element.exists:
                    loc = element.info.get("bounds", {})
                    if loc:
                        x_loc = loc["left"] + 10
                        y_loc = loc["top"] + 10
                        click_on_loc(device=device, x_loc=x_loc, y_loc=y_loc)
                        return True
                time.sleep(0.5)
        except Exception as e:
            print(f"Error in click loop: {e}")
            return False


def click_on_loc(device: Device, x_loc: int, y_loc: int) -> bool:
    """
    Click on specific coordinates using UI Automator 2

    Args:
        device: UIAutomator2 Device instance
        x_loc: X coordinate
        y_loc: Y coordinate

    Returns:
        True if click successful
    """
    try:
        device.click(x_loc, y_loc)
        print(f"Clicked at coordinates: x={x_loc}, y={y_loc}")
        return True
    except Exception as e:
        print(f"Failed to click at coordinates: {e}")
        return False


def click_on_element_by_resource_id(
    device: Device,
    resource_id: str,
    timeout: int = 10,
) -> bool:
    """
    Click element by resource ID

    Args:
        device: UIAutomator2 Device instance
        resource_id: Android resource ID
        timeout: Timeout in seconds

    Returns:
        True if click successful
    """
    try:
        selector = f'resourceId("{resource_id}")'
        element = device(selector)
        if element.wait(timeout=timeout * 1000):
            element.click()
            return True
        return False
    except Exception as e:
        print(f"Failed to click by resource ID: {e}")
        return False


def click_on_element_by_text(
    device: Device,
    text: str,
    timeout: int = 10,
    contains: bool = False,
) -> bool:
    """
    Click element by text

    Args:
        device: UIAutomator2 Device instance
        text: Text to search for
        timeout: Timeout in seconds
        contains: If True, search for text containing the string

    Returns:
        True if click successful
    """
    try:
        if contains:
            selector = f'textContains("{text}")'
        else:
            selector = f'text("{text}")'

        element = device(selector)
        if element.wait(timeout=timeout * 1000):
            element.click()
            return True
        return False
    except Exception as e:
        print(f"Failed to click by text: {e}")
        return False


def click_on_element_by_description(
    device: Device,
    description: str,
    timeout: int = 10,
    contains: bool = False,
) -> bool:
    """
    Click element by content description

    Args:
        device: UIAutomator2 Device instance
        description: Content description
        timeout: Timeout in seconds
        contains: If True, search for description containing the string

    Returns:
        True if click successful
    """
    try:
        if contains:
            selector = f'descriptionContains("{description}")'
        else:
            selector = f'description("{description}")'

        element = device(selector)
        if element.wait(timeout=timeout * 1000):
            element.click()
            return True
        return False
    except Exception as e:
        print(f"Failed to click by description: {e}")
        return False


def long_click_on_element(
    device: Device,
    selector: str,
    duration: float = 1.0,
    timeout: int = 10,
) -> bool:
    """
    Long click on element

    Args:
        device: UIAutomator2 Device instance
        selector: UIAutomator2 selector
        duration: Long click duration in seconds
        timeout: Timeout in seconds

    Returns:
        True if long click successful
    """
    try:
        element = device(selector)
        if element.wait(timeout=timeout * 1000):
            element.long_click(duration=duration)
            return True
        return False
    except Exception as e:
        print(f"Failed to long click: {e}")
        return False


def double_click_on_element(
    device: Device,
    selector: str,
    timeout: int = 10,
) -> bool:
    """
    Double click on element

    Args:
        device: UIAutomator2 Device instance
        selector: UIAutomator2 selector
        timeout: Timeout in seconds

    Returns:
        True if double click successful
    """
    try:
        element = device(selector)
        if element.wait(timeout=timeout * 1000):
            element.double_click()
            return True
        return False
    except Exception as e:
        print(f"Failed to double click: {e}")
        return False


def click_and_drag(
    device: Device,
    start_selector: str,
    end_x: int,
    end_y: int,
    duration: float = 1.0,
    timeout: int = 10,
) -> bool:
    """
    Click and drag from element to coordinates

    Args:
        device: UIAutomator2 Device instance
        start_selector: Starting element selector
        end_x: End X coordinate
        end_y: End Y coordinate
        duration: Drag duration in seconds
        timeout: Timeout in seconds

    Returns:
        True if drag successful
    """
    try:
        element = device(start_selector)
        if element.wait(timeout=timeout * 1000):
            bounds = element.info.get("bounds", {})
            start_x = bounds["left"] + (bounds["right"] - bounds["left"]) // 2
            start_y = bounds["top"] + (bounds["bottom"] - bounds["top"]) // 2

            device.drag(start_x, start_y, end_x, end_y, duration=duration)
            return True
        return False
    except Exception as e:
        print(f"Failed to click and drag: {e}")
        return False


# Helper functions for backward compatibility
def click_on_element_wait_by_xpath(
    device: Device,
    xpath: str,
    x_loc_replace: int = 540,
    y_loc_replace: int = None,
    timeout: int = 30,
    text_contains: str = None,
    is_check_hidden: bool = False,
) -> bool:
    """
    Wrapper for backward compatibility with xpath
    Converts xpath to UIAutomator2 selector
    """
    # Convert xpath to UIAutomator2 selector
    selector = convert_xpath_to_uiautomator_selector(xpath)
    return click_on_element_wait_by_selector(
        device=device,
        selector=selector,
        x_loc_replace=x_loc_replace,
        y_loc_replace=y_loc_replace,
        timeout=timeout,
        text_contains=text_contains,
        is_check_hidden=is_check_hidden,
    )


def convert_xpath_to_uiautomator_selector(xpath: str) -> str:
    """
    Convert simple xpath to UIAutomator2 selector

    Args:
        xpath: XPath string

    Returns:
        UIAutomator2 selector string
    """
    # This is a simplified converter for common xpaths
    # You may need to expand this based on your specific xpaths

    # Handle resource-id
    if "@resource-id=" in xpath:
        import re

        match = re.search(r'@resource-id="([^"]+)"', xpath)
        if match:
            return f'resourceId("{match.group(1)}")'

    # Handle text
    if "@text=" in xpath:
        import re

        match = re.search(r'@text="([^"]+)"', xpath)
        if match:
            return f'text("{match.group(1)}")'

    # Handle class name
    if "android.widget." in xpath:
        import re

        match = re.search(r"android\.widget\.(\w+)", xpath)
        if match:
            return f'className("android.widget.{match.group(1)}")'

    # Default: return as is (UIAutomator2 supports some xpath)
    return xpath
