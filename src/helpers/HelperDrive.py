"""
Helper Drive - UI Automator 2 Device Connection Helper
"""

import uiautomator2 as u2
import time
from typing import Optional


def connect_device(device_id: str = "3201912d6c0b2645") -> Optional[u2.Device]:
    """
    Connect to Android device using UI Automator 2

    Args:
        device_id: Android device ID/serial number

    Returns:
        UIAutomator2 Device instance if successful, None otherwise
    """
    try:
        # Connect to device by serial number
        print(f"Attempting to connect to device {device_id}...")
        device = u2.connect(device_id)

        # Verify connection by getting device info
        device_info = device.info

        # Check if device is actually connected
        if device_info and "currentPackageName" in device_info:
            print(f"✅ Connect device {device_id} success")
            print(
                f"   Device model: {device_info.get('productName', 'Unknown')} ({device_info.get('sdkInt', 'Unknown')} API)"
            )
            print(
                f"   Screen size: {device_info.get('displayWidth', 'Unknown')}x{device_info.get('displayHeight', 'Unknown')}"
            )
            return device
        else:
            print(f"❌ Failed to connect to device {device_id}")
            return None

    except Exception as e:
        print(f"❌ Error connecting to device {device_id}: {str(e)}")
        print("   Please ensure:")
        print("   1. USB debugging is enabled on the device")
        print("   2. Device is connected via USB")
        print("   3. ADB is properly installed")
        print("   4. Device authorization is accepted")
        print("   5. UIAutomator2 is installed (run: python -m uiautomator2 init)")
        return None


def connect_device_wifi(device_ip: str, port: int = 7912) -> Optional[u2.Device]:
    """
    Connect to Android device via WiFi using UI Automator 2

    Args:
        device_ip: IP address of the device
        port: Port number (default: 7912)

    Returns:
        UIAutomator2 Device instance if successful, None otherwise
    """
    try:
        # Connect to device via WiFi
        device_address = f"{device_ip}:{port}"
        device = u2.connect(device_address)

        # Verify connection
        device_info = device.info

        if device_info and "currentPackageName" in device_info:
            print(f"✅ Connect device via WiFi {device_address} success")
            print(
                f"   Device model: {device_info.get('productName', 'Unknown')} ({device_info.get('sdkInt', 'Unknown')} API)"
            )
            print(
                f"   Screen size: {device_info.get('displayWidth', 'Unknown')}x{device_info.get('displayHeight', 'Unknown')}"
            )
            return device
        else:
            print(f"❌ Failed to connect to device via WiFi {device_address}")
            return None

    except Exception as e:
        print(f"❌ Error connecting to device via WiFi {device_ip}: {str(e)}")
        print("   Please ensure:")
        print("   1. Device and PC are on the same network")
        print("   2. Wireless debugging is enabled on the device")
        print("   3. Port is properly forwarded")
        return None


def connect_first_available_device() -> Optional[u2.Device]:
    """
    Connect to the first available USB device

    Returns:
        UIAutomator2 Device instance if successful, None otherwise
    """
    try:
        # Connect to the first available device
        device = u2.connect()

        # Verify connection
        device_info = device.info

        if device_info and "currentPackageName" in device_info:
            device_id = device_info.get("serial", "Unknown")
            print(f"✅ Connect to first available device success")
            print(
                f"   Device model: {device_info.get('productName', 'Unknown')} ({device_info.get('sdkInt', 'Unknown')} API)"
            )
            print(
                f"   Screen size: {device_info.get('displayWidth', 'Unknown')}x{device_info.get('displayHeight', 'Unknown')}"
            )
            return device
        else:
            print("❌ No available device found")
            return None

    except Exception as e:
        print(f"❌ Error connecting to device: {str(e)}")
        return None


def init_uiautomator2(device_id: str = "3201912d6c0b2645") -> bool:
    """
    Manually install and initialize UIAutomator2 on device

    Args:
        device_id: Android device ID/serial number

    Returns:
        True if successful, False otherwise
    """
    try:
        print(f"Installing UIAutomator2 on device {device_id}...")

        # Use uiautomator2 init command directly
        import subprocess

        init_result = subprocess.run(
            ["python", "-m", "uiautomator2", "init", "--serial", device_id],
            capture_output=True,
            text=True,
        )

        if init_result.returncode == 0:
            print("✅ UIAutomator2 installed successfully")
            return True
        else:
            print(f"❌ Installation failed: {init_result.stderr}")
            return False

    except Exception as e:
        print(f"❌ Error installing UIAutomator2: {str(e)}")
        print("Please run manually: python -m uiautomator2 init")
        return False


# Convenience function for the specific device
def connect_to_3201912d6c0b2645() -> Optional[u2.Device]:
    """
    Connect to device with ID: 3201912d6c0b2645 and open Settings

    Returns:
        UIAutomator2 Device instance if successful, None otherwise
    """
    device = connect_device("3201912d6c0b2645")

    if device:
        # Open Settings app after successful connection
        try:
            print("\nOpening Settings app...")
            device.app_start("com.android.settings")
            time.sleep(2)
            print("✅ Settings app opened successfully")
        except Exception as e:
            print(f"❌ Failed to open Settings: {str(e)}")

    return device
