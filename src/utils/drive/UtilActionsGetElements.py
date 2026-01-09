"""
UI Automator 2 Actions - Get Elements Operations
Converted from Appium to UI Automator 2
"""

import os
import time
import cv2
import numpy as np
from typing import List, Optional, Dict
from uiautomator2 import Device


def check_element_disable_by_selector(
    device: Device, selector: str, time_get_check: int = 6
) -> bool:
    """
    Check if element is disabled/doesn't exist

    Args:
        device: UIAutomator2 Device instance
        selector: UIAutomator2 selector string
        time_get_check: Number of times to check

    Returns:
        True if element is disabled/doesn't exist, False if enabled
    """
    count_time_get_check = 0
    while True:
        try:
            if count_time_get_check == time_get_check:
                return False
            element = device(selector)
            if element.exists:
                time.sleep(1)
                count_time_get_check += 1
            else:
                return True
        except:
            return True


def get_multi_elements_by_selector(
    device: Device, selector: str, timeout: int = 10
) -> List:
    """
    Get multiple elements by selector

    Args:
        device: UIAutomator2 Device instance
        selector: UIAutomator2 selector string
        timeout: Timeout in seconds

    Returns:
        List of UIAutomator2 elements
    """
    time.sleep(1)
    elements = device(selector)
    return elements.all() if elements.exists else []


def get_multi_elements_wait_by_selector(
    device: Device, selector: str, timeout: int = 60
) -> List:
    """
    Get multiple elements with wait

    Args:
        device: UIAutomator2 Device instance
        selector: UIAutomator2 selector string
        timeout: Timeout in seconds

    Returns:
        List of UIAutomator2 elements
    """
    time.sleep(1)
    elements = device(selector)
    if elements.wait(timeout=timeout * 1000):
        return elements.all()
    return []


def get_element_by_selector(
    device: Device,
    selector: str,
    text_contains: str = None,
    text_start_with: str = None,
    timeout: int = 5,
):
    """
    Get element by selector

    Args:
        device: UIAutomator2 Device instance
        selector: UIAutomator2 selector string
        text_contains: Filter by text contains
        text_start_with: Filter by text starts with
        timeout: Timeout in seconds

    Returns:
        UIAutomator2 element or None
    """
    selector_transform = selector

    if text_start_with:
        selector_transform = (
            f'{selector_transform}[starts-with(@text, "{text_start_with}")]'
        )
    if text_contains:
        selector_transform = f'{selector_transform}[contains(@text, "{text_contains}")]'

    time.sleep(1)
    element = device(selector_transform)
    return element if element.exists else None


def get_element_by_resource_id(device: Device, resource_id: str, timeout: int = 5):
    """
    Get element by resource ID

    Args:
        device: UIAutomator2 Device instance
        resource_id: Android resource ID
        timeout: Timeout in seconds

    Returns:
        UIAutomator2 element or None
    """
    time.sleep(1)
    selector = f'resourceId("{resource_id}")'
    element = device(selector)
    return element if element.exists else None


def get_element_by_class_name(device: Device, class_name: str, timeout: int = 5):
    """
    Get element by class name

    Args:
        device: UIAutomator2 Device instance
        class_name: Android class name
        timeout: Timeout in seconds

    Returns:
        UIAutomator2 element or None
    """
    time.sleep(1)
    selector = f'className("{class_name}")'
    element = device(selector)
    return element if element.exists else None


def get_element_by_text(
    device: Device, text: str, timeout: int = 5, contains: bool = False
):
    """
    Get element by text

    Args:
        device: UIAutomator2 Device instance
        text: Text to search
        timeout: Timeout in seconds
        contains: If True, search for text containing the string

    Returns:
        UIAutomator2 element or None
    """
    time.sleep(1)
    if contains:
        selector = f'textContains("{text}")'
    else:
        selector = f'text("{text}")'

    element = device(selector)
    return element if element.exists else None


def get_element_by_description(
    device: Device, description: str, timeout: int = 5, contains: bool = False
):
    """
    Get element by content description

    Args:
        device: UIAutomator2 Device instance
        description: Content description
        timeout: Timeout in seconds
        contains: If True, search for description containing the string

    Returns:
        UIAutomator2 element or None
    """
    time.sleep(1)
    if contains:
        selector = f'descriptionContains("{description}")'
    else:
        selector = f'description("{description}")'

    element = device(selector)
    return element if element.exists else None


def get_element_wait_by_selector(
    device: Device,
    selector: str,
    text_contains: str = None,
    text_start_with: str = None,
    timeout: int = 60,
):
    """
    Get element with wait

    Args:
        device: UIAutomator2 Device instance
        selector: UIAutomator2 selector string
        text_contains: Filter by text contains
        text_start_with: Filter by text starts with
        timeout: Timeout in seconds

    Returns:
        UIAutomator2 element or None
    """
    time.sleep(1)

    selector_transform = selector
    if text_start_with:
        selector_transform = (
            f'{selector_transform}[starts-with(@text, "{text_start_with}")]'
        )
    if text_contains:
        selector_transform = f'{selector_transform}[contains(@text, "{text_contains}")]'

    element = device(selector_transform)
    if element.wait(timeout=timeout * 1000):
        return element
    return None


def get_element_wait_by_resource_id(
    device: Device, resource_id: str, timeout: int = 60
):
    """
    Get element by resource ID with wait

    Args:
        device: UIAutomator2 Device instance
        resource_id: Android resource ID
        timeout: Timeout in seconds

    Returns:
        UIAutomator2 element or None
    """
    time.sleep(1)
    selector = f'resourceId("{resource_id}")'
    element = device(selector)
    if element.wait(timeout=timeout * 1000):
        return element
    return None


def get_element_wait_by_class_name(device: Device, class_name: str, timeout: int = 60):
    """
    Get element by class name with wait

    Args:
        device: UIAutomator2 Device instance
        class_name: Android class name
        timeout: Timeout in seconds

    Returns:
        UIAutomator2 element or None
    """
    time.sleep(1)
    selector = f'className("{class_name}")'
    element = device(selector)
    if element.wait(timeout=timeout * 1000):
        return element
    return None


def get_element_wait_by_text(
    device: Device, text: str, timeout: int = 60, contains: bool = False
):
    """
    Get element by text with wait

    Args:
        device: UIAutomator2 Device instance
        text: Text to search
        timeout: Timeout in seconds
        contains: If True, search for text containing the string

    Returns:
        UIAutomator2 element or None
    """
    time.sleep(1)
    if contains:
        selector = f'textContains("{text}")'
    else:
        selector = f'text("{text}")'

    element = device(selector)
    if element.wait(timeout=timeout * 1000):
        return element
    return None


def get_element_wait_by_description(
    device: Device, description: str, timeout: int = 60, contains: bool = False
):
    """
    Get element by content description with wait

    Args:
        device: UIAutomator2 Device instance
        description: Content description
        timeout: Timeout in seconds
        contains: If True, search for description containing the string

    Returns:
        UIAutomator2 element or None
    """
    time.sleep(1)
    if contains:
        selector = f'descriptionContains("{description}")'
    else:
        selector = f'description("{description}")'

    element = device(selector)
    if element.wait(timeout=timeout * 1000):
        return element
    return None


def get_loc_element_by_image(
    device: Device,
    image_path: str,
    x_start: int,
    y_start: int,
    x_end: int,
    y_end: int,
    dir_name: str = "images-compare",
    image_name: str = "image_compare.PNG",
) -> Optional[Dict[str, int]]:
    """
    Get element location by image matching

    Args:
        device: UIAutomator2 Device instance
        image_path: Path to reference image
        x_start: X coordinate start of search area
        y_start: Y coordinate start of search area
        x_end: X coordinate end of search area
        y_end: Y coordinate end of search area
        dir_name: Directory name for saving comparison images
        image_name: Name for saving comparison image

    Returns:
        Dictionary with x_loc and y_loc if found, None otherwise
    """
    current_directory = os.getcwd()

    # Read the reference image
    reference_image = cv2.imread(image_path)
    if reference_image is None:
        print(f"Error: Could not read reference image at {image_path}")
        return None

    # Take a screenshot of the current screen
    screenshot = device.screenshot()

    # Convert PIL Image to numpy array for OpenCV
    screenshot_np = np.array(screenshot)

    # Convert RGB to BGR for OpenCV
    screenshot_bgr = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)

    # Crop the screenshot to the specified area
    cropped_image = screenshot_bgr[y_start:y_end, x_start:x_end]

    # Define the directory path
    directory_path = f"{current_directory}\\app-auto\\images\\{dir_name}"

    # Create the directory if it doesn't exist
    os.makedirs(directory_path, exist_ok=True)

    # Save the cropped image
    cropped_path = os.path.join(directory_path, image_name)
    cv2.imwrite(cropped_path, cropped_image)

    # Match the reference image within the screenshot
    result = cv2.matchTemplate(cropped_image, reference_image, cv2.TM_CCOEFF_NORMED)

    # Get the location of the matched element
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    print(f"min_val: {min_val}")
    print(f"max_val: {max_val}")
    print(f"min_loc: {min_loc}")
    print(f"max_loc: {max_loc}")

    # Check if match is good enough (threshold can be adjusted)
    threshold = 0.8
    if max_val < threshold:
        print(f"No good match found. Max correlation: {max_val}")
        return None

    top_left = max_loc
    height, width, _ = reference_image.shape
    bottom_right = (top_left[0] + width, top_left[1] + height)

    # Calculate the center of the element (relative to cropped area)
    center_x = top_left[0] + width // 2
    center_y = top_left[1] + height // 2

    # Convert to absolute coordinates
    abs_x = x_start + center_x
    abs_y = y_start + center_y

    return {"x_loc": abs_x, "y_loc": abs_y}


def push_file_to_device(device: Device, file_path: str, device_path: str) -> bool:
    """
    Push file to device using UIAutomator2

    Args:
        device: UIAutomator2 Device instance
        file_path: Local file path
        device_path: Destination path on device

    Returns:
        True if successful, False otherwise
    """
    try:
        # Push file using UIAutomator2
        device.push(file_path, device_path)
        print(f"File pushed successfully: {file_path} -> {device_path}")
        return True
    except Exception as e:
        print(f"Failed to push file: {e}")
        return False


def pull_file_from_device(device: Device, device_path: str, local_path: str) -> bool:
    """
    Pull file from device using UIAutomator2

    Args:
        device: UIAutomator2 Device instance
        device_path: Path on device
        local_path: Local destination path

    Returns:
        True if successful, False otherwise
    """
    try:
        # Pull file using UIAutomator2
        device.pull(device_path, local_path)
        print(f"File pulled successfully: {device_path} -> {local_path}")
        return True
    except Exception as e:
        print(f"Failed to pull file: {e}")
        return False


# Helper functions for backward compatibility
def check_element_disable_by_xpath(
    device: Device, xpath: str, time_get_check: int = 6
) -> bool:
    """Wrapper for backward compatibility"""
    selector = convert_xpath_to_uiautomator_selector(xpath)
    return check_element_disable_by_selector(device, selector, time_get_check)


def get_multi_elements_by_xpath(device: Device, xpath: str, timeout: int = 10) -> List:
    """Wrapper for backward compatibility"""
    selector = convert_xpath_to_uiautomator_selector(xpath)
    return get_multi_elements_by_selector(device, selector, timeout)


def get_multi_elements_wait_by_xpath(
    device: Device, xpath: str, timeout: int = 60
) -> List:
    """Wrapper for backward compatibility"""
    selector = convert_xpath_to_uiautomator_selector(xpath)
    return get_multi_elements_wait_by_selector(device, selector, timeout)


def get_element_by_xpath(
    device: Device,
    xpath: str,
    text_contains: str = None,
    text_start_with: str = None,
    timeout: int = 5,
):
    """Wrapper for backward compatibility"""
    selector = convert_xpath_to_uiautomator_selector(xpath)
    return get_element_by_selector(
        device, selector, text_contains, text_start_with, timeout
    )


def get_element_wait_by_xpath(
    device: Device,
    xpath: str,
    text_contains: str = None,
    text_start_with: str = None,
    timeout: int = 60,
):
    """Wrapper for backward compatibility"""
    selector = convert_xpath_to_uiautomator_selector(xpath)
    return get_element_wait_by_selector(
        device, selector, text_contains, text_start_with, timeout
    )


def get_element_by_id(device: Device, id: str, timeout: int = 5):
    """Wrapper for backward compatibility - maps to resource ID"""
    return get_element_by_resource_id(device, id, timeout)


def get_element_wait_by_id(device: Device, id: str, timeout: int = 60):
    """Wrapper for backward compatibility - maps to resource ID"""
    return get_element_wait_by_resource_id(device, id, timeout)


def get_element_by_accessibility_id(
    device: Device, accessibility_id: str, timeout: int = 5
):
    """Wrapper for backward compatibility - maps to description"""
    return get_element_by_description(device, accessibility_id, timeout)


def get_element_wait_by_accessibility_id(
    device: Device, accessibility_id: str, timeout: int = 60
):
    """Wrapper for backward compatibility - maps to description"""
    return get_element_wait_by_description(device, accessibility_id, timeout)


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

    # Handle accessibility_id (content-desc)
    if "@content-desc=" in xpath:
        match = re.search(r'@content-desc="([^"]+)"', xpath)
        if match:
            return f'description("{match.group(1)}")'

    # Default: return as is (UIAutomator2 supports some xpath)
    return xpath
