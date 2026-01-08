"""
UI Automator 2 Actions - Scroll Operations
Converted from Appium to UI Automator 2
"""

import time
from typing import Optional
from uiautomator2 import Device
from constants import ConstantPhone


def scroll_vertical_until_find_element_by_selector(
    device: Device,
    selector: str,
    y_start: int = 1800,
    y_end: int = 300,
    x_loc: int = None,
    timeout: int = 5,
    max_scroll_find: int = 5,
    duration: float = 0.5,
) -> bool:
    """
    Scroll vertically until element is found

    Args:
        device: UIAutomator2 Device instance
        selector: UIAutomator2 selector string
        y_start: Starting Y coordinate for scroll
        y_end: Ending Y coordinate for scroll
        x_loc: X coordinate for scroll (center of screen if None)
        timeout: Timeout for checking element existence
        max_scroll_find: Maximum number of scroll attempts
        duration: Scroll duration in seconds

    Returns:
        True if element found, False otherwise
    """
    time.sleep(1)
    count_scroll_find = 0

    # Default to center of screen width
    if x_loc is None:
        x_loc = ConstantPhone.CONST_WIDTH_PHONE // 2

    while count_scroll_find < max_scroll_find:
        try:
            element = device(selector)
            if element.exists:
                print(f"Element found after {count_scroll_find} scrolls")
                return True

            # Element not found, scroll
            scroll_by_vertical(
                device=device,
                y_start=y_start,
                y_end=y_end,
                x_loc=x_loc,
                number_scroll=1,
                duration=duration,
            )
            count_scroll_find += 1
            time.sleep(0.5)
        except Exception as e:
            print(f"Error during scroll: {e}")
            count_scroll_find += 1
            time.sleep(1)

    print(f"Element not found after {max_scroll_find} scrolls")
    return False


def scroll_horizontal_until_find_element_by_selector(
    device: Device,
    selector: str,
    y_loc: int,
    x_start: int,
    x_end: int,
    timeout: int = 5,
    max_scroll_find: int = 5,
    duration: float = 0.5,
) -> bool:
    """
    Scroll horizontally until element is found

    Args:
        device: UIAutomator2 Device instance
        selector: UIAutomator2 selector string
        y_loc: Y coordinate for scroll
        x_start: Starting X coordinate for scroll
        x_end: Ending X coordinate for scroll
        timeout: Timeout for checking element existence
        max_scroll_find: Maximum number of scroll attempts
        duration: Scroll duration in seconds

    Returns:
        True if element found, False otherwise
    """
    time.sleep(1)
    count_scroll_find = 0

    while count_scroll_find < max_scroll_find:
        try:
            element = device(selector)
            if element.exists:
                print(f"Element found after {count_scroll_find} scrolls")
                return True

            # Element not found, scroll
            scroll_by_horizontal(
                device=device,
                x_start=x_start,
                x_end=x_end,
                y_loc=y_loc,
                number_scroll=1,
                duration=duration,
            )
            count_scroll_find += 1
            time.sleep(0.5)
        except Exception as e:
            print(f"Error during scroll: {e}")
            count_scroll_find += 1
            time.sleep(1)

    print(f"Element not found after {max_scroll_find} scrolls")
    return False


def scroll_by_vertical(
    device: Device,
    y_start: int = 1800,
    y_end: int = 200,
    x_loc: int = None,
    number_scroll: int = 1,
    duration: float = 0.5,
) -> bool:
    """
    Scroll vertically

    Args:
        device: UIAutomator2 Device instance
        y_start: Starting Y coordinate
        y_end: Ending Y coordinate
        x_loc: X coordinate (center of screen if None)
        number_scroll: Number of times to scroll
        duration: Scroll duration in seconds

    Returns:
        True if successful
    """
    time.sleep(1)
    count_scroll = 0

    # Default to center of screen width
    if x_loc is None:
        x_loc = ConstantPhone.CONST_WIDTH_PHONE // 2

    while count_scroll < number_scroll:
        try:
            print(f"Scroll vertical from ({x_loc}, {y_start}) to ({x_loc}, {y_end})")
            device.swipe(x_loc, y_start, x_loc, y_end, duration=duration)
            time.sleep(1)
            count_scroll += 1
        except Exception as e:
            print(f"Error during vertical scroll: {e}")
            time.sleep(2)

    return True


def scroll_by_horizontal(
    device: Device,
    x_start: int,
    x_end: int,
    y_loc: int = None,
    number_scroll: int = 1,
    duration: float = 0.5,
) -> bool:
    """
    Scroll horizontally

    Args:
        device: UIAutomator2 Device instance
        x_start: Starting X coordinate
        x_end: Ending X coordinate
        y_loc: Y coordinate (center of screen height if None)
        number_scroll: Number of times to scroll
        duration: Scroll duration in seconds

    Returns:
        True if successful
    """
    time.sleep(1)
    count_scroll = 0

    # Default to center of screen height
    if y_loc is None:
        y_loc = ConstantPhone.CONST_HEIGH_PHONE // 2

    while count_scroll < number_scroll:
        try:
            print(f"Scroll horizontal from ({x_start}, {y_loc}) to ({x_end}, {y_loc})")
            device.swipe(x_start, y_loc, x_end, y_loc, duration=duration)
            time.sleep(1)
            count_scroll += 1
        except Exception as e:
            print(f"Error during horizontal scroll: {e}")
            time.sleep(2)

    return True


def scroll_to_top(device: Device) -> bool:
    """
    Scroll to the top of the screen

    Args:
        device: UIAutomator2 Device instance

    Returns:
        True if successful
    """
    try:
        # Scroll up multiple times to reach top
        for _ in range(5):
            device.swipe(
                ConstantPhone.CONST_WIDTH_PHONE // 2,
                300,
                ConstantPhone.CONST_WIDTH_PHONE // 2,
                1800,
                0.3,
            )
            time.sleep(0.5)
        return True
    except Exception as e:
        print(f"Failed to scroll to top: {e}")
        return False


def scroll_to_bottom(device: Device) -> bool:
    """
    Scroll to the bottom of the screen

    Args:
        device: UIAutomator2 Device instance

    Returns:
        True if successful
    """
    try:
        # Scroll down multiple times to reach bottom
        for _ in range(5):
            device.swipe(
                ConstantPhone.CONST_WIDTH_PHONE // 2,
                1800,
                ConstantPhone.CONST_WIDTH_PHONE // 2,
                300,
                0.3,
            )
            time.sleep(0.5)
        return True
    except Exception as e:
        print(f"Failed to scroll to bottom: {e}")
        return False


def scroll_to_element(
    device: Device,
    selector: str,
    direction: str = "down",
    max_swipes: int = 10,
) -> bool:
    """
    Scroll to a specific element

    Args:
        device: UIAutomator2 Device instance
        selector: UIAutomator2 selector string
        direction: Scroll direction ("up" or "down")
        max_swipes: Maximum number of swipes

    Returns:
        True if element found, False otherwise
    """
    try:
        if direction.lower() == "up":
            # Scroll up
            for _ in range(max_swipes):
                element = device(selector)
                if element.exists:
                    return True
                device.swipe(
                    ConstantPhone.CONST_WIDTH_PHONE // 2,
                    300,
                    ConstantPhone.CONST_WIDTH_PHONE // 2,
                    1800,
                    0.5,
                )
                time.sleep(0.5)
        else:
            # Scroll down
            for _ in range(max_swipes):
                element = device(selector)
                if element.exists:
                    return True
                device.swipe(
                    ConstantPhone.CONST_WIDTH_PHONE // 2,
                    1800,
                    ConstantPhone.CONST_WIDTH_PHONE // 2,
                    300,
                    0.5,
                )
                time.sleep(0.5)

        return False
    except Exception as e:
        print(f"Failed to scroll to element: {e}")
        return False


def scroll_in_view(
    device: Device,
    container_selector: str,
    direction: str = "down",
    max_swipes: int = 10,
) -> bool:
    """
    Scroll within a specific view/container

    Args:
        device: UIAutomator2 Device instance
        container_selector: Selector for the scrollable container
        direction: Scroll direction ("up", "down", "left", "right")
        max_swipes: Maximum number of swipes

    Returns:
        True if successful
    """
    try:
        container = device(container_selector)
        if not container.exists:
            print("Container not found")
            return False

        # Get container bounds
        bounds = container.info.get("bounds", {})
        if not bounds:
            print("Could not get container bounds")
            return False

        center_x = (bounds["left"] + bounds["right"]) // 2
        center_y = (bounds["top"] + bounds["bottom"]) // 2

        # Calculate swipe coordinates based on direction
        if direction.lower() == "down":
            start_y = center_y + (bounds["bottom"] - bounds["top"]) // 3
            end_y = center_y - (bounds["bottom"] - bounds["top"]) // 3
            for _ in range(max_swipes):
                device.swipe(center_x, start_y, center_x, end_y, 0.5)
                time.sleep(0.5)
        elif direction.lower() == "up":
            start_y = center_y - (bounds["bottom"] - bounds["top"]) // 3
            end_y = center_y + (bounds["bottom"] - bounds["top"]) // 3
            for _ in range(max_swipes):
                device.swipe(center_x, start_y, center_x, end_y, 0.5)
                time.sleep(0.5)
        elif direction.lower() == "right":
            start_x = center_x - (bounds["right"] - bounds["left"]) // 3
            end_x = center_x + (bounds["right"] - bounds["left"]) // 3
            for _ in range(max_swipes):
                device.swipe(start_x, center_y, end_x, center_y, 0.5)
                time.sleep(0.5)
        elif direction.lower() == "left":
            start_x = center_x + (bounds["right"] - bounds["left"]) // 3
            end_x = center_x - (bounds["right"] - bounds["left"]) // 3
            for _ in range(max_swipes):
                device.swipe(start_x, center_y, end_x, center_y, 0.5)
                time.sleep(0.5)

        return True
    except Exception as e:
        print(f"Failed to scroll in view: {e}")
        return False


def fling_up(device: Device) -> bool:
    """
    Perform a fling gesture (fast swipe) upward

    Args:
        device: UIAutomator2 Device instance

    Returns:
        True if successful
    """
    try:
        device.fling_up()
        return True
    except Exception as e:
        print(f"Failed to fling up: {e}")
        return False


def fling_down(device: Device) -> bool:
    """
    Perform a fling gesture (fast swipe) downward

    Args:
        device: UIAutomator2 Device instance

    Returns:
        True if successful
    """
    try:
        device.fling_down()
        return True
    except Exception as e:
        print(f"Failed to fling down: {e}")
        return False


def fling_left(device: Device) -> bool:
    """
    Perform a fling gesture (fast swipe) to the left

    Args:
        device: UIAutomator2 Device instance

    Returns:
        True if successful
    """
    try:
        device.fling_left()
        return True
    except Exception as e:
        print(f"Failed to fling left: {e}")
        return False


def fling_right(device: Device) -> bool:
    """
    Perform a fling gesture (fast swipe) to the right

    Args:
        device: UIAutomator2 Device instance

    Returns:
        True if successful
    """
    try:
        device.fling_right()
        return True
    except Exception as e:
        print(f"Failed to fling right: {e}")
        return False


# Helper functions for backward compatibility
def scroll_vertical_until_find_element_by_xpath(
    device: Device,
    xpath: str,
    y_start: int = 1800,
    y_end: int = 300,
    x_loc: int = None,
    timeout: int = 5,
    max_scroll_find: int = 5,
    duration: float = 0.5,
) -> bool:
    """Wrapper for backward compatibility"""
    selector = convert_xpath_to_uiautomator_selector(xpath)
    return scroll_vertical_until_find_element_by_selector(
        device, selector, y_start, y_end, x_loc, timeout, max_scroll_find, duration
    )


def scroll_horizontal_until_find_element_by_xpath(
    device: Device,
    xpath: str,
    y_loc: int,
    x_start: int,
    x_end: int,
    timeout: int = 5,
    max_scroll_find: int = 5,
    duration: float = 0.5,
) -> bool:
    """Wrapper for backward compatibility"""
    selector = convert_xpath_to_uiautomator_selector(xpath)
    return scroll_horizontal_until_find_element_by_selector(
        device, selector, y_loc, x_start, x_end, timeout, max_scroll_find, duration
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
