import time, random, subprocess
from interfaces.model.common.TypeAccount import TypeAccount
from utils.actions import (
    UtilActionsGetElements,
    UtilActionsClick,
    UtilActionsScroll,
    UtilActionsRedirect,
)
from utils import UtilConvert, UtilValues
from helpers import HelperKeycode
from appium.webdriver.webdriver import WebDriver
from enums.ESocials import ESocials
from apis.server.common.ApiAccount import ApiAccount

# from helpers.HelperAppClone import check_update_version_app_clone


class ServiceCloneApp:
    def __init__(self, master: any, driver: WebDriver, account: TypeAccount) -> None:
        self.master = master
        self.driver = driver
        self.account: TypeAccount = account

    def run_diff_app(self, deviceKey):
        # Run the diff-app.py script using subprocess and capture the output
        result = subprocess.run(
            ["python", "diff-app.py", deviceKey],  # Run diff-app.py with the device key
            stdout=subprocess.PIPE,  # Capture the output (differences)
            stderr=subprocess.PIPE,  # Capture any errors
            text=True,  # Ensure the output is in text format
        )

        # Check if there was an error
        if result.returncode != 0:
            print(f"Error running diff-app.py: {result.stderr}")
        else:
            print(f"Differences package for device {deviceKey}:")
            return result.stdout

    def write_pack_new(self, deviceKey):
        # Run the diff-app.py script using subprocess and capture the output
        result = subprocess.run(
            [
                "python",
                "write-package-new.py",
                deviceKey,
            ],  # Run diff-app.py with the device key
            stdout=subprocess.PIPE,  # Capture the output (differences)
            stderr=subprocess.PIPE,  # Capture any errors
            text=True,  # Ensure the output is in text format
        )

        # Check if there was an error
        if result.returncode != 0:
            print(f"Error running diff-app.py: {result.stderr}")
        else:
            # Print the output (differences)
            print(f"Differences for device {deviceKey}:")
            print(result.stdout)

    def write_pack_old(self, deviceKey):
        # Run the diff-app.py script using subprocess and capture the output
        result = subprocess.run(
            [
                "python",
                "write-package-old.py",
                deviceKey,
            ],  # Run diff-app.py with the device key
            stdout=subprocess.PIPE,  # Capture the output (differences)
            stderr=subprocess.PIPE,  # Capture any errors
            text=True,  # Ensure the output is in text format
        )

        # Check if there was an error
        if result.returncode != 0:
            print(f"Error running diff-app.py: {result.stderr}")
        else:
            # Print the output (differences)
            print(f"Differences for device {deviceKey}:")
            print(result.stdout)

    def cloneApp(self) -> str:
        typeSocial = self.account.get("account_social")
        typeDevice = self.account.get("account_typeDevice")
        nameDevice = self.account.get("account_nameDevice")
        deviceKey = self.account.get("account_deviceKey")

        print("Write for save old app")
        self.write_pack_old(deviceKey)

        UtilActionsGetElements.get_element_wait_by_xpath(
            driver=self.driver, xpath='//android.widget.TextView[@text="Show all apps"]'
        )

        isFound = False
        while not isFound:
            try:
                titleSocial = None
                if typeSocial == ESocials.Instagram.value:
                    print("Select the item instagram to clone")
                    titleSocial = UtilActionsGetElements.get_element_by_xpath(
                        driver=self.driver,
                        xpath='//android.widget.TextView[@resource-id="com.py.cloneapp.huawei:id/tv_app_name" and @text="Instagram"]',
                    )
                if typeSocial == ESocials.Threads.value:
                    print("Select the item threads to clone")
                    titleSocial = UtilActionsGetElements.get_element_by_xpath(
                        driver=self.driver,
                        xpath='//android.widget.TextView[@resource-id="com.py.cloneapp.huawei:id/tv_app_name" and @text="Threads"]',
                    )
                if typeSocial == ESocials.Facebook.value:
                    print("Select the item instagram to clone")
                    titleSocial = UtilActionsGetElements.get_element_by_xpath(
                        driver=self.driver,
                        xpath='//android.widget.TextView[@resource-id="com.py.cloneapp.huawei:id/tv_app_name" and @text="Instagram"]',
                    )
                if typeSocial == ESocials.Tiktok.value:
                    print("Select the item threads to clone")
                    titleSocial = UtilActionsGetElements.get_element_by_xpath(
                        driver=self.driver,
                        xpath='//android.widget.TextView[@resource-id="com.py.cloneapp.huawei:id/tv_app_name" and @text="Threads"]',
                    )
                time.sleep(1)
                UtilActionsClick.click_on_element(
                    driver=self.driver, element=titleSocial
                )
                isFound = True
            except:
                UtilActionsScroll.scroll_by_vertical(
                    driver=self.driver, y_start=2000, y_end=500
                )

        print("Change the app name based on the username")
        userName = self.account.get("account_username")

        appName = UtilValues.get_name_app_clone(
            user_name=userName, type_social=typeSocial
        )
        UtilActionsGetElements.get_element_wait_by_xpath(
            driver=self.driver,
            xpath='//android.widget.EditText[@resource-id="com.py.cloneapp.huawei:id/et_name"]',
        ).send_keys(appName)

        print("########### Click 'General settings'")
        UtilActionsGetElements.get_element_wait_by_xpath(
            driver=self.driver,
            xpath='//android.widget.RelativeLayout[@resource-id="com.py.cloneapp.huawei:id/rl_btn_general"]',
        ).click()

        print("Switch gg play services")
        statusGGService = UtilActionsGetElements.get_element_wait_by_xpath(
            driver=self.driver,
            xpath='//android.widget.Switch[@resource-id="com.py.cloneapp.huawei:id/switch_gms"]',
        ).text
        if statusGGService == "ON":
            UtilActionsGetElements.get_element_wait_by_xpath(
                driver=self.driver,
                xpath='//android.widget.Switch[@resource-id="com.py.cloneapp.huawei:id/switch_gms"]',
            ).click()

        print("Switch gg play services")
        statusVPN = UtilActionsGetElements.get_element_wait_by_xpath(
            driver=self.driver,
            xpath='//android.widget.Switch[@resource-id="com.py.cloneapp.huawei:id/switch_virtual_vpn"]',
        ).text
        if statusVPN == "OFF":
            UtilActionsGetElements.get_element_wait_by_xpath(
                driver=self.driver,
                xpath='//android.widget.Switch[@resource-id="com.py.cloneapp.huawei:id/switch_virtual_vpn"]',
            ).click()

        HelperKeycode.keycodeMoveBack(driver=self.driver)
        time.sleep(1)

        print("########### Click device privacy")
        UtilActionsClick.click_on_loc(driver=self.driver, x_loc=155, y_loc=1396)
        time.sleep(3)

        print("Click Open A New")
        UtilActionsGetElements.get_element_by_id(
            driver=self.driver, id="com.py.cloneapp.huawei:id/switch_all"
        ).click()

        print("Select Model")
        UtilActionsGetElements.get_element_by_id(
            driver=self.driver, id="com.py.cloneapp.huawei:id/tv_btn_brand_model"
        ).click()

        print("Click chose type device")
        UtilActionsClick.click_on_element_wait_by_xpath(
            driver=self.driver,
            xpath=f'//android.view.View[@content-desc="{typeDevice}"]',
        )
        time.sleep(1)

        countScrollFindDeviceName = 0
        maxScrollFindDeviceName = 3
        while countScrollFindDeviceName < maxScrollFindDeviceName:
            try:
                print("Click chose name device")
                UtilActionsClick.click_on_element_wait_by_xpath(
                    driver=self.driver,
                    xpath=f'//android.view.View[@content-desc="{nameDevice}"]',
                )
                break
            except:
                UtilActionsScroll.scroll_by_vertical(
                    driver=self.driver, x_loc=650, y_start=1800, y_end=800
                )
                countScrollFindDeviceName += 1

        if countScrollFindDeviceName == maxScrollFindDeviceName:
            print("Chose random")
            UtilActionsClick.click_on_loc(driver=self.driver, x_loc=650, y_loc=540)

        print("Click 'Turn on'")
        UtilActionsClick.click_on_element_by_xpath(
            driver=self.driver, xpath='//android.widget.TextView[@text="Turn on"]'
        )

        time.sleep(1)
        print("Move back")
        UtilActionsRedirect.move_back_until_find_element_by_xpath(
            driver=self.driver,
            xpath='//android.widget.TextView[@text="Personal privacy"]',
        )

        print("########### Click Personal Privacy")
        UtilActionsClick.click_on_element_by_xpath(
            driver=self.driver,
            xpath='//android.widget.TextView[@text="Personal privacy"]',
        )

        print("Click virtual photo album")
        statusVirtualPhoto = UtilActionsGetElements.get_element_wait_by_xpath(
            driver=self.driver,
            xpath='//android.widget.Switch[@resource-id="com.py.cloneapp.huawei:id/switch_ablum"]',
        )
        if statusVirtualPhoto.text.lower() == "off":
            statusVirtualPhoto.click()

        print("Click Fake Location")
        UtilActionsGetElements.get_element_by_id(
            driver=self.driver, id="com.py.cloneapp.huawei:id/tv_btn_location"
        ).click()

        print("Allow GPS")
        try:
            UtilActionsGetElements.get_element_by_id(
                driver=self.driver,
                id="com.android.permissioncontroller:id/permission_allow_foreground_only_button",
            ).click()
        except:
            pass

        longitude = random.uniform(-75, -90)
        latitude = random.uniform(35, 44)
        # Click edit location
        print("Click edit location")
        UtilActionsGetElements.get_element_by_id(
            driver=self.driver, id="com.py.cloneapp.huawei:id/iv_btn_edit"
        ).click()

        # Entry Longitude and Latitude (USA)
        print("Entry Longitude and Latitude (USA)")

        UtilActionsGetElements.get_element_by_id(
            driver=self.driver, id="com.py.cloneapp.huawei:id/et_longitude"
        ).send_keys(longitude)

        UtilActionsGetElements.get_element_by_id(
            driver=self.driver, id="com.py.cloneapp.huawei:id/et_latitude"
        ).send_keys(latitude)

        time.sleep(2)

        # Click go
        print("Click go")
        UtilActionsGetElements.get_element_by_id(
            driver=self.driver, id="com.py.cloneapp.huawei:id/tv_btn_go"
        ).click()
        time.sleep(2)

        # Click Apply
        print("Click Apply")
        UtilActionsGetElements.get_element_by_id(
            driver=self.driver, id="com.py.cloneapp.huawei:id/tv_btn_apply"
        ).click()
        time.sleep(2)

        # Move back
        print("Move back")
        UtilActionsGetElements.get_element_by_id(
            driver=self.driver, id="com.py.cloneapp.huawei:id/iv_back"
        ).click()

        # Click clone
        print("Click clone")
        UtilActionsGetElements.get_element_wait_by_id(
            driver=self.driver, id="com.py.cloneapp.huawei:id/tv_btn_next"
        ).click()

        # Wait for the clone to finish
        print("Wait for the clone to finish")
        time.sleep(10)

        try:
            swAllowSource = UtilActionsGetElements.get_element_by_xpath(
                driver=self.driver,
                xpath='//android.widget.Switch[@resource-id="android:id/switch_widget"]',
                timeout=5,
            )
            if swAllowSource.text == "Off":
                swAllowSource.click()
                HelperKeycode.keycodeMoveBack(driver=self.driver)
        except:
            pass

        try:
            print("Click Decline(If have)")
            UtilActionsClick.click_on_element_by_xpath(
                driver=self.driver,
                xpath='//android.widget.TextView[@text="Decline"]',
                timeout=5,
            )
        except:
            pass

        try:
            UtilActionsClick.click_on_element_by_xpath(
                driver=self.driver,
                xpath='//android.widget.Button[@resource-id="android:id/button1"]',
            )
            print("Click Install(If have) v1")
        except:
            pass
        try:
            UtilActionsClick.click_on_element_by_xpath(
                driver=self.driver,
                xpath='//android.widget.Button[@resource-id="com.android.packageinstaller:id/ok_button"]',
            )
            print("Click Install(If have) v2")
        except:
            pass

        try:
            print("Click Decline(If have)")
            UtilActionsClick.click_on_element_by_xpath(
                driver=self.driver,
                xpath='//android.widget.TextView[@text="Decline"]',
                timeout=3,
            )
        except:
            pass

        try:
            print("Click Done(If have) v1")
            UtilActionsClick.click_on_element_by_xpath(
                driver=self.driver,
                xpath='//android.widget.Button[@resource-id="android:id/button2"]',
            )
        except:
            pass
        try:
            UtilActionsClick.click_on_element_by_xpath(
                driver=self.driver,
                xpath='//android.widget.Button[@resource-id="com.android.packageinstaller:id/done_button"]',
            )
            print("Click Done(If have) v2")
        except:
            pass

        try:
            print("Click Decline(If have)")
            UtilActionsClick.click_on_element_by_xpath(
                driver=self.driver,
                xpath='//android.widget.TextView[@text="Decline"]',
                timeout=3,
            )
        except:
            pass

        print("Write for save new app")
        self.write_pack_new(deviceKey)
        time.sleep(3)

        newPackage = self.run_diff_app(deviceKey=deviceKey)

        print("newPackage:::", newPackage.strip())

        HelperKeycode.keycodeClearApp(driver=self.driver)

        return newPackage.strip()
