import random
import time
from apis.server.common.ApiAccount import ApiAccount
from enums.EAppNamePermission import EAppNamePermission
from helpers import HelperKeycode
from enums.ESocials import ESocials
from utils import UtilConvert, UtilValues
from utils.UtilPhoneDevice import access_app_clone_by_adb
from utils.actions import UtilDeviceActionTool
from appium.webdriver.webdriver import WebDriver
from appium.webdriver.common.appiumby import AppiumBy
from interfaces.model.common.TypeAccount import TypeAccount
from services.device.ServiceCloneApp import ServiceCloneApp
from utils.actions import UtilActionsGetElements, UtilActionsClick, UtilActionsScroll


def accessSocial(
    master,
    driver: WebDriver,
    account: TypeAccount,
):
    appName = UtilValues.get_name_app_clone(
        user_name=account.get("account_username"),
        type_social=account.get("account_social"),
    )

    isHaveApp = UtilDeviceActionTool.execute_access_app_clone(
        driver=driver, appName=appName, account=account
    )
    print("isHaveApp:::", isHaveApp)

    if isHaveApp:
        return

    while True:
        try:
            print("--------------- Access Clone App Pro ---------------")
            UtilDeviceActionTool.execute_access_app_device(
                driver=driver,
                appName=EAppNamePermission.CloneAppPro.value,
                deviceKey=account.get("account_deviceKey"),
            )
            print(f"Click clone new app")
            UtilActionsClick.click_on_element_by_xpath(
                driver=driver,
                xpath='//android.widget.ImageView[@resource-id="com.py.cloneapp.huawei:id/iv_btn_create"]',
                timeout=10,
            ).click()
            break
        except:
            pass

    print("# Clone App")
    packageName = ServiceCloneApp(
        master=master, account=account, driver=driver
    ).cloneApp()

    print("Access to package name:", packageName)
    access_app_clone_by_adb(
        deviceKey=account.get("account_deviceKey"),
        social=account.get("account_social"),
        packageName=packageName,
    )


def check_update_version_app_clone(
    driver: WebDriver,
):

    try:
        time.sleep(2)
        UtilActionsGetElements.get_element_by_xpath(
            driver=driver,
            xpath='//android.widget.TextView[@resource-id="com.py.cloneapp.huawei:id/tv_btn_ok"]',
        ).click()
        print("Click I got it")
        time.sleep(10)

        print("Click không hỏi lại")
        UtilActionsGetElements.get_element_by_xpath(
            driver=driver,
            xpath='//android.widget.Button[@resource-id="android:id/button2"]',
        ).click()

        print("Click Agree and continue")
        UtilActionsGetElements.get_element_by_xpath(
            driver=driver,
            xpath='//android.widget.TextView[@resource-id="com.py.cloneapp.huawei:id/tv_btn_new_user_ok"]',
        ).click()
    except:
        pass

    try:
        countClickRetry = 0
        maxClickRetry = 15
        time.sleep(2)

        print("Check connect device")
        while countClickRetry < maxClickRetry:
            try:
                UtilActionsClick.click_on_element_by_xpath(
                    driver=driver,
                    xpath='//android.widget.TextView[@resource-id="com.py.cloneapp.huawei:id/tv_btn_retry"]',
                )
                print(f"Click retry {countClickRetry} time")
                countClickRetry += 1
            except:
                break

        if countClickRetry == maxClickRetry:
            raise ("UnConnect")

    except Exception as e:
        return print("Exception:::", e)

    isClickUpdate = False
    countCheckBtnUpdate = 0
    maxCheckBtnUpdate = 5
    while True:
        if countCheckBtnUpdate == maxCheckBtnUpdate:
            break
        btnUpdate: str = UtilConvert.convert_img_text(
            driver=driver,
            dir_name="images_text",
            image_name="btn_update_app_clone",
            x_start=random.randint(455, 462),
            x_end=random.randint(610, 615),
            y_start=random.randint(1260, 1265),
            y_end=random.randint(1320, 1325),
        )
        if btnUpdate.lower().strip() == "update":
            print("Click update")
            UtilActionsClick.click_on_loc(driver=driver, y_loc=1280)
            isClickUpdate = True
            break
        else:
            countCheckBtnUpdate += 1

    if isClickUpdate:
        print("Waiting for click install...")
        UtilActionsGetElements.get_element_wait_by_xpath(
            driver=driver,
            xpath='//android.widget.Button[@resource-id="android:id/button2"]',
            timeout=300,
        ).click()


def change_name(
    master,
    driver: WebDriver,
    account: TypeAccount,
    old_app_name: str,
    new_app_name: str,
):
    print("--------------- Access Clone App Pro ---------------")
    UtilDeviceActionTool.execute_access_app_device(
        driver=driver,
        appName=EAppNamePermission.CloneAppPro.value,
        deviceKey=account.get("account_deviceKey"),
    )

    print("--------------- Check update new version ---------------")
    check_update_version_app_clone(driver=driver)

    print("Click open app")
    try:
        isFind = UtilActionsScroll.scroll_vertical_until_find_element_by_xpath(
            driver=driver,
            maxScrollFind=10,
            xpath=f'//android.widget.TextView[@resource-id="com.py.cloneapp.huawei:id/tv_name" and @text="{old_app_name}"]',
        )
        if isFind:
            UtilActionsGetElements.get_element_wait_by_xpath(
                driver=driver,
                xpath=f'//android.widget.TextView[@resource-id="com.py.cloneapp.huawei:id/tv_name" and @text="{old_app_name}"]',
            ).click()
    except:
        raise ("Some thing went wrong for open the application")

    print("Click STOP app IG")
    UtilActionsGetElements.get_element_wait_by_id(
        driver=driver,
        id="com.py.cloneapp.huawei:id/tv_btn_close",
    ).click()

    print("Click FIX app IG")
    UtilActionsGetElements.get_element_wait_by_id(
        driver=driver,
        id="com.py.cloneapp.huawei:id/rl_btn_edit",
    ).click()

    print("Enter the new name of app clone")
    UtilActionsGetElements.get_element_wait_by_id(
        driver=driver,
        id="com.py.cloneapp.huawei:id/et_name",
    ).clear()
    time.sleep(1)
    UtilActionsGetElements.get_element_wait_by_id(
        driver=driver,
        id="com.py.cloneapp.huawei:id/et_name",
    ).send_keys(new_app_name)

    print("Click OKE for apply new name")
    UtilActionsGetElements.get_element_wait_by_id(
        driver=driver,
        id="com.py.cloneapp.huawei:id/tv_btn",
    ).click()

    print("Click install for update new name for the app")
    UtilActionsGetElements.get_element_wait_by_xpath(
        driver=driver,
        xpath='//android.widget.Button[@resource-id="android:id/button1"]',
    ).click()

    print("Waiting for install success")
    UtilActionsGetElements.get_element_wait_by_id(
        driver=driver,
        id="com.android.packageinstaller:id/install_success",
    )
    print("Click DONE")
    UtilActionsGetElements.get_element_wait_by_xpath(
        driver=driver,
        xpath='//android.widget.Button[@resource-id="android:id/button2"]',
    ).click()
