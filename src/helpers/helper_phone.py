import time
import requests, os, shutil, subprocess, uuid

from constants import constant_package_application
from constants.constant_permission import (
    PERMISSION_CANVA,
    PERMISSION_PLAY_STORE,
    PERMISSION_CHROME,
    PERMISSION_CLONE_APP_PRO,
    PERMISSION_GMAIL,
    PERMISSION_INSTAGRAM,
)
from enums.EAppName import EAppName
from enums.EAppNamePermission import EAppNamePermission
from enums.ESocials import ESocials

FILE_FOLDER_LOCAL = "files"
FOLDER_DOWNLOAD_PHONE_STORE = "/sdcard/Download/"
FOLDER_IMAGES_PHONE_STORE = "/sdcard/Images/"
FOLDER_CANVA_PHONE_STORE = "/sdcard/Canva/"


def create_folder_on_device(deviceKey: str, folderPath: str) -> None:
    # Command to create the directory on the device
    command = f"adb -s {deviceKey} shell mkdir -p {folderPath}"
    process = subprocess.run(command, shell=True, capture_output=True)
    if process.returncode == 0:
        print(f"Successfully created directory {folderPath} on the device")
    else:
        print(
            f"Failed to create directory {folderPath}. Error: {process.stderr.decode()}"
        )


def reload_media_on_device(deviceKey: str, folderPath: str) -> None:
    print("Command to broadcast a media scan intent")
    command = f"adb -s {deviceKey} shell am broadcast -a android.intent.action.MEDIA_SCANNER_SCAN_FILE -d file://{folderPath}"
    process = subprocess.run(command, shell=True, capture_output=True)
    if process.returncode == 0:
        print(f"Media scan broadcast successfully for {folderPath}")
    else:
        print(f"Failed to broadcast media scan. Error: {process.stderr.decode()}")


def remove_files_in_folder_phone(
    deviceKey: str, folderPath: str = FOLDER_DOWNLOAD_PHONE_STORE
) -> None:
    # Command to remove all files in the directory on the device
    command = f"adb -s {deviceKey} shell rm -f {folderPath}/*"
    process = subprocess.run(command, shell=True, capture_output=True)
    if process.returncode == 0:
        print(f"Successfully removed all item in directory {folderPath}")
    else:
        print(
            f"Failed to remove item in directory {folderPath}. Error: {process.stderr.decode()}"
        )

    reload_media_on_device(deviceKey=deviceKey, folderPath=folderPath)


def push_files_to_device_download(file_urls: list[str], deviceKey: str) -> None:

    print("Remove all file in pc")
    remove_all_files_in_folder_local(deviceKey=deviceKey)
    time.sleep(1)

    print("Remove all files in folder download in phone")
    remove_files_in_folder_phone(
        deviceKey=deviceKey, folderPath=FOLDER_DOWNLOAD_PHONE_STORE
    )
    print("Remove all files in folder images in phone")
    remove_files_in_folder_phone(
        deviceKey=deviceKey, folderPath=FOLDER_IMAGES_PHONE_STORE
    )
    time.sleep(1)
    print("Remove all files in folder canva in phone")
    remove_files_in_folder_phone(
        deviceKey=deviceKey, folderPath=FOLDER_CANVA_PHONE_STORE
    )
    time.sleep(1)

    print("Create folder on phone")
    create_folder_on_device(deviceKey=deviceKey, folderPath=FOLDER_DOWNLOAD_PHONE_STORE)
    time.sleep(1)

    folderFiles = f"{FILE_FOLDER_LOCAL}\\{deviceKey}"

    print("Create the folder if it doesn't exist")
    os.makedirs(folderFiles, exist_ok=True)

    # print("file_urls::::", file_urls)

    for index, file_url in enumerate(file_urls):
        save_file_to_folder(
            folderPath=folderFiles,
            file_url=file_url,
            deviceKey=deviceKey,
            index=index + 3,
        )
        time.sleep(1)

    listFilesName = os.listdir(folderFiles)
    sortedListFilesName = sorted(listFilesName)

    try:
        for filename in sortedListFilesName:
            filePath = os.path.join(folderFiles, filename)

            print("filePath:::", filePath)

            if os.path.isfile(filePath):
                # Use adb push command to transfer the file to the device
                command = (
                    f"adb -s {deviceKey} push {filePath} {FOLDER_DOWNLOAD_PHONE_STORE}"
                )
                process = subprocess.run(command, shell=True, capture_output=True)
                if process.returncode == 0:
                    print(
                        f"Successfully pushed {filename} to device at {FOLDER_DOWNLOAD_PHONE_STORE}"
                    )
                else:
                    print(
                        f"Failed to push {filename}. Error: {process.stderr.decode()}"
                    )
    except Exception as e:
        print("e:::", e)
        pass
    finally:
        time.sleep(1)
        reload_media_on_device(
            deviceKey=deviceKey, folderPath=FOLDER_DOWNLOAD_PHONE_STORE
        )


def save_file_to_folder(
    folderPath: str, file_url: str, deviceKey: str, index: int
) -> None:

    # print("Create the folder if it doesn't exist")
    # os.makedirs(folderPath, exist_ok=True)

    file_path = None
    if ".mp4" in file_url:
        file_path = os.path.join(folderPath, f"video_{uuid.uuid4()}.mp4")
    # else ".jpg" in file_url or ".png" in file_url:
    #     file_path = os.path.join(folderPath, f"{index}image_{uuid.uuid4()}.jpg")
    else:
        file_path = os.path.join(folderPath, f"page_{index}.jpg")

    # Send a GET request to the URL
    response = requests.get(file_url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Open a file in binary write mode
        with open(file_path, "wb") as file:
            # Write the content of the response to the file
            file.write(response.content)
        print(f"File saved successfully to {file_path}")
        time.sleep(1)
    else:
        print("Failed to retrieve the video")


def remove_all_files_in_folder_local(deviceKey: str) -> None:
    folderPath = f"{FILE_FOLDER_LOCAL}\\{deviceKey}"

    # Check if the folder exists
    if os.path.exists(folderPath):
        # List all files in the folder
        for filename in os.listdir(folderPath):
            file_path = os.path.join(folderPath, filename)
            try:
                # Check if it's a file (not a directory)
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.remove(file_path)
                # If it's a directory, you can remove it as well
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f"Failed to delete {file_path}. Reason: {e}")
        print(f"All files in {folderPath} have been removed.")
    else:
        print(f"The folder {folderPath} does not exist.")


def check_version_device(deviceKey: str) -> int:
    try:
        # Run adb command to get Android version of the device
        result = subprocess.run(
            ["adb", "-s", deviceKey, "shell", "getprop", "ro.build.version.release"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        # Check for errors in adb command
        if result.returncode != 0:
            raise Exception(
                f"Error checking version for device {deviceKey}: {result.stderr}"
            )

        # Extract the version from the output
        version = result.stdout.strip()

        if not version:
            raise Exception(
                f"Could not retrieve Android version for device {deviceKey}"
            )

        return int(version)

    except Exception as e:
        return str(e)


def set_brightness(deviceKey: str, brightnessPercentage: int = 80):
    # Calculate the brightness value based on the percentage (0 to 255 range)
    brightness_value = int(255 * (brightnessPercentage / 100))

    # Run the adb command to set the screen brightness
    command = [
        "adb",
        "-s",
        deviceKey,
        "shell",
        "settings",
        "put",
        "system",
        "screen_brightness",
        str(brightness_value),
    ]

    # Execute the command using subprocess
    result = subprocess.run(
        command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )

    # Check if the command was successful
    if result.returncode == 0:
        print(f"Successfully set brightness to {brightnessPercentage}%")
    else:
        print(f"Error setting brightness: {result.stderr}")


def get_device_language(deviceKey: str):
    try:
        # Get language
        language = (
            subprocess.check_output(
                ["adb", "-s", deviceKey, "shell", "getprop", "persist.sys.locale"]
            )
            .decode()
            .strip()
        )

        # "en-US", "vi-VN"
        return language
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")
        return None


def check_app_installed(deviceKey: str, appName: str):
    try:
        # Run the ADB command to list packages on the specific device
        command = f"adb -s {deviceKey} shell pm list packages | findstr {appName}"
        result = subprocess.run(command, shell=True, capture_output=True, text=True)

        # If the result return code is 0, that means the app is installed
        if result.returncode == 0:
            return True
        else:
            return False

    except Exception as e:
        print(f"An error occurred: {e}")
        return False


def access_app_device_by_adb(deviceKey: str, appName: str):
    command = None
    if appName == EAppName.Settings.value:
        command = f"adb -s {deviceKey} shell am start -n com.android.settings/.Settings"
    if appName == EAppName.SupperProxy.value:
        command = f"adb -s {deviceKey} shell am start -n com.scheler.superproxy/.activity.MainActivity"
    if appName == EAppName.MyFiles.value:
        command = f"adb -s {deviceKey} shell am start -n com.sec.android.app.myfiles/.external.ui.MainActivity"
    if appName == EAppName.Chrome.value:
        turn_on_permission_app_device(deviceKey=deviceKey, appName=appName)
        command = f"adb -s {deviceKey} shell am start -n com.android.chrome/com.google.android.apps.chrome.Main"
    if appName == EAppName.PlayStore.value:
        turn_on_permission_app_device(deviceKey=deviceKey, appName=appName)
        command = f"adb -s {deviceKey} shell am start -n com.android.vending/com.google.android.finsky.activities.MainActivity"
    if appName == EAppName.Canva.value:
        turn_on_permission_app_device(deviceKey=deviceKey, appName=appName)
        command = f"adb -s {deviceKey} shell am start -n com.canva.editor/com.canva.app.editor.splash.SplashActivity"
    if appName == EAppName.Gmail.value:
        turn_on_permission_app_device(deviceKey=deviceKey, appName=appName)
        command = f"adb -s {deviceKey} shell am start -n com.google.android.gm/com.google.android.gm.ConversationListActivityGmail"
    if appName == EAppName.CloneAppPro.value:
        turn_on_permission_app_device(deviceKey=deviceKey, appName=appName)
        command = f"adb -s {deviceKey} shell am start -n com.py.cloneapp.huawei/.activity.SplashActivity"
    print("command:::", command)
    subprocess.run(command, shell=True, capture_output=True, text=True)


def access_app_clone_by_adb(deviceKey: str, packageName: str, social: str):
    turn_on_permission_app_clone(
        deviceKey=deviceKey, social=social, packageName=packageName
    )

    command = None
    if social == ESocials.Instagram.value:
        # command = f"adb -s {deviceKey} shell am start -n {packageName}/com.instagram.mainactivity.LauncherActivity" => Apply for main app
        command = f"adb -s {deviceKey} shell am start -n {packageName}/com.py.chaos.PlugSplash"  # => Apply for clone app

    print(f"command {deviceKey}:::", command)
    subprocess.run(command, shell=True, capture_output=True, text=True)


def turn_on_permission_app_clone(deviceKey: str, social: str, packageName: str):
    command = None
    if social == ESocials.Instagram.value:
        for permission in PERMISSION_INSTAGRAM:
            print(
                f"Allow permission of {ESocials.Instagram.value}->{packageName}::: {permission}"
            )
            command = f"adb -s {deviceKey} shell pm grant {packageName} {permission}"
            subprocess.run(command, shell=True, capture_output=True, text=True)


def turn_on_permission_app_device(deviceKey: str, appName: str):
    command = None
    if appName == EAppNamePermission.Canva.value:
        for permission in PERMISSION_CANVA:
            print(
                f"Allow permission of {EAppNamePermission.Canva.value}::: {permission}"
            )
            command = f"adb -s {deviceKey} shell pm grant {constant_package_application.CANVA} {permission}"
            subprocess.run(command, shell=True, capture_output=True, text=True)

    if appName == EAppNamePermission.Chrome.value:
        for permission in PERMISSION_CHROME:
            print(
                f"Allow permission of {EAppNamePermission.Chrome.value}::: {permission}"
            )
            command = f"adb -s {deviceKey} shell pm grant {constant_package_application.CHROME} {permission}"
            subprocess.run(command, shell=True, capture_output=True, text=True)

    if appName == EAppNamePermission.CloneAppPro.value:
        for permission in PERMISSION_CLONE_APP_PRO:
            print(
                f"Allow permission of {EAppNamePermission.CloneAppPro.value}::: {permission}"
            )
            command = f"adb -s {deviceKey} shell pm grant {constant_package_application.CLONE_APP_PRO} {permission}"
            subprocess.run(command, shell=True, capture_output=True, text=True)

    if appName == EAppNamePermission.Gmail.value:
        for permission in PERMISSION_GMAIL:
            print(
                f"Allow permission of {EAppNamePermission.Gmail.value}::: {permission}"
            )
            command = f"adb -s {deviceKey} shell pm grant {constant_package_application.GMAIL} {permission}"
            subprocess.run(command, shell=True, capture_output=True, text=True)

    if appName == EAppNamePermission.PlayStore.value:
        for permission in PERMISSION_PLAY_STORE:
            print(
                f"Allow permission of {EAppNamePermission.PlayStore.value}::: {permission}"
            )
            command = f"adb -s {deviceKey} shell pm grant {constant_package_application.PLAY_STORE} {permission}"
            subprocess.run(command, shell=True, capture_output=True, text=True)


def is_package_installed(deviceKey: str, packageName: str) -> bool:
    # Run adb command to list installed packages and check if the packageName is present

    command = f"adb -s {deviceKey} shell pm list packages | grep {packageName}"
    result = subprocess.run(
        command,
        stdout=subprocess.PIPE,  # Capture the output
        stderr=subprocess.PIPE,
        text=True,  # Use text mode for easy string handling
    )

    print("result:::", result)

    # If the package is found, it will be present in stdout
    if result.returncode == 0 and result.stdout:
        print(f"The package '{packageName}' is installed.")
        return True
    else:
        print(f"The package '{packageName}' is not installed.")
        return False


# adb -s 3201d47abc0a1643 shell pm list packages > packages1.txt

## adb -s 3201d47abc0a1643 shell dumpsys package com.android.settings | findstr "Activity" => Get all activities in package nane
# adb -s 3201d47abc0a1643 shell dumpsys package com.android.chrome | findstr "permission" => Find all permission('runtime permissions':)
# adb -s 3201d47abc0a1643 shell pm grant com.android.chrome android.permission.GET_ACCOUNTS => Change permission is 'True'
# adb -s 3201d47abc0a1643 shell pm revoke com.android.chrome android.permission.GET_ACCOUNTS => Change permission is 'False'

############### Settings ###############
# adb -s 3201d47abc0a1643 shell pm list packages | findstr com.android.settings  => Get package setting
# adb -s 3201d47abc0a1643 shell am start -n com.android.settings/.Settings ==> Access to Settings


############### Files ###############
# adb -s 3201d47abc0a1643 shell pm list packages | com.sec.android.app.myfiles  => Get package files
# adb -s 3201d47abc0a1643 shell am start -n com.sec.android.app.myfiles/.external.ui.MainActivity ==> Access to Files

############### CH play ###############
# adb -s 3201d47abc0a1643 shell pm list packages | findstr "com.android.vending" => Get package ch play
# adb -s 3201d47abc0a1643 shell am start -n com.android.vending/com.google.android.finsky.activities.MainActivity

############### Chrome ###############
# adb -s 3201d47abc0a1643 shell pm list packages | findstr "com.android.chrome" => Get package ch play
# adb -s 3201d47abc0a1643 shell am start -n com.android.chrome/com.google.android.apps.chrome.Main


############### Canva ###############
# adb -s 3201d47abc0a1643 shell pm list packages | findstr "com.canva.editor" => Get package ch play
# adb -s 3201d47abc0a1643 shell dumpsys package com.canva.editor | findstr "Activity"
# adb -s 3201d47abc0a1643 shell am start -n com.canva.editor/com.canva.app.editor.splash.SplashActivity

############### Gmail ###############
# adb -s 3201d47abc0a1643 shell pm list packages | findstr "com.google.android.gm" => Get package ch play
# adb -s 3201d47abc0a1643 shell am start -n com.google.android.gm/com.google.android.gm.ConversationListActivityGmail


############### Supper Proxy ###############
# adb -s 3201d47abc0a1643 shell pm list packages | findstr "com.scheler.superproxy" => Get package ch play
# adb -s 3201d47abc0a1643 shell am start -n com.scheler.superproxy/.activity.MainActivity


############### Clone app pro ###############
# adb -s 32014acfaf0a1629 shell pm list packages | findstr "com.py.cloneapp.huawei" => Get package ch play
# adb -s 32014acfaf0a1629 shell dumpsys package com.py.cloneapp.huawei | findstr "Activity" => Get all activities in package nane
# adb -s 32014acfaf0a1629 shell am start -n com.py.cloneapp.huawei/.activity.SplashActivity
