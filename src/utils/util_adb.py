from enum import Enum
import subprocess
from typing import Type


class IDeviceADB(Type):
    key: str
    name: str
    index: str
    status: str


class EStatusDeviceAdb(Enum):
    Online = "Online"
    Offline = "Offline"
    Unauthorized = "Unauthorized"


def list_devices() -> list[IDeviceADB]:
    DEVICE_ONLINE = "device"
    DEVICE_OFFLINE = "offline"
    DEVICE_UNAUTHORIZED = "unauthorized"

    try:
        result = subprocess.run(
            ["adb", "devices", "-l"], capture_output=True, text=True
        )
        lines = result.stdout.splitlines()

        # Skip the first line (List of devices attached)
        lines = lines[1:]

        devicesList: list[IDeviceADB] = []
        for index, line in enumerate(lines):
            if DEVICE_ONLINE in line:
                parts = line.split()
                device_key = parts[0]
                model_info = [part for part in parts if part.startswith("model:")]
                device_name = model_info[0].split(":")[1] if model_info else "Unknown"

                device_info: IDeviceADB = {
                    "key": device_key,
                    "name": device_name,
                    "index": index,
                    "status": EStatusDeviceAdb.Online.value,
                }
                devicesList.append(device_info)
            if DEVICE_OFFLINE in line:
                parts = line.split()
                device_key = parts[0]
                model_info = [part for part in parts if part.startswith("model:")]
                device_name = model_info[0].split(":")[1] if model_info else "Unknown"

                device_info: IDeviceADB = {
                    "key": device_key,
                    "name": device_name,
                    "index": index,
                    "status": EStatusDeviceAdb.Offline.value,
                }
                devicesList.append(device_info)
            if DEVICE_UNAUTHORIZED in line:
                parts = line.split()
                device_key = parts[0]
                model_info = [part for part in parts if part.startswith("model:")]
                device_name = model_info[0].split(":")[1] if model_info else "Unknown"

                device_info: IDeviceADB = {
                    "key": device_key,
                    "name": device_name,
                    "index": index,
                    "status": EStatusDeviceAdb.Unauthorized.value,
                }
                devicesList.append(device_info)

        return devicesList
    except FileNotFoundError:
        print(
            "Error: adb command not found. Please ensure that the Android SDK Platform Tools are installed and in your system's PATH."
        )
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
