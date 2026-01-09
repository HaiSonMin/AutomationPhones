import time
from appium.webdriver.webdriver import WebDriver
from enums.EAppName import EAppName
from enums.status.EStatusCommon import EStatusCommon
from interfaces.model.common.TypeDevice import TypeDevice
from utils.actions import (
    UtilActionsClick,
    UtilActionsScroll,
    UtilActionsGetElements,
    UtilActionsRedirect,
    UtilDeviceActionTool,
)
from utils import UtilPhoneDevice
from appium.webdriver.common.appiumby import AppiumBy
from enums.script.EServiceDevice import EServiceDevice
from enums.script.EActionDevice import EActionDevice
from helpers import HelperKeycode
from apis.server.common.ApiDevice import ApiDevice


# Start for testing
class ServiceSetupDevice:
    def __init__(self, master: any, driver: WebDriver, deviceKey: str) -> None:
        self.master = master
        self.driver = driver
        self.deviceKey = deviceKey


def execute(instance: ServiceSetupDevice):
    driver = instance.driver
    master = instance.master
    deviceKey = instance.deviceKey

    print("---------- Starting for setup language ----------")
    setting_language(driver=driver, deviceKey=deviceKey)

    UtilDeviceActionTool.execute_access_app_device(
        driver=driver, appName=EAppName.Settings.value, deviceKey=deviceKey
    )

    print("----------Starting remove app internet samsung ----------")
    remove_app_internet_default(driver=driver, deviceKey=deviceKey)

    print("----------Starting login to wifi ----------")
    setting_access_wifi(driver=driver)

    print("---------- Starting turn off location ----------")
    setting_turn_off_location(driver=driver)

    print("---------- Starting turn off auto update ----------")
    setting_turnoff_auto_update(driver=driver)

    print("---------- Starting for setup keyboard ----------")
    setting_keyboard(driver=driver)

    print("---------- Starting for setup date and time ----------")
    setting_time_zone(driver=driver)

    print("---------- Starting for setup lock screen ----------")
    setting_lock_screen(driver=driver)

    # print("---------- Starting setting silence mode ----------")
    # setting_silence_mode(driver=driver)

    print("---------- Done Setting Device!!!-----------")
    HelperKeycode.keycodeHome(driver=driver)
    HelperKeycode.keycodeClearApp(driver=driver)
    dataDeviceUpdate: TypeDevice = {"device_statusSetup": EStatusCommon.Available.value}
    ApiDevice(master=instance.master).updateByDeviceKey(
        deviceKey=instance.deviceKey, payload=dataDeviceUpdate
    )


def remove_app_internet_default(driver: WebDriver, deviceKey: str):

    print("Click for search setting")
    iconAccountRecord = UtilActionsGetElements.get_element_by_xpath(
        driver=driver,
        xpath='//android.widget.Button[@content-desc="Samsung account profile"]',
    )
    UtilActionsClick.click_on_loc(
        driver=driver,
        x_loc=iconAccountRecord.location["x"] - 50,
        y_loc=iconAccountRecord.location["y"] + 50,
    )

    print("Search to find 'Location'")
    UtilActionsGetElements.get_element_by_xpath(
        driver=driver,
        xpath='//android.widget.EditText[@resource-id="com.android.settings.intelligence:id/search_src_text"]',
    ).send_keys("Apps")

    UtilActionsGetElements.get_element_wait_by_xpath(
        driver=driver,
        xpath='//android.widget.TextView[@resource-id="android:id/title" and @text="Apps"]',
        timeout=90,
    ).click()
    time.sleep(5)

    UtilActionsGetElements.get_element_wait_by_xpath(
        driver=driver,
        xpath='//android.widget.Button[@content-desc="Search apps"]',
    ).click()

    UtilActionsGetElements.get_element_wait_by_xpath(
        driver=driver,
        xpath='//android.widget.EditText[@resource-id="com.android.settings:id/search_src_text"]',
    ).send_keys("Samsung Internet")

    try:
        UtilActionsClick.click_on_element_by_xpath(
            driver=driver,
            xpath='//android.widget.TextView[@resource-id="android:id/title" and @text="Samsung Internet"]',
        )

        print("Click uninstall")
        UtilActionsClick.click_on_element_by_xpath(
            driver=driver,
            xpath='//android.widget.Button[@resource-id="com.android.settings:id/button2"]',
        )

        print("Click ok")
        UtilActionsClick.click_on_element_by_xpath(
            driver=driver,
            xpath='//android.widget.Button[@resource-id="android:id/button1"]',
        )
    except:
        pass

    UtilActionsRedirect.move_back_until_find_element_by_xpath(
        driver=driver,
        xpath='//android.widget.Button[@content-desc="Samsung account profile"]',
        timeout=3,
    )


def setting_turn_off_location(driver: WebDriver):
    print("Click for search setting")
    iconAccountRecord = UtilActionsGetElements.get_element_by_xpath(
        driver=driver,
        xpath='//android.widget.Button[@content-desc="Samsung account profile"]',
    )
    UtilActionsClick.click_on_loc(
        driver=driver,
        x_loc=iconAccountRecord.location["x"] - 50,
        y_loc=iconAccountRecord.location["y"] + 50,
    )

    print("Search to find 'Location'")
    UtilActionsGetElements.get_element_by_xpath(
        driver=driver,
        xpath='//android.widget.EditText[@resource-id="com.android.settings.intelligence:id/search_src_text"]',
    ).send_keys("Location")
    time.sleep(1)
    UtilActionsGetElements.get_element_wait_by_xpath(
        driver=driver,
        xpath='//android.widget.TextView[@resource-id="android:id/title" and @text="Location"]',
        timeout=90,
    ).click()
    time.sleep(1)

    try:
        UtilActionsGetElements.get_element_by_xpath(
            driver=driver,
            xpath='//android.widget.Button[@resource-id="android:id/button2"]',
            timeout=5,
        ).click()
    except:
        pass

    print("Turn off Location")
    swLocation = UtilActionsGetElements.get_element_by_xpath(
        driver=driver,
        xpath='//android.widget.Switch[@resource-id="com.android.settings:id/switch_widget"]',
        timeout=10,
    )
    if swLocation.text == "Location, On":
        swLocation.click()

    try:
        UtilActionsGetElements.get_element_by_xpath(
            driver=driver,
            xpath='//android.widget.Button[@resource-id="android:id/button2"]',
            timeout=5,
        ).click()
    except:
        pass

    print("Scrolling down")
    UtilActionsScroll.scroll_by_vertical(
        driver=driver, number_scroll=1, y_start=2100, y_end=200
    )
    time.sleep(1)

    try:

        print("Clicking Earthquake alerts")
        UtilActionsGetElements.get_element_by_xpath(
            driver=driver,
            xpath='//android.widget.TextView[@resource-id="android:id/title" and @text="Earthquake alerts"]',
        ).click()

        time.sleep(1)

        print("Turn off Earthquake alerts")
        swEarthquake = UtilActionsGetElements.get_element_by_xpath(
            driver=driver,
            xpath='//android.widget.Switch[@resource-id="com.google.android.gms:id/toggle"]',
        )
        if swEarthquake.text == "On":
            swEarthquake.click()

        print("Move back")
        UtilActionsGetElements.get_element_by_xpath(
            driver=driver,
            xpath='//android.widget.ImageButton[@content-desc="Navigate up"]',
        ).click()
        time.sleep(1)
    except:
        pass

    try:
        print("Click Emergency Location Service")
        UtilActionsGetElements.get_element_by_xpath(
            driver=driver,
            xpath='//android.widget.TextView[@resource-id="android:id/title" and @text="Emergency Location Service"]',
        ).click()
        time.sleep(1)

        print("Turn off Emergency Location Service")
        swEmergency = UtilActionsGetElements.get_element_by_xpath(
            driver=driver,
            xpath='//android.widget.Switch[@resource-id="android:id/switch_widget"]',
        )
        if swEmergency.text == "On":
            swEmergency.click()
        time.sleep(1)

        print("Move back")
        UtilActionsGetElements.get_element_by_xpath(
            driver=driver,
            xpath='//android.widget.ImageButton[@content-desc="Navigate up"]',
        ).click()
        time.sleep(1)
    except:
        pass

    try:
        print("Clicking Location Accuracy")
        UtilActionsGetElements.get_element_by_xpath(
            driver=driver,
            xpath='//android.widget.TextView[@resource-id="android:id/title" and @text="Location Accuracy"]',
        ).click()
        time.sleep(1)

        print("Turn off Location Accuracy")
        swAccuracy = UtilActionsGetElements.get_element_by_xpath(
            driver=driver,
            xpath='//android.widget.Switch[@resource-id="android:id/switch_widget"]',
        )
        if swAccuracy.text == "On":
            swAccuracy.click()
        time.sleep(1)
    except:
        pass

    UtilActionsRedirect.move_back_until_find_element_by_xpath(
        driver=driver,
        xpath='//android.widget.Button[@content-desc="Samsung account profile"]',
        timeout=3,
    )


def setting_keyboard(driver: WebDriver):
    print("----------------------> Setting Keyboard <----------------------")

    print("Click for search setting")
    iconAccountRecord = UtilActionsGetElements.get_element_by_xpath(
        driver=driver,
        xpath='//android.widget.Button[@content-desc="Samsung account profile"]',
    )
    UtilActionsClick.click_on_loc(
        driver=driver,
        x_loc=iconAccountRecord.location["x"] - 50,
        y_loc=iconAccountRecord.location["y"] + 50,
    )

    print("Search to find 'General management'")
    UtilActionsGetElements.get_element_by_xpath(
        driver=driver,
        xpath='//android.widget.EditText[@resource-id="com.android.settings.intelligence:id/search_src_text"]',
    ).send_keys("General management")

    listTitles = UtilActionsGetElements.get_multi_elements_wait_by_xpath(
        driver=driver,
        xpath='(//android.widget.TextView[@resource-id="android:id/title"])',
        timeout=90,
    )
    for title in listTitles:
        if title.text == "General management":
            UtilActionsClick.click_on_element(driver=driver, element=title)
            break

    print("Click on 'Language and input'")
    titleLanguageAndKeyboard = UtilActionsGetElements.get_element_wait_by_xpath(
        driver=driver,
        xpath='//android.widget.TextView[@resource-id="android:id/title" and @text="Language and input"]',
    )
    UtilActionsClick.click_on_element(driver=driver, element=titleLanguageAndKeyboard)

    print("Click on 'On-screen keyboard'")
    titleOnScreenKeyboard = UtilActionsGetElements.get_element_wait_by_xpath(
        driver=driver,
        xpath='//android.widget.TextView[@resource-id="android:id/title" and @text="On-screen keyboard"]',
    )
    UtilActionsClick.click_on_element(driver=driver, element=titleOnScreenKeyboard)
    time.sleep(4)

    print("Click on 'Samsung Keyboard'")
    try:
        UtilActionsClick.click_on_element_by_xpath(
            driver=driver,
            xpath='//android.widget.TextView[@resource-id="android:id/title" and @text="Samsung Keyboard"]',
        )
    except:
        UtilActionsClick.click_on_loc(driver=driver, y_loc=400)
        pass

    try:
        print("Click on 'Languages and types'")
        UtilActionsClick.click_on_element_by_xpath(
            driver=driver,
            xpath='//android.widget.TextView[@resource-id="android:id/title" and @text="Languages and types"]',
        )
    except:
        raise ("Lỗi rồi")

    print("Click option for remove language VN")
    UtilActionsGetElements.get_element_wait_by_xpath(
        driver=driver,
        xpath='//android.widget.ImageView[@content-desc="More options"]',
    ).click()

    try:
        print("Click on 'Remove'")
        titleRemove = UtilActionsGetElements.get_element_by_xpath(
            driver=driver,
            xpath='//android.widget.TextView[@resource-id="com.sec.android.inputmethod:id/title" and @text="Remove"]',
        )
        UtilActionsClick.click_on_element(driver=driver, element=titleRemove)

        print("Click on 'Select All'")
        UtilActionsGetElements.get_element_wait_by_xpath(
            driver=driver,
            xpath='//android.widget.CheckBox[@resource-id="com.sec.android.inputmethod:id/select_all_checkbox"]',
        ).click()

        print("Click on 'English' => Ignore English")
        titleEnglishUS = UtilActionsGetElements.get_element_wait_by_xpath(
            driver=driver,
            xpath='//android.widget.TextView[@resource-id="com.sec.android.inputmethod:id/tv_language" and @text="English (US)"]',
        )
        UtilActionsClick.click_on_element(driver=driver, element=titleEnglishUS)

        print("Click on 'Remove'")
        UtilActionsGetElements.get_element_wait_by_xpath(
            driver=driver,
            xpath='//android.widget.Button[@resource-id="com.sec.android.inputmethod:id/remove_menu"]',
        ).click()

    except:
        pass

    finally:
        UtilActionsClick.click_on_loc(driver=driver, y_loc=2000)
        time.sleep(1)
        # UtilActionsRedirect.move_back(driver=driver, number_move=2)
        UtilActionsRedirect.move_back_until_find_element_by_xpath(
            driver=driver,
            xpath='//android.widget.TextView[@resource-id="android:id/title" and @text="Default keyboard"]',
        )

    print("Click on 'Default Keyboard'")
    UtilActionsClick.click_on_element_by_xpath(
        driver=driver,
        xpath='//android.widget.TextView[@resource-id="android:id/title" and @text="Default keyboard"]',
    )

    print("Click chose Samsung keyboard")
    time.sleep(1)
    UtilActionsClick.click_on_element_by_xpath(
        driver=driver,
        xpath='//android.widget.TextView[@resource-id="android:id/text1" and @text="Samsung Keyboard"]',
    )

    time.sleep(1)

    UtilActionsRedirect.move_back_until_find_element_by_xpath(
        driver=driver,
        xpath='//android.widget.Button[@content-desc="Samsung account profile"]',
        timeout=3,
    )


def setting_language(driver: WebDriver, deviceKey: str):
    deviceLanguage = UtilPhoneDevice.get_device_language(deviceKey)

    if deviceLanguage.strip() == "en-US":
        print("Language is english")
        return

    time.sleep(1)
    HelperKeycode.keycodeHome(driver=driver)

    time.sleep(1)
    UtilActionsScroll.scroll_by_vertical(driver=driver, y_start=2000, y_end=300)

    time.sleep(1)
    UtilActionsGetElements.get_element_by_xpath(
        driver=driver,
        xpath='//android.widget.EditText[@resource-id="com.sec.android.app.launcher:id/app_search_edit_text"]',
    ).click()

    print("----------------------> Setting Language <----------------------")
    try:
        print("Waiting for check language...")
        UtilActionsGetElements.get_element_by_xpath(
            driver=driver,
            xpath='//android.widget.LinearLayout[@content-desc="Tùy chọn khác"]/android.widget.ImageView',
        )
    except:
        return print("----> Language is english")

    UtilActionsGetElements.get_element_wait_by_xpath(
        driver=driver,
        xpath='//android.widget.EditText[@resource-id="com.samsung.android.app.galaxyfinder:id/edit_search"]',
    ).send_keys("Cài đặt")

    UtilActionsGetElements.get_element_by_xpath(
        driver=driver,
        xpath='//android.widget.TextView[@content-desc="Cài đặt"]',
    ).click()

    print("Click for search setting")
    iconAccountRecord = UtilActionsGetElements.get_element_by_xpath(
        driver=driver,
        xpath='//android.widget.Button[@content-desc="Hồ sơ Samsung account"]',
    )
    UtilActionsClick.click_on_loc(
        driver=driver,
        x_loc=iconAccountRecord.location["x"] - 50,
        y_loc=iconAccountRecord.location["y"] + 50,
    )

    print("Search to find 'Quản lý chung'")
    UtilActionsGetElements.get_element_by_xpath(
        driver=driver,
        xpath='//android.widget.EditText[@resource-id="com.android.settings.intelligence:id/search_src_text"]',
    ).send_keys("Quản lý chung")
    UtilActionsGetElements.get_element_wait_by_xpath(
        driver=driver,
        xpath='//android.widget.ImageView[@resource-id="android:id/icon"]',
        timeout=60,
    ).click()

    print("Click on 'Ngôn ngữ và bàn phím'")
    titleLanguageAndKeyboard = UtilActionsGetElements.get_element_wait_by_xpath(
        driver=driver,
        xpath='//android.widget.TextView[@resource-id="android:id/title" and @text="Ngôn ngữ và bàn phím"]',
    )

    UtilActionsClick.click_on_element(driver=driver, element=titleLanguageAndKeyboard)

    print("Click on 'Ngôn ngữ'")
    UtilActionsClick.click_on_loc(driver=driver, y_loc=370)

    isEnglishUS = False
    print("Check have English US")
    try:
        titleEnglishUS = UtilActionsGetElements.get_element_by_xpath(
            driver=driver,
            xpath='//android.widget.TextView[@content-desc="Tiếng Anh (Hoa Kỳ)"]',
        )
        UtilActionsClick.click_on_element(driver=driver, element=titleEnglishUS)
        isEnglishUS = True

        UtilActionsGetElements.get_element_by_xpath(
            driver=driver,
            xpath='//android.widget.Button[@resource-id="com.android.settings:id/apply_button"]',
        ).click()

        UtilActionsClick.click_hold_on_element_by_xpath(
            driver=driver,
            xpath='//android.widget.TextView[@content-desc="Vietnamese (Vietnam)"]',
            timeout=4,
        )

        UtilActionsClick.click_on_element_by_xpath(
            driver=driver,
            xpath='//android.widget.TextView[@resource-id="com.android.settings:id/largeLabel"]',
        )

        UtilActionsClick.click_on_element_by_xpath(
            driver=driver,
            xpath='//android.widget.Button[@resource-id="com.android.settings:id/button1"]',
        )
    except:
        pass

    if not isEnglishUS:
        print("Click on 'Add ngôn ngữ'")
        UtilActionsGetElements.get_element_wait_by_xpath(
            driver=driver,
            xpath='//android.widget.Button[@resource-id="com.android.settings:id/add_language"]',
        ).click()

        print("Click chose English")
        itemEnglish = UtilActionsGetElements.get_element_wait_by_xpath(
            driver=driver,
            xpath='//android.widget.TextView[@content-desc="Tiếng Anh"]',
        )
        UtilActionsClick.click_on_element(driver=driver, element=itemEnglish)

        print("Click chose English Hoa Kỳ")
        itemUS = UtilActionsGetElements.get_element_wait_by_xpath(
            driver=driver,
            xpath='//android.widget.TextView[@content-desc="Hoa Kỳ"]',
        )
        UtilActionsClick.click_on_element(driver=driver, element=itemUS)

        print("Click On 'Đặt mặc định'")
        UtilActionsGetElements.get_element_wait_by_xpath(
            driver=driver,
            xpath='//android.widget.Button[@resource-id="android:id/button1"]',
        ).click()

        print("Remove language VN")
        isClickEdit = False
        try:
            # Apply for android 10
            UtilActionsGetElements.get_element_by_xpath(
                driver=driver, xpath='//android.widget.Button[@text="Edit"]'
            ).click()
            isClickEdit = True
        except:
            pass

        if not isClickEdit:
            try:
                # Apply for android 9
                UtilActionsGetElements.get_element_by_xpath(
                    driver=driver, xpath='//android.widget.Button[@text="Remove"]'
                ).click()
            except:
                pass

        try:
            print("Click chose Vietnamese")
            itemVietNamese = UtilActionsGetElements.get_element_by_xpath(
                driver=driver,
                xpath='//android.widget.TextView[@content-desc="Vietnamese (Vietnam)"]',
            )
            UtilActionsClick.click_on_element(driver=driver, element=itemVietNamese)

            UtilActionsGetElements.get_element_wait_by_xpath(
                driver=driver, xpath='//android.widget.Button[@content-desc="Remove"]'
            ).click()
            print("Click for remove")
            UtilActionsGetElements.get_element_wait_by_xpath(
                driver=driver,
                xpath='//android.widget.Button[@resource-id="com.android.settings:id/button1"]',
            ).click()
        except:
            pass

    time.sleep(1)

    UtilActionsRedirect.move_back_until_find_element_by_xpath(
        driver=driver,
        xpath='//android.widget.Button[@content-desc="Samsung account profile"]',
        timeout=3,
    )


def setting_time_zone(driver: WebDriver):
    print("----------------------> Setting Time zone <----------------------")

    print("Click for search setting")
    iconAccountRecord = UtilActionsGetElements.get_element_by_xpath(
        driver=driver,
        xpath='//android.widget.Button[@content-desc="Samsung account profile"]',
    )
    UtilActionsClick.click_on_loc(
        driver=driver,
        x_loc=iconAccountRecord.location["x"] - 50,
        y_loc=iconAccountRecord.location["y"] + 50,
    )

    print("Search to find 'General management'")
    UtilActionsGetElements.get_element_by_xpath(
        driver=driver,
        xpath='//android.widget.EditText[@resource-id="com.android.settings.intelligence:id/search_src_text"]',
    ).send_keys("General management")
    time.sleep(1)

    listTitles = UtilActionsGetElements.get_multi_elements_wait_by_xpath(
        driver=driver,
        xpath='(//android.widget.TextView[@resource-id="android:id/title"])',
        timeout=90,
    )
    for title in listTitles:
        if title.text == "General management":
            UtilActionsClick.click_on_element(driver=driver, element=title)
            break

    print("Click on Date and time")
    UtilActionsClick.click_on_element_by_xpath(
        driver=driver,
        xpath='//android.widget.TextView[@resource-id="android:id/title" and @text="Date and time"]',
    )

    try:
        print("Check format time zone")
        time.sleep(1)
        UtilActionsGetElements.get_element_by_xpath(
            driver=driver,
            xpath='//android.widget.Switch[@resource-id="android:id/switch_widget" and @text="On"]',
        ).click()
    except:
        pass

    try:
        print("Click select time zone")
        titleSelectTimeZone = UtilActionsGetElements.get_element_wait_by_xpath(
            driver=driver,
            xpath='//android.widget.TextView[@resource-id="android:id/title" and @text="Select time zone"]',
        )
        UtilActionsClick.click_on_element(driver=driver, element=titleSelectTimeZone)

    except:
        titleAutomaticDateAndTime = UtilActionsGetElements.get_element_wait_by_xpath(
            driver=driver,
            xpath='//android.widget.TextView[@resource-id="android:id/title" and @text="Automatic date and time"]',
        )
        UtilActionsClick.click_on_element(
            driver=driver, element=titleAutomaticDateAndTime
        )

    print("Click chose region")
    titleRegion = UtilActionsGetElements.get_element_wait_by_xpath(
        driver=driver,
        xpath='//android.widget.TextView[@resource-id="android:id/title" and @text="Region"]',
    )
    UtilActionsClick.click_on_element(driver=driver, element=titleRegion)

    print("Search USA")
    UtilActionsGetElements.get_element_wait_by_xpath(
        driver=driver,
        xpath='//android.widget.EditText[@resource-id="com.android.settings:id/search_src_text"]',
    ).send_keys("US")
    time.sleep(1)
    UtilActionsClick.click_on_loc(driver=driver, y_loc=360)

    print("Click chose Los Angeles")
    titleLosAngeles = UtilActionsGetElements.get_element_wait_by_xpath(
        driver=driver,
        xpath='//android.widget.TextView[@resource-id="android:id/title" and @text="Los Angeles"]',
    )
    UtilActionsClick.click_on_element(driver=driver, element=titleLosAngeles)

    time.sleep(1)
    UtilActionsRedirect.move_back_until_find_element_by_xpath(
        driver=driver,
        xpath='//android.widget.Button[@content-desc="Samsung account profile"]',
        timeout=3,
    )


def setting_lock_screen(driver: WebDriver):
    print("----------------------> Setting lock screen <----------------------")

    print("Click for search setting")
    iconAccountRecord = UtilActionsGetElements.get_element_by_xpath(
        driver=driver,
        xpath='//android.widget.Button[@content-desc="Samsung account profile"]',
    )
    UtilActionsClick.click_on_loc(
        driver=driver,
        x_loc=iconAccountRecord.location["x"] - 50,
        y_loc=iconAccountRecord.location["y"] + 50,
    )

    print("Search to find 'Lock screen'")
    UtilActionsGetElements.get_element_by_xpath(
        driver=driver,
        xpath='//android.widget.EditText[@resource-id="com.android.settings.intelligence:id/search_src_text"]',
    ).send_keys("Lock screen")
    time.sleep(1)

    UtilActionsGetElements.get_element_wait_by_xpath(
        driver=driver,
        xpath='//android.widget.TextView[@resource-id="android:id/title" and @text="Lock screen"]',
        timeout=90,
    ).click()
    time.sleep(1)

    print("Click on 'Screen lock type'")
    titleScreenLockType = UtilActionsGetElements.get_element_wait_by_xpath(
        driver=driver,
        xpath='//android.widget.TextView[@resource-id="android:id/title" and @text="Screen lock type"]',
    )
    UtilActionsClick.click_on_element(driver=driver, element=titleScreenLockType)

    print("Click on 'None'")
    titleNone = UtilActionsGetElements.get_element_wait_by_xpath(
        driver=driver,
        xpath='//android.widget.TextView[@resource-id="android:id/title" and @text="None"]',
    )
    UtilActionsClick.click_on_element(driver=driver, element=titleNone)

    time.sleep(1)
    UtilActionsRedirect.move_back_until_find_element_by_xpath(
        driver=driver,
        xpath='//android.widget.Button[@content-desc="Samsung account profile"]',
        timeout=3,
    )


def setting_access_wifi(driver: WebDriver):
    listWifiName = ["MyzenQ9", "Sea Dragon IT", "Canh-A19.16", "Canh-A19.16- 5G"]
    listWifiPass = ["0906708345", "@seadragonit99", "Canh56789", "Canh56789"]

    print("Click for search setting")
    iconAccountRecord = UtilActionsGetElements.get_element_by_xpath(
        driver=driver,
        xpath='//android.widget.Button[@content-desc="Samsung account profile"]',
    )
    UtilActionsClick.click_on_loc(
        driver=driver,
        x_loc=iconAccountRecord.location["x"] - 50,
        y_loc=iconAccountRecord.location["y"] + 50,
    )

    print("Search to find 'Connections'")
    UtilActionsGetElements.get_element_by_xpath(
        driver=driver,
        xpath='//android.widget.EditText[@resource-id="com.android.settings.intelligence:id/search_src_text"]',
    ).send_keys("Connections")
    time.sleep(1)

    listTitles = UtilActionsGetElements.get_multi_elements_wait_by_xpath(
        driver=driver,
        xpath='(//android.widget.TextView[@resource-id="android:id/title"])',
        timeout=90,
    )
    for title in listTitles:
        if title.text == "Connections":
            UtilActionsClick.click_on_element(driver=driver, element=title)
            break

    print("Click on Wi-Fi")
    UtilActionsClick.click_on_element_by_xpath(
        driver=driver,
        xpath='//android.widget.TextView[@resource-id="android:id/title" and @text="Wi-Fi"]',
        timeout=10,
    )

    print("Check is on")
    swOnOffWifi = UtilActionsGetElements.get_element_wait_by_xpath(
        driver=driver,
        xpath='//android.widget.Switch[@resource-id="com.android.settings:id/switch_widget"]',
    )
    if swOnOffWifi.text == "Wi-Fi, Off":
        swOnOffWifi.click()
        print("Waiting for loading wifi")
        time.sleep(8)

    isConnected = False
    for idx, wifiName in enumerate(listWifiName):
        if isConnected:
            break

        numbScroll = 0
        maxNumScroll = 1
        while True:
            if numbScroll == maxNumScroll:
                UtilActionsScroll.scroll_by_vertical(
                    driver=driver, y_start=250, y_end=2000
                )
                break
            try:
                itemWifi = UtilActionsGetElements.get_element_by_xpath(
                    driver=driver,
                    xpath=f'//android.widget.TextView[@resource-id="com.android.settings:id/title" and @text="{wifiName}"]',
                )

                try:
                    print("Check wifi is connected...")
                    labelConnected = UtilActionsGetElements.get_element_by_xpath(
                        driver=driver,
                        xpath=f'//android.widget.TextView[@resource-id="com.android.settings:id/summary"]',
                    )

                    if labelConnected.text == "Connected":
                        print("---------> Wifi connected")
                        isConnected = True
                        break
                except:
                    pass

                print("Click to connect wifi")
                UtilActionsClick.click_on_element(driver=driver, element=itemWifi)

                print("Enter pass wifi")
                UtilActionsGetElements.get_element_by_xpath(
                    driver=driver,
                    xpath=f'//android.widget.EditText[@resource-id="com.android.settings:id/edittext"]',
                ).send_keys(listWifiPass[idx])

                print("Click connect")
                UtilActionsGetElements.get_element_by_xpath(
                    driver=driver,
                    xpath=f'//android.widget.Button[@resource-id="com.android.settings:id/button"]',
                ).click()

                try:
                    print("Waiting for connect wifi....")
                    labelConnected = UtilActionsGetElements.get_element_by_xpath(
                        driver=driver,
                        xpath=f'//android.widget.TextView[@resource-id="com.android.settings:id/summary"]',
                        timeout=15,
                    )

                    if labelConnected.text == "Connected":
                        print("---------> Wifi connected <---------")
                except:
                    print(
                        "---------> Some thing went wrong connected wifi, check next step <---------"
                    )

                try:
                    labelConnected = UtilActionsGetElements.get_element_wait_by_xpath(
                        driver=driver,
                        xpath=f'//android.widget.TextView[@resource-id="android:id/message"]',
                        timeout=15,
                    )

                    if labelConnected.text == "Couldn't connect to network.":

                        UtilActionsGetElements.get_element_by_xpath(
                            driver=driver,
                            xpath=f'//android.widget.Button[@resource-id="android:id/button1"]',
                        ).click()
                        time.sleep(1)

                except:
                    print("---------> Wifi connected <---------")
                    break

            except:
                print(
                    "---------> Cant find the wifi to connect, scroll down to find wifi"
                )
                UtilActionsScroll.scroll_by_vertical(
                    driver=driver, y_start=1500, y_end=500
                )
                numbScroll += 1

    UtilActionsRedirect.move_back_until_find_element_by_xpath(
        driver=driver,
        xpath='//android.widget.Button[@content-desc="Samsung account profile"]',
        timeout=3,
    )


def setting_silence_mode(driver: WebDriver):

    print("Scroll to settings")
    UtilActionsScroll.scroll_by_vertical(
        driver=driver, number_scroll=2, y_start=45, y_end=1200
    )
    time.sleep(1)
    while True:
        try:
            print("Checking for setting silence mode...")
            UtilActionsGetElements.get_element_by_xpath(
                driver=driver,
                xpath='//android.widget.TextView[@content-desc="Vibrate, Button label, Double tap to view relevant quick settings."]',
            )
            break
        except:
            pass
        print("Click for change mode to silence")
        UtilActionsClick.click_on_element_by_xpath(
            driver=driver,
            xpath='(//android.widget.ImageView[@resource-id="android:id/icon"])[2]',
            timeout=3,
        )

    print("Change mode success")
    HelperKeycode.keycodeClearApp(driver=driver)


def setting_turnoff_auto_update(driver: WebDriver):
    print("----------------------> Setting turnoff auto update <----------------------")

    print("Click for search setting")
    iconAccountRecord = UtilActionsGetElements.get_element_by_xpath(
        driver=driver,
        xpath='//android.widget.Button[@content-desc="Samsung account profile"]',
    )
    UtilActionsClick.click_on_loc(
        driver=driver,
        x_loc=iconAccountRecord.location["x"] - 50,
        y_loc=iconAccountRecord.location["y"] + 50,
    )

    print("Search to find 'Software update'")
    UtilActionsGetElements.get_element_by_xpath(
        driver=driver,
        xpath='//android.widget.EditText[@resource-id="com.android.settings.intelligence:id/search_src_text"]',
    ).send_keys("Software update")
    time.sleep(1)
    listTitles = UtilActionsGetElements.get_multi_elements_wait_by_xpath(
        driver=driver,
        xpath='(//android.widget.TextView[@resource-id="android:id/title"])',
        timeout=90,
    )
    for title in listTitles:
        if title.text == "Software update":
            UtilActionsClick.click_on_element(driver=driver, element=title)
            break
    # time.sleep(1)
    # UtilActionsClick.click_on_loc(driver=driver, y_loc=350)

    print("Click turn off auto download over wifi")
    swOnOff = UtilActionsGetElements.get_element_wait_by_xpath(
        driver=driver,
        xpath='//android.widget.Switch[@resource-id="android:id/switch_widget"]',
    )
    if swOnOff.text == "On":
        swOnOff.click()

    time.sleep(1)
    UtilActionsRedirect.move_back_until_find_element_by_xpath(
        driver=driver,
        xpath='//android.widget.Button[@content-desc="Samsung account profile"]',
        timeout=3,
    )


setattr(
    ServiceSetupDevice,
    EActionDevice.DEVICE_ACTION_SETUP_DEVICE.name,
    execute,
)
globals()[EServiceDevice.DEVICE_SERVICE_SETUP_DEVICE.name] = ServiceSetupDevice
