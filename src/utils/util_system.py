"""
System Utility - Get PC identification from Windows system

Provides functions to retrieve:
- MachineGUID: Unique PC identifier from Windows registry
- Computer Name: Current PC hostname
"""

import platform
from typing import Tuple

# Only import winreg on Windows
try:
    import winreg
except ImportError:
    winreg = None


def get_machine_guid() -> str:
    """
    Get Windows MachineGUID from registry.

    Returns:
        str: MachineGUID string or "unknown-machine" if not available
    """
    if winreg is None:
        return "unknown-machine"

    try:
        with winreg.OpenKey(
            winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Cryptography"
        ) as key:
            return winreg.QueryValueEx(key, "MachineGuid")[0]
    except Exception as e:
        print(f"⚠️ Could not get MachineGUID: {e}")
        return "unknown-machine"


def get_computer_name() -> str:
    """
    Get computer/hostname name.

    Returns:
        str: Computer name or "unknown-pc" if not available
    """
    try:
        return platform.node()
    except Exception:
        return "unknown-pc"


def get_pc_ip() -> str:
    """
    Get the local IP address of the PC.

    Returns:
        str: IP address or "unknown-ip" if not available
    """
    import socket

    try:
        # Create a socket connection to get the local IP
        # This doesn't actually connect, just determines the route
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception as e:
        print(f"⚠️ Could not get IP address: {e}")
        return "unknown-ip"


def get_os_info() -> str:
    """
    Get operating system information.

    Returns:
        str: OS information string (e.g., "Windows 10")
    """
    try:
        return f"{platform.system()} {platform.release()}"
    except Exception:
        return "unknown-os"


def get_pc_info() -> Tuple[str, str]:
    """
    Get both PC_ID (MachineGUID) and PC_NAME (hostname).

    Returns:
        Tuple[str, str]: (machine_guid, computer_name)
    """
    return get_machine_guid(), get_computer_name()
