from appium.webdriver.webdriver import WebDriver
from apis.server.common.ApiDevice import ApiDevice
from constants import ConstantPackageApplication
from enums.EAppName import EAppName
from enums.EAppNamePermission import EAppNamePermission
from enums.status.EStatusCommon import EStatusCommon
from helpers import HelperKeycode
from interfaces.model.common.TypeDevice import TypeDevice
from utils.UtilPhoneDevice import is_package_installed, remove_files_in_folder_phone
from utils.actions import (
    UtilActionsClick,
    UtilActionsGetElements,
    UtilActionsRedirect,
    UtilActionsScroll,
    UtilDeviceActionTool,
)
import time
from enums.script.EServiceDevice import EServiceDevice
from enums.script.EActionDevice import EActionDevice


# Start for testing
class ServiceSetUpCHPlay:
    def __init__(self, master: any, driver: WebDriver, deviceKey: str) -> None:
        self.master = master
        self.driver = driver
        self.deviceKey = deviceKey


def execute(instance: ServiceSetUpCHPlay):
    driver = instance.driver
    master = instance.master
    deviceKey = instance.deviceKey
    # email = "longhoang999666@gmail.com"
    # password = "long5678@"
    # email = "hson27032020@gmail.com"
    # password = "Bokute27032020"

    device = ApiDevice(master).getOneByDeviceKey(deviceKey=deviceKey)

    print("-----------> Starting action in CH play application <------------")
    UtilDeviceActionTool.execute_access_app_device(
        driver=driver,
        appName=EAppNamePermission.PlayStore.value,
        deviceKey=deviceKey,
    )

    email = device.get("device_emailInfo").get("email")
    password = device.get("device_emailInfo").get("password")

    print("------------------- Starting login CH Play -------------------")
    login_ch_play(driver=driver, email=email, password=password)

    print("------------------- Starting turn off protected mode -------------------")
    turn_off_protected_mode(driver=driver)

    print("------------------- Starting turn save password mode -------------------")
    turn_off_save_password(driver=driver)

    print("------------------- Starting download Instagram -------------------")
    handler_install(
        driver=driver, deviceKey=deviceKey, appName=EAppName.Instagram.value
    )

    print("------------------- Starting download Threads -------------------")
    handler_install(driver=driver, deviceKey=deviceKey, appName=EAppName.Threads.value)

    print("------------------- Starting download Facebook -------------------")
    handler_install(driver=driver, deviceKey=deviceKey, appName=EAppName.Facebook.value)

    print("------------------- Starting download Youtube -------------------")
    handler_install(driver=driver, deviceKey=deviceKey, appName=EAppName.Youtube.value)

    print("------------------- Starting download X -------------------")
    handler_install(driver=driver, deviceKey=deviceKey, appName=EAppName.X.value)

    print("------------------- Starting download Tiktok -------------------")
    handler_install(driver=driver, deviceKey=deviceKey, appName=EAppName.Tiktok.value)

    print("------------------- Starting download Reddit -------------------")
    handler_install(driver=driver, deviceKey=deviceKey, appName=EAppName.Reddit.value)

    print("------------------- Starting download Pinterest -------------------")
    handler_install(
        driver=driver, deviceKey=deviceKey, appName=EAppName.Pinterest.value
    )

    print("------------------- Starting download Tumblr -------------------")
    handler_install(driver=driver, deviceKey=deviceKey, appName=EAppName.Tumblt.value)

    print("------------------- Starting download Meddium -------------------")
    handler_install(driver=driver, deviceKey=deviceKey, appName=EAppName.Medium.value)

    print("------------------- Starting download Quora -------------------")
    handler_install(driver=driver, deviceKey=deviceKey, appName=EAppName.Quora.value)

    print("------------------- Starting download proxy super -------------------")
    handler_install(
        driver=driver, deviceKey=deviceKey, appName=EAppName.SupperProxy.value
    )

    print("------------------- Starting download app clone -------------------")
    download_app_clone(driver=driver, deviceKey=deviceKey)

    HelperKeycode.keycodeClearApp(driver=driver)
    print("--------- Done setting CH PLAY!!! ---------")

    dataDeviceUpdate: TypeDevice = {
        "device_statusCHPlay": EStatusCommon.Available.value
    }
    ApiDevice(master=instance.master).updateByDeviceKey(
        deviceKey=instance.deviceKey, payload=dataDeviceUpdate
    )


def login_ch_play(driver: WebDriver, email: str, password: str):

    try:
        time.sleep(1)
        UtilActionsGetElements.get_element_by_xpath(
            driver=driver,
            xpath='//android.widget.Button[@resource-id="com.android.vending:id/0_resource_name_obfuscated"]',
            timeout=10,
        ).click()
        print("Click for sign in")
    except:
        print("CH play have login")
        return

    time.sleep(1)
    print("Enter email")
    UtilActionsGetElements.get_element_by_xpath(
        driver=driver, xpath='//android.widget.EditText[@resource-id="identifierId"]'
    ).send_keys(email)
    time.sleep(1)

    print("Click next")
    UtilActionsGetElements.get_element_wait_by_xpath(
        driver=driver,
        xpath='//android.widget.Button[@text="Next"]',
    ).click()

    try:
        print("Check email")
        UtilActionsGetElements.get_element_by_xpath(
            driver=driver,
            xpath='//android.widget.TextView[@text="Couldn’t find your Google Account"]',
            timeout=5,
        )
        print("Email not found")
        return
    except:
        pass

    print("Enter password")
    UtilActionsGetElements.get_element_by_xpath(
        driver=driver, xpath='//android.view.View[@resource-id="password"]'
    )
    time.sleep(1)
    UtilActionsGetElements.get_element_by_xpath(
        driver=driver, xpath="//android.widget.EditText"
    ).send_keys(password)
    time.sleep(1)

    print("Click next")
    UtilActionsGetElements.get_element_wait_by_xpath(
        driver=driver,
        xpath='//android.widget.Button[@text="Next"]',
    ).click()

    try:
        print("Check password is correct")
        UtilActionsGetElements.get_element_by_xpath(
            driver=driver,
            xpath='//android.widget.TextView[@text="Wrong password. Try again or click Forgot password to reset it."]',
            timeout=5,
        )
        print("Password incorrect")
        return
    except:
        pass

    try:
        time.sleep(3)
        UtilActionsScroll.scroll_by_vertical(driver=driver, y_start=1800, y_end=500)
        UtilActionsClick.click_on_element_by_xpath(
            driver=driver, xpath='//android.widget.Button[@text="Skip"]', timeout=5
        )
        print("Click Skip add phone number")
    except:
        pass

    try:
        UtilActionsClick.click_on_element_by_xpath(
            driver=driver, xpath='//android.widget.Button[@text="I agree"]', timeout=5
        )
        print("Click agree")
        time.sleep(5)
    except:
        pass

    try:
        UtilActionsClick.click_on_element_by_xpath(
            driver=driver,
            xpath='//android.widget.Button[@text="Don\'t turn on"]',
            timeout=30,
        )
        print("Click dont turn on")
    except:
        pass

    try:
        UtilActionsClick.click_on_element_by_xpath(
            driver=driver, xpath='//android.widget.Button[@text="Not now"]', timeout=10
        )
        print("Click not now")
        time.sleep(5)
    except:
        pass

    try:
        print("Turn off Back up device data")
        UtilActionsClick.click_on_element_by_xpath(
            driver=driver,
            xpath='//android.widget.Switch[@resource-id="com.google.android.gms:id/sud_items_switch"]',
        )

        UtilActionsClick.click_on_element_by_xpath(
            driver=driver,
            xpath='//android.widget.Button[@text="Accept"]',
        )
        print("Click accept")
    except:
        pass

    try:
        UtilActionsClick.click_on_element_by_xpath(
            driver=driver,
            xpath='//android.widget.Button[@resource-id="com.android.vending:id/0_resource_name_obfuscated" and @text="Accept"]',
        )
        print("Click accept")
    except:
        pass

    try:
        print("Turn not now")
        UtilActionsClick.click_on_element_by_xpath(
            driver=driver,
            xpath='//android.widget.TextView[@content-desc="Not now"]',
            timeout=5,
        )
    except:
        pass


def turn_off_protected_mode(driver: WebDriver):

    while True:
        try:
            print("Click on Icon Avatar Account")
            iconAvatarAccount = UtilActionsGetElements.get_element_by_xpath(
                driver=driver,
                xpath='//android.widget.ImageView[@resource-id="com.android.vending:id/0_resource_name_obfuscated"]',
            )
            UtilActionsClick.click_on_element(driver=driver, element=iconAvatarAccount)
            break
        except:
            HelperKeycode.keycodeMoveBack(driver=driver)

    print("Click on Play Protected")
    titlePlayProtected = UtilActionsGetElements.get_element_wait_by_xpath(
        driver=driver,
        xpath='//android.widget.TextView[@resource-id="com.android.vending:id/0_resource_name_obfuscated" and @text="Play Protect"]',
    )
    UtilActionsClick.click_on_element(driver=driver, element=titlePlayProtected)

    isProtected = False
    print("Check have on protected mode")
    try:
        UtilActionsGetElements.get_element_by_xpath(
            driver=driver,
            xpath='//android.widget.Button[@resource-id="com.android.vending:id/0_resource_name_obfuscated" and @text="Scan"]',
        )
        isProtected = True
    except:
        pass

    if isProtected:
        print("Click on setting")
        titlePlayProtected = UtilActionsGetElements.get_element_wait_by_xpath(
            driver=driver,
            xpath='//android.widget.Button[@content-desc="Settings"]',
        ).click()

        time.sleep(2)
        UtilActionsClick.click_on_loc(driver=driver, y_loc=500)

        UtilActionsGetElements.get_element_wait_by_xpath(
            driver=driver,
            xpath='//android.widget.Button[@resource-id="com.android.vending:id/0_resource_name_obfuscated" and @text="Turn off"]',
        ).click()

    print("Move back home CH Play")
    UtilActionsRedirect.move_back_until_find_element_by_xpath(
        driver=driver,
        xpath='//android.widget.TextView[@text="Search"]',
    )


def login_gg_web(driver: WebDriver, email: str, password: str):

    try:
        time.sleep(2)
        UtilActionsGetElements.get_element_by_xpath(
            driver=driver,
            xpath='//android.widget.Button[@resource-id="com.android.chrome:id/message_primary_button"]',
        )

        UtilActionsClick.click_on_loc(driver=driver, x_loc=200, y_loc=2100)

        time.sleep(1)
        print("Scroll find english US")
        UtilActionsScroll.scroll_vertical_until_find_element_by_xpath(
            driver=driver,
            y_start=500,
            y_end=1800,
            x_loc=245,
            xpath='//android.view.View[@text="English (United States)"]',
        )

        print("Chose english US")
        titleEnglish = UtilActionsGetElements.get_element_by_xpath(
            driver=driver, xpath='//android.view.View[@text="English (United States)"]'
        ).click()
        UtilActionsClick.click_on_element(driver=driver, element=titleEnglish)

    except:
        pass

    try:
        print("Check verify")
        UtilActionsGetElements.get_element_by_xpath(
            driver=driver,
            xpath='//android.widget.Button[@text="Next"]',
        ).click()

        print("Click for switch account")
        UtilActionsGetElements.get_element_wait_by_xpath(
            driver=driver, xpath='//android.widget.TextView[@text="Welcome"]'
        )
        UtilActionsClick.click_on_loc(driver=driver, y_loc=670)

        UtilActionsGetElements.get_element_wait_by_xpath(
            driver=driver,
            xpath='//android.view.View[@content-desc="Use another account"]',
        )

        isHaveAccount = False
        try:
            print("Check have account in the list")
            labelEmailAccount = UtilActionsGetElements.get_element_by_xpath(
                driver=driver,
                xpath=f'//android.widget.TextView[@text="{email}"]',
            )
            UtilActionsClick.click_on_element(driver=driver, element=labelEmailAccount)
            isHaveAccount = True

        except:
            pass

        if not isHaveAccount:
            UtilActionsGetElements.get_element_wait_by_xpath(
                driver=driver,
                xpath='//android.view.View[@content-desc="Use another account"]',
            ).click()

            try:
                time.sleep(1)
                UtilActionsGetElements.get_element_by_xpath(
                    driver=driver,
                    xpath='//android.widget.Button[@resource-id="com.android.chrome:id/account_picker_dismiss_button"]',
                ).click()
            except:
                pass

            print("Enter email")
            UtilActionsGetElements.get_element_wait_by_xpath(
                driver=driver,
                xpath="//android.widget.EditText",
            ).send_keys(email)
            print("Click search")
            UtilActionsGetElements.get_element_wait_by_xpath(
                driver=driver,
                xpath='//android.widget.Button[@text="Next"]',
            ).click()

            print("Enter password")
            UtilActionsGetElements.get_element_wait_by_xpath(
                driver=driver,
                xpath="//android.widget.EditText",
            ).send_keys(password)
            print("Click search")
            UtilActionsClick.click_keyboard_phone_find(driver=driver)

    except:
        pass

    print("Click for dowload")
    UtilActionsGetElements.get_element_wait_by_xpath(
        driver=driver, xpath='//android.widget.Button[@text="Download anyway"]'
    ).click()

    while True:
        try:
            UtilActionsGetElements.get_element_by_xpath(
                driver=driver,
                xpath='//android.widget.Button[@resource-id="com.android.chrome:id/positive_button"]',
            ).click()
            break
        except:
            pass
        time.sleep(2)
        print("Click for download")
        UtilActionsClick.click_on_loc(driver=driver, x_loc=850, y_loc=1430)


def turn_off_save_password(driver: WebDriver):
    print("Click on avatar")
    UtilActionsClick.click_on_element_by_xpath(
        driver=driver,
        xpath='//android.widget.ImageView[@resource-id="com.android.vending:id/0_resource_name_obfuscated"]',
    )

    UtilActionsGetElements.get_element_wait_by_xpath(
        driver=driver,
        xpath='//android.widget.Button[@resource-id="com.android.vending:id/0_resource_name_obfuscated" and @text="Manage your Google Account"]',
    ).click()

    UtilActionsGetElements.get_element_wait_by_xpath(
        driver=driver, xpath='//android.widget.TextView[@text="Data & privacy"]'
    )
    time.sleep(1)
    UtilActionsScroll.scroll_by_vertical(driver=driver, y_start=500, y_end=1000)
    time.sleep(1)
    UtilActionsScroll.scroll_by_horizontal(
        driver=driver, x_start=800, x_end=200, y_loc=780
    )

    print('Click "Security"')
    UtilActionsGetElements.get_element_wait_by_xpath(
        driver=driver,
        xpath='//android.widget.TextView[@text="Security"]',
    ).click()
    time.sleep(2)

    UtilActionsScroll.scroll_by_vertical(
        driver=driver, y_start=2000, y_end=500, number_scroll=4
    )

    print('Click "Manage passwords"')
    UtilActionsGetElements.get_element_wait_by_xpath(
        driver=driver,
        xpath='//android.widget.TextView[@resource-id="com.google.android.gms:id/link_text" and @text="Manage passwords"]',
    ).click()

    print('Click "Settings"')
    UtilActionsClick.click_on_element_wait_by_xpath(
        driver=driver,
        xpath='//android.widget.TextView[@resource-id="com.google.android.gms:id/navigation_bar_item_small_label_view" and @text="Settings"]',
    )

    switchSavePassword = UtilActionsGetElements.get_element_wait_by_xpath(
        driver=driver,
        xpath='//android.widget.Switch[@content-desc="Offer to save passwords"]',
    )
    if switchSavePassword.text.lower() == "on":
        switchSavePassword.click()
    time.sleep(1)

    switchAlertPassword = UtilActionsGetElements.get_element_wait_by_xpath(
        driver=driver,
        xpath='//android.widget.Switch[@content-desc="Password alerts"]',
    )
    if switchAlertPassword.text.lower() == "on":
        switchAlertPassword.click()

    time.sleep(1)
    print("Move back home CH Play")
    UtilActionsRedirect.move_back(driver=driver, number_move=3)


def handler_install(driver: WebDriver, deviceKey: str, appName: str):
    packageName = None
    if appName == EAppName.X.value:
        packageName = ConstantPackageApplication.X
    if appName == EAppName.Facebook.value:
        packageName = ConstantPackageApplication.FACEBOOK
    if appName == EAppName.Tiktok.value:
        packageName = ConstantPackageApplication.TIKTOK
    if appName == EAppName.Instagram.value:
        packageName = ConstantPackageApplication.INSTAGRAM
    if appName == EAppName.Threads.value:
        packageName = ConstantPackageApplication.THREADS
    if appName == EAppName.Youtube.value:
        packageName = ConstantPackageApplication.YOUTUBE
    if appName == EAppName.Medium.value:
        packageName = ConstantPackageApplication.MEDIUM
    if appName == EAppName.Reddit.value:
        packageName = ConstantPackageApplication.REDDIT
    if appName == EAppName.Tumblt.value:
        packageName = ConstantPackageApplication.TUMBLT
    if appName == EAppName.Pinterest.value:
        packageName = ConstantPackageApplication.PINTEREST
    if appName == EAppName.Quora.value:
        packageName = ConstantPackageApplication.QUORA
    if appName == EAppName.SupperProxy.value:
        packageName = ConstantPackageApplication.SUPPER_PROXY

    isAppInstalled = is_package_installed(deviceKey=deviceKey, packageName=packageName)

    if isAppInstalled:
        return print(f"Application {appName} have installed")

    print(f"Search app {appName}")
    time.sleep(2)
    UtilActionsClick.click_on_element_wait_by_xpath(
        driver=driver, xpath='//android.widget.TextView[@text="Search"]'
    )

    UtilActionsClick.click_on_element_wait_by_xpath(
        driver=driver, xpath='//android.widget.TextView[@text="Search apps & games"]'
    )

    UtilActionsGetElements.get_element_wait_by_xpath(
        driver=driver, xpath="//android.widget.EditText"
    ).send_keys(appName)
    time.sleep(2)

    print("Click enter for search")
    UtilActionsClick.click_keyboard_phone_find(driver=driver)
    time.sleep(3)

    listBtnInstall = UtilActionsGetElements.get_multi_elements_by_xpath(
        driver=driver,
        xpath='(//android.widget.TextView[@content-desc="Install"])',
        timeout=5,
    )
    if not listBtnInstall or len(listBtnInstall) == 0:
        print(f"------- Installed {appName} -------")
        UtilActionsRedirect.move_back_until_find_element_by_xpath(
            driver=driver, xpath='//android.widget.TextView[@text="Search"]'
        )
        return

    isClickInstall = False
    if len(listBtnInstall) > 1:
        UtilActionsClick.click_on_loc(
            driver=driver, y_loc=listBtnInstall[1].location["y"] + 10
        )
        isClickInstall = True

    if not isClickInstall:
        print("Check app Have installed")
        try:
            btnOpen = UtilActionsGetElements.get_element_by_xpath(
                driver=driver,
                xpath='//android.widget.TextView[@content-desc="Open"]',
            )
            if btnOpen.location["y"] > 500:
                print("Done installed(Open)")
                return
        except:
            pass

        try:
            btnUpdate = UtilActionsGetElements.get_element_by_xpath(
                driver=driver,
                xpath='//android.widget.TextView[@content-desc="Update"]',
            )
            if btnUpdate.location["y"] > 500:
                print("Done installed(Update)")
                return
        except:
            pass

        print("Click for install")
        UtilActionsClick.click_on_loc(
            driver=driver, y_loc=listBtnInstall[0].location["y"] + 10
        )

    try:
        print("Check install")
        UtilActionsGetElements.get_element_by_xpath(
            driver=driver,
            xpath='//android.widget.TextView[@content-desc="Install"]',
        ).click()
        print("Click install")
    except:
        return

    while True:
        print("Waiting for loading...")
        try:
            UtilActionsGetElements.get_element_by_xpath(
                driver=driver,
                xpath='//android.widget.TextView[@content-desc="Uninstall"]',
            )
            break
        except:
            pass

        try:
            UtilActionsGetElements.get_element_by_xpath(
                driver=driver,
                xpath='//android.widget.Button[@resource-id="com.android.vending:id/0_resource_name_obfuscated" and @text="Not now"]',
            ).click()
        except:
            pass

    print(f"------- Install {appName} successfully -------")

    print("Move back")
    UtilActionsRedirect.move_back_until_find_element_by_xpath(
        driver=driver, xpath='//android.widget.TextView[@text="Search"]'
    )


def download_app_clone(driver: WebDriver, deviceKey: str):
    URL = "https://bit.ly/clonecanh"
    remove_files_in_folder_phone(deviceKey=deviceKey)

    print("Check clone app pro")
    isAppInstalled = is_package_installed(
        deviceKey=deviceKey, packageName=ConstantPackageApplication.CLONE_APP_PRO
    )

    if isAppInstalled:
        return print(f"Application Clone App Pro have installed")

    UtilDeviceActionTool.execute_access_app_device(
        driver=driver,
        appName=EAppNamePermission.Chrome.value,
        deviceKey=deviceKey,
    )

    try:
        print("Click home gg")
        UtilActionsGetElements.get_element_by_xpath(
            driver=driver,
            xpath='//android.widget.ImageButton[@content-desc="Open the home page"]',
        ).click()
    except:
        time.sleep(1)
        print("Click without account")
        UtilActionsClick.click_on_element_by_xpath(
            driver=driver,
            xpath='//android.widget.Button[@resource-id="com.android.chrome:id/signin_fre_dismiss_button"]',
        )
        time.sleep(1)
        print("Got it")
        UtilActionsClick.click_on_element_by_xpath(
            driver=driver,
            xpath='//android.widget.Button[@resource-id="com.android.chrome:id/ack_button"]',
        )

    print("Send URL")
    UtilActionsGetElements.get_element_wait_by_xpath(
        driver=driver,
        xpath='//android.widget.EditText[@resource-id="com.android.chrome:id/search_box_text"]',
    ).click()
    UtilActionsGetElements.get_element_wait_by_xpath(
        driver=driver,
        xpath='//android.widget.EditText[@resource-id="com.android.chrome:id/url_bar"]',
    ).send_keys(URL)
    time.sleep(1)

    print("Click search")
    UtilActionsClick.click_keyboard_phone_find(driver=driver)

    print("Waiting for loading...")
    try:
        UtilActionsGetElements.get_element_wait_by_xpath(
            driver=driver,
            xpath='//android.webkit.WebView[@text="Download - MEGA"]/android.view.View/android.view.View[1]/android.view.View[1]/android.view.View[1]',
            timeout=120,
        )
    except:
        return print("Some thing went wrong with your wifi")

    try:
        print("Check 'Set Chrome as your default browser app?'")
        UtilActionsGetElements.get_element_by_xpath(
            driver=driver,
            xpath='//android.widget.TextView[@resource-id="com.android.permissioncontroller:id/title" and @text="Set Chrome as your default browser app?"]',
            timeout=5,
        )

        print("Chose chrome")
        UtilActionsClick.click_on_element_by_xpath(
            driver=driver,
            xpath='//android.widget.TextView[@resource-id="com.android.permissioncontroller:id/title" and @text="Chrome"]',
        )
        time.sleep(1)

        print("Click set as default")
        UtilActionsClick.click_on_element_by_xpath(
            driver=driver,
            xpath='//android.widget.Button[@resource-id="android:id/button1"]',
        )
    except:
        pass

    print("Click download")
    UtilActionsGetElements.get_element_by_xpath(
        driver=driver, xpath='//android.widget.Button[@text=""]'
    ).click()

    try:
        print("Check 'Set Chrome as your default browser app?'")
        UtilActionsGetElements.get_element_by_xpath(
            driver=driver,
            xpath='//android.widget.TextView[@resource-id="com.android.permissioncontroller:id/title" and @text="Set Chrome as your default browser app?"]',
            timeout=5,
        )

        print("Chose chrome")
        UtilActionsClick.click_on_element_by_xpath(
            driver=driver,
            xpath='//android.widget.TextView[@resource-id="com.android.permissioncontroller:id/title" and @text="Chrome"]',
        )
        time.sleep(1)

        print("Click set as default")
        UtilActionsClick.click_on_element_by_xpath(
            driver=driver,
            xpath='//android.widget.Button[@resource-id="android:id/button1"]',
        )

        print("Click download again")
        UtilActionsGetElements.get_element_by_xpath(
            driver=driver, xpath='//android.widget.Button[@text=""]'
        ).click()
    except:
        pass

    countCheckingDownload = 0
    maxCheckingDownload = 20
    while True:
        if countCheckingDownload == maxCheckingDownload:
            return print("Some thing went wrong  download clone app")

        try:
            UtilActionsGetElements.get_element_wait_by_xpath(
                driver=driver,
                xpath='//android.widget.Button[@text="OK, got it"]',
                timeout=3,
            ).click()

            print("Click download again")
            UtilActionsGetElements.get_element_by_xpath(
                driver=driver, xpath='//android.widget.Button[@text=""]'
            ).click()
            countCheckingDownload = 0
        except:
            pass

        try:

            print("Waiting for downloading...")
            UtilActionsGetElements.get_element_wait_by_xpath(
                driver=driver,
                xpath='//android.widget.Button[@text="Continue"]',
                timeout=10,
            ).click()
            print("Click continue")
            break
        except:
            pass

    try:
        UtilActionsGetElements.get_element_by_xpath(
            driver=driver,
            xpath='//android.widget.Button[@resource-id="com.android.chrome:id/positive_button"]',
        ).click()
        print("Download anyway")
        time.sleep(1)

        UtilActionsClick.click_on_element_by_xpath(
            driver=driver,
            xpath='//android.widget.TextView[@text="Decline"]',
        ).click()
        print("Click decline CH play")
        time.sleep(2)
    except:
        pass

    print("Access to My Files")
    UtilDeviceActionTool.execute_access_app_device(
        driver=driver, deviceKey=deviceKey, appName=EAppName.MyFiles.value
    )

    print("Click Internal storage")
    UtilActionsClick.click_on_element_by_xpath(
        driver=driver,
        xpath='//android.widget.TextView[@resource-id="com.sec.android.app.myfiles:id/home_list_item_text" and @text="Internal storage"]',
    )
    print("Click download")
    UtilActionsClick.click_on_element_by_xpath(
        driver=driver,
        xpath='//android.widget.TextView[@resource-id="com.sec.android.app.myfiles:id/file_name" and @text="Download"]',
    )
    time.sleep(1)

    print("Click on for install app")
    UtilActionsClick.click_on_loc(driver=driver, y_loc=540)

    try:
        print("Check for allow setting for install the app clone(If have)")
        UtilActionsClick.click_on_element_by_xpath(
            driver=driver,
            xpath='//android.widget.Button[@resource-id="android:id/button1"]',
        )
        print("Click setting for allow install app")

        print("Switch allow")
        UtilActionsGetElements.get_element_by_xpath(
            driver=driver,
            xpath='//android.widget.Switch[@resource-id="android:id/switch_widget"]',
        ).click()

        print("Move back")
        HelperKeycode.keycodeMoveBack(driver=driver)
    except:
        pass

    try:
        UtilActionsGetElements.get_element_by_xpath(
            driver=driver,
            xpath='//android.widget.Button[@resource-id="android:id/button1"]',
            timeout=10,
        ).click()
        print("Click install v1")
        time.sleep(15)
    except:
        pass

    try:
        UtilActionsGetElements.get_element_by_xpath(
            driver=driver,
            xpath='//android.widget.Button[@resource-id="com.android.packageinstaller:id/launch_button"]',
            timeout=5,
        ).click()
        print("Click install v2")
        time.sleep(15)
    except:
        pass

    try:
        print("Click Decline")
        UtilActionsClick.click_on_element_by_xpath(
            driver=driver,
            xpath='//android.widget.TextView[@text="Decline"]',
            timeout=5,
        ).click()
    except:
        pass

    try:
        print("Click open")
        UtilActionsGetElements.get_element_wait_by_xpath(
            driver=driver,
            xpath='//android.widget.Button[@resource-id="android:id/button1"]',
            timeout=10,
        ).click()
        time.sleep(1)
    except:
        pass

    try:
        print("Click open v2")
        UtilActionsGetElements.get_element_wait_by_xpath(
            driver=driver,
            xpath='//android.widget.Button[@resource-id="com.android.packageinstaller:id/launch_button"]',
            timeout=5,
        ).click()
        time.sleep(1)
    except:
        pass

    try:
        time.sleep(2)
        print("Click I got it")
        UtilActionsGetElements.get_element_by_xpath(
            driver=driver,
            xpath='//android.widget.TextView[@resource-id="com.py.cloneapp.huawei:id/tv_btn_ok"]',
        ).click()
        time.sleep(15)
    except:
        pass

    try:
        print("Click không hỏi lại")
        UtilActionsGetElements.get_element_by_xpath(
            driver=driver,
            xpath='//android.widget.Button[@resource-id="android:id/button2"]',
        ).click()
    except:
        pass

    try:
        time.sleep(2)
        print("Click Agree and continue")
        UtilActionsGetElements.get_element_by_xpath(
            driver=driver,
            xpath='//android.widget.TextView[@resource-id="com.py.cloneapp.huawei:id/tv_btn_new_user_ok"]',
        ).click()
    except:
        pass

    print("------- Install App clone successfully -------")


def remove_internet_default(driver: WebDriver):
    driver



setattr(
    ServiceSetUpCHPlay,
    EActionDevice.DEVICE_ACTION_CH_PLAY.name,
    execute,
)

globals()[EServiceDevice.DEVICE_SERVICE_CH_PLAY.name] = ServiceSetUpCHPlay
