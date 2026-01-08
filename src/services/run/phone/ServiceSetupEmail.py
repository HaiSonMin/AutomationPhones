from apis.server.common.ApiDevice import ApiDevice
from enums.status.EStatusCommon import EStatusCommon
from interfaces.model.common.TypeDevice import TypeDevice
from utils.actions import UtilDeviceActionTool
from apis.lib.Api2FA import Api2FA
from apis.server.common.ApiSheetTool import ApiSheetTool
from enums.EAppNamePermission import EAppNamePermission
from enums.type.ETypeSheetDevice import ETypeSheetDevice
from enums.type.ETypeSheetIGThreads import ETypeSheetIGThreads
from enums.status.EStatusExecuteCommon import EStatusExecuteCommon
from appium.webdriver.webdriver import WebDriver
from enums.status.EStatusExecuteCommon import EStatusExecuteCommon
from helpers import HelperKeycode
from interfaces.common.TypeDeviceADB import TypeDeviceADB
from interfaces.common.TypeResponse import TypeDataUser
from utils.actions import (
    UtilActionsClick,
    UtilActionsGetElements,
    UtilActionsRedirect,
    UtilActionsScroll,
)
from utils import UtilValues
import time
from appium.webdriver.common.appiumby import AppiumBy
from enums.script.EServiceDevice import EServiceDevice
from enums.script.EActionDevice import EActionDevice
from interfaces.sheets.common.TypeSheetSetupDevice import TypeSheetSetupDevice
from interfaces.model.common.TypeSheetTool import TypeSheetTool
from appium.webdriver.common.appiumby import AppiumBy


# Start for testing
class ServiceSetupEmail:
    def __init__(self, master: any, driver: WebDriver, deviceKey: str) -> None:
        print("Service Change Email")
        self.master = master
        self.driver = driver
        self.deviceKey = deviceKey
        self.user: TypeDataUser = master.user
        self.sheetIdSetupDevice = None
        self.sheetNameSetupDevice = None
        self.sheetIndexSetupDevice = None
        self.dataSetupDevice = None

        listSheetSetupDevice: list[TypeSheetTool] = ApiSheetTool(
            master=master
        ).getMultiByType(typeSheet=ETypeSheetDevice.TYPE_SETUP_DEVICE.value)
        dataSheetSetupDevice: TypeSheetTool = listSheetSetupDevice[0]

        self.sheetIdSetupDevice = UtilValues.get_id_of_sheet(
            url=dataSheetSetupDevice.get("sheet_url")
        )
        self.sheetNameSetupDevice = dataSheetSetupDevice.get("sheet_name")

        dataSheetsSetupDevice: list[TypeSheetSetupDevice] = (
            UtilValues.get_values_google_sheet(
                sheetId=self.sheetIdSetupDevice,
                sheetName=self.sheetNameSetupDevice,
            )
        )

        for index, dataSheet in enumerate(dataSheetsSetupDevice):
            if dataSheet.get("device_key") == self.deviceKey:
                self.dataSetupDevice = dataSheet
                self.sheetIndexSetupDevice = index
                break


def execute(instance: ServiceSetupEmail):
    driver = instance.driver
    master = instance.master
    dataSetupDevice = instance.dataSetupDevice
    keysColSetupDevice = list(dataSetupDevice.keys())

    print("dataSetupDevice:::", dataSetupDevice)
    print("keysColSetupDevice:::", keysColSetupDevice)

    if not dataSetupDevice:
        return print("Data sheets is empty")

    else:
        indexOfKey = keysColSetupDevice.index("device_key")
        colName = UtilValues.get_col_name(indexCol=indexOfKey)
        UtilValues.write_to_google_sheet(
            sheetId=instance.sheetIdSetupDevice,
            sheetName=instance.sheetNameSetupDevice,
            row=instance.sheetIndexSetupDevice,
            col=colName,
            value=instance.deviceKey,
        )

    indexOfKeyStatusChangeMail = keysColSetupDevice.index("status_setup_gmail")
    colNameStatusChangeMail = UtilValues.get_col_name(
        indexCol=indexOfKeyStatusChangeMail
    )

    try:
        print("----------- Access to gmail -----------")
        UtilDeviceActionTool.execute_access_app_device(
            driver=driver,
            appName=EAppNamePermission.Gmail.value,
            deviceKey=instance.deviceKey,
        )

        print("----------- Login gmail -----------")
        isLoginSuccess = login_gmail(
            instance=instance,
            driver=driver,
        )
        if isLoginSuccess:
            print("Click on avatar")
            UtilActionsGetElements.get_element_wait_by_xpath(
                driver=driver,
                xpath='//android.widget.ImageView[@resource-id="com.google.android.gm:id/og_apd_internal_image_view"]',
            ).click()

            print("Click 'Manager your GG account'")
            UtilActionsGetElements.get_element_wait_by_xpath(
                driver=driver,
                xpath='//android.widget.Button[@resource-id="com.google.android.gm:id/my_account_chip"]',
            ).click()

            # print("----------- Setup privacy gmail -----------")
            # setup_data_privacy(driver=driver)

            print("----------- Setup security -----------")
            setup_security(
                instance=instance,
                driver=driver,
            )

            dataDeviceUpdate: TypeDevice = {
                "device_statusSetupEmail": EStatusCommon.Available.value
            }
            ApiDevice(master=instance.master).updateByDeviceKey(
                deviceKey=instance.deviceKey, payload=dataDeviceUpdate
            )

    except Exception as e:
        UtilValues.write_to_google_sheet(
            sheetId=instance.sheetIdSetupDevice,
            sheetName=instance.sheetNameSetupDevice,
            row=instance.sheetIndexSetupDevice,
            col=colNameStatusChangeMail,
            value=EStatusExecuteCommon.Error.value,
        )

    HelperKeycode.keycodeClearApp(driver=driver)


def login_gmail(instance: ServiceSetupEmail, driver: WebDriver) -> bool:

    dataSetupDevice = instance.dataSetupDevice
    keysColSetupDevice = list(dataSetupDevice.keys())

    isHomePage = False
    try:
        print("Checking home page...")
        UtilActionsGetElements.get_element_by_xpath(
            driver=driver,
            xpath='//android.widget.FrameLayout[@resource-id="com.google.android.gm:id/hub_tabs_nav_container"]',
        )
        isHomePage = True
    except:
        pass

    if not isHomePage:
        try:
            print("Click 'Skip tour' for new email")
            UtilActionsGetElements.get_element_by_xpath(
                driver=driver,
                xpath='//android.widget.TextView[@resource-id="com.google.android.gm:id/welcome_tour_skip"]',
                timeout=5,
            ).click()
        except:
            pass

        try:
            print("Click 'got it' for new email")
            UtilActionsGetElements.get_element_by_xpath(
                driver=driver,
                xpath='//android.widget.TextView[@resource-id="com.google.android.gm:id/welcome_tour_got_it"]',
                timeout=5,
            ).click()
        except:
            pass

        print("Check have email")
        isHaveEmail = False
        try:
            UtilActionsGetElements.get_element_by_xpath(
                driver=driver,
                xpath='//android.widget.TextView[@resource-id="com.google.android.gm:id/setup_addresses_add_another"]',
            )
            UtilActionsClick.click_on_element_by_xpath(
                driver=driver,
                xpath=f'//android.widget.TextView[@resource-id="com.google.android.gm:id/account_address" and @text="{dataSetupDevice.get("email")}"]',
            )
            isHaveEmail = True
        except:
            pass

        if not isHaveEmail:
            print("Click 'add another email'")
            time.sleep(1)
            UtilActionsGetElements.get_element_wait_by_xpath(
                driver=driver,
                xpath='//android.widget.TextView[@resource-id="com.google.android.gm:id/setup_addresses_add_another"]',
            ).click()

            print("Click 'Google'")
            time.sleep(1)
            UtilActionsClick.click_on_element_by_xpath(
                driver=driver,
                xpath='//android.widget.TextView[@resource-id="com.google.android.gm:id/account_setup_label" and @text="Google"]',
            )

            print("Enter email")
            email = dataSetupDevice.get("email")
            password = dataSetupDevice.get("password_email_current")
            time.sleep(3)
            UtilActionsGetElements.get_element_by_xpath(
                driver=driver,
                xpath='//android.widget.EditText[@resource-id="identifierId"]',
            ).send_keys(email)
            time.sleep(1)
            UtilActionsGetElements.get_element_by_xpath(
                driver=driver, xpath='//android.widget.Button[@text="Next"]'
            ).click()
            time.sleep(5)

            try:
                print("Check email have exist")
                UtilActionsGetElements.get_element_by_xpath(
                    driver=driver,
                    xpath='//android.widget.TextView[@text="Couldn’t find your Google Account"]',
                    timeout=5,
                )

                print("Update status")
                indexOfKey = keysColSetupDevice.index("status_setup_gmail")
                colName = UtilValues.get_col_name(indexCol=indexOfKey)
                UtilValues.write_to_google_sheet(
                    sheetId=instance.sheetIdSetupDevice,
                    sheetName=instance.sheetNameSetupDevice,
                    row=instance.sheetIndexSetupDevice,
                    col=colName,
                    value=EStatusExecuteCommon.Error.value,
                )

                indexOfKey = keysColSetupDevice.index("note")
                colName = UtilValues.get_col_name(indexCol=indexOfKey)
                UtilValues.write_to_google_sheet(
                    sheetId=instance.sheetIdSetupDevice,
                    sheetName=instance.sheetNameSetupDevice,
                    row=instance.sheetIndexSetupDevice,
                    col=colName,
                    value="Email not exist",
                )
                return False
            except:
                pass

            print("Enter password")
            UtilActionsGetElements.get_element_wait_by_xpath(
                driver=driver, xpath="//android.widget.EditText"
            ).send_keys(password)
            print("Click next")
            time.sleep(1)
            UtilActionsGetElements.get_element_wait_by_xpath(
                driver=driver, xpath='//android.widget.Button[@text="Next"]'
            ).click()
            time.sleep(10)

            try:
                print("Check account 'VERIFY'")
                headingText = UtilActionsGetElements.get_element_by_xpath(
                    driver=driver,
                    xpath='//android.widget.TextView[@resource-id="headingText"]',
                    timeout=5,
                )
                print("headingText.text:::", headingText.text)

                if headingText.text == "Verify it’s you":
                    print("Update status")
                    indexOfKey = keysColSetupDevice.index("status_setup_gmail")
                    colName = UtilValues.get_col_name(indexCol=indexOfKey)
                    UtilValues.write_to_google_sheet(
                        sheetId=instance.sheetIdSetupDevice,
                        sheetName=instance.sheetNameSetupDevice,
                        row=instance.sheetIndexSetupDevice,
                        col=colName,
                        value=EStatusExecuteCommon.Error.value,
                    )

                    indexOfKey = keysColSetupDevice.index("note")
                    colName = UtilValues.get_col_name(indexCol=indexOfKey)
                    UtilValues.write_to_google_sheet(
                        sheetId=instance.sheetIdSetupDevice,
                        sheetName=instance.sheetNameSetupDevice,
                        row=instance.sheetIndexSetupDevice,
                        col=colName,
                        value="Account require verify, please change email and run setting gmail again",
                    )
                    return False
            except:
                pass

            try:
                print("Check pass is correct")
                UtilActionsGetElements.get_element_by_xpath(
                    driver=driver,
                    xpath='//android.widget.TextView[@text="Couldn’t find your Google Account"]',
                    timeout=5,
                )

                print("Update status")
                indexOfKey = keysColSetupDevice.index("status_setup_gmail")
                colName = UtilValues.get_col_name(indexCol=indexOfKey)
                UtilValues.write_to_google_sheet(
                    sheetId=instance.sheetIdSetupDevice,
                    sheetName=instance.sheetNameSetupDevice,
                    row=instance.sheetIndexSetupDevice,
                    col=colName,
                    value=EStatusExecuteCommon.Error.value,
                )

                indexOfKey = keysColSetupDevice.index("note")
                colName = UtilValues.get_col_name(indexCol=indexOfKey)
                UtilValues.write_to_google_sheet(
                    sheetId=instance.sheetIdSetupDevice,
                    sheetName=instance.sheetNameSetupDevice,
                    row=instance.sheetIndexSetupDevice,
                    col=colName,
                    value="Password incorrect",
                )
                return False
            except:
                pass

            try:
                print("Check 'Add phone number'")
                headingText = UtilActionsGetElements.get_element_wait_by_xpath(
                    driver=driver,
                    xpath='//android.widget.TextView[@resource-id="headingText"]',
                )
                if headingText.text == "Add phone number?":
                    UtilActionsScroll.scroll_by_vertical(driver=driver)

                    print("Click yes(Add phone number)")
                    UtilActionsGetElements.get_element_wait_by_xpath(
                        driver=driver,
                        xpath='//android.widget.Button[@text="Yes, I’m in"]',
                    ).click()
            except:
                pass

            try:
                print("Click agree")
                UtilActionsGetElements.get_element_wait_by_xpath(
                    driver=driver, xpath='//android.widget.Button[@text="I agree"]'
                ).click()
            except:
                pass

        try:
            print("Check 'You're signed in'")
            headingText = UtilActionsGetElements.get_element_wait_by_xpath(
                driver=driver,
                xpath='//android.widget.TextView[@resource-id="headingText"]',
            )
            if headingText.text == "You're signed in":
                UtilActionsClick.click_on_element_by_xpath(
                    driver=driver,
                    xpath='//android.widget.Button[@text="Not now"]',
                )
        except:
            pass

        try:
            print("Click dont turn on")
            UtilActionsClick.click_on_element_by_xpath(
                driver=driver,
                xpath='//android.widget.Button[@text="Don\'t turn on"]',
            )

            print("Click Not now")
            UtilActionsClick.click_on_element_by_xpath(
                driver=driver,
                xpath='//android.widget.Button[@text="Not now"]',
            )
        except:
            pass

        try:
            print("Click Accept")
            UtilActionsClick.click_on_element_by_xpath(
                driver=driver,
                xpath='//android.widget.Switch[@resource-id="com.google.android.gms:id/sud_items_switch"]',
            )
            UtilActionsClick.click_on_element_by_xpath(
                driver=driver,
                xpath='//android.widget.Button[@text="Accept"]',
            )
        except:
            pass

        try:
            time.sleep(1)
            print("Click chose email")
            UtilActionsClick.click_on_element_by_xpath(
                driver=driver,
                xpath=f'//android.widget.TextView[@resource-id="com.google.android.gm:id/account_address" and @text="{dataSetupDevice.get("email")}"]',
            )
        except:
            pass

        try:
            print("Click take me to gmail")
            UtilActionsGetElements.get_element_by_xpath(
                driver=driver,
                xpath='//android.widget.TextView[@resource-id="com.google.android.gm:id/action_done"]',
            ).click()
        except:
            pass

        try:
            print("Click skip tour")
            UtilActionsGetElements.get_element_by_xpath(
                driver=driver,
                xpath='//android.widget.TextView[@resource-id="com.google.android.gm:id/welcome_tour_skip"]',
            ).click()
            time.sleep(3)
            print("Click take me to gmail")
            UtilActionsGetElements.get_element_by_xpath(
                driver=driver,
                xpath='//android.widget.TextView[@resource-id="com.google.android.gm:id/action_done"]',
            ).click()
        except:
            pass

    print("Click on my avatar")
    UtilActionsClick.click_on_element_by_xpath(
        driver=driver,
        xpath='//android.widget.ImageView[@resource-id="com.google.android.gm:id/og_apd_internal_image_view"]',
    )

    try:
        time.sleep(1)
        titleEmail = UtilActionsGetElements.get_element_by_xpath(
            driver=driver,
            xpath=f'//android.widget.TextView[@resource-id="com.google.android.gm:id/og_secondary_account_information" and @text="{dataSetupDevice.get("email")}"]',
        )
        titleManageGGAccount = UtilActionsGetElements.get_element_by_xpath(
            driver=driver,
            xpath='//android.widget.Button[@resource-id="com.google.android.gm:id/my_account_chip"]',
        )
        if titleEmail.location["y"] < titleManageGGAccount.location["y"]:
            print("Its my account current is login")
            HelperKeycode.keycodeMoveBack(driver=driver)
        else:
            print("Click chose account")
            UtilActionsClick.click_on_element(driver=driver, element=titleEmail)
        return True
    except:
        print("=>>>>>>>>>>>>>>>>>> Account not yet login")
        pass

    print("Click 'Add another account'")
    time.sleep(1)
    labelAddAnotherAccount = UtilActionsGetElements.get_element_wait_by_xpath(
        driver=driver,
        xpath='//android.widget.TextView[@resource-id="com.google.android.gm:id/og_text_card_title" and @text="Add another account"]',
    )
    UtilActionsClick.click_on_element(driver=driver, element=labelAddAnotherAccount)

    print("Click 'Google'")
    time.sleep(1)
    UtilActionsClick.click_on_element_by_xpath(
        driver=driver,
        xpath='//android.widget.TextView[@resource-id="com.google.android.gm:id/account_setup_label" and @text="Google"]',
    )

    print("Enter email")
    email = dataSetupDevice.get("email")
    password = dataSetupDevice.get("password_email_current")
    time.sleep(3)
    UtilActionsGetElements.get_element_by_xpath(
        driver=driver,
        xpath='//android.widget.EditText[@resource-id="identifierId"]',
    ).send_keys(email)
    time.sleep(1)
    UtilActionsGetElements.get_element_by_xpath(
        driver=driver, xpath='//android.widget.Button[@text="Next"]'
    ).click()
    time.sleep(5)

    print("Enter password")
    UtilActionsGetElements.get_element_wait_by_xpath(
        driver=driver, xpath="//android.widget.EditText"
    ).send_keys(password)
    print("Click next")
    time.sleep(1)
    UtilActionsGetElements.get_element_wait_by_xpath(
        driver=driver, xpath='//android.widget.Button[@text="Next"]'
    ).click()
    time.sleep(2)

    try:
        print("Click agree")
        UtilActionsGetElements.get_element_wait_by_xpath(
            driver=driver, xpath='//android.widget.Button[@text="I agree"]'
        ).click()
    except:
        print("Password incorrect")
        indexOfKey = keysColSetupDevice.index("status_setup_gmail")
        colName = UtilValues.get_col_name(indexCol=indexOfKey)
        UtilValues.write_to_google_sheet(
            sheetId=instance.sheetIdSetupDevice,
            sheetName=instance.sheetNameSetupDevice,
            row=instance.sheetIndexSetupDevice,
            col=colName,
            value=EStatusExecuteCommon.Error.value,
        )

        indexOfKey = keysColSetupDevice.index("note")
        colName = UtilValues.get_col_name(indexCol=indexOfKey)
        UtilValues.write_to_google_sheet(
            sheetId=instance.sheetIdSetupDevice,
            sheetName=instance.sheetNameSetupDevice,
            row=instance.sheetIndexSetupDevice,
            col=colName,
            value="Password incorrect",
        )

        return False

    try:
        print("Click dont turn on")
        UtilActionsClick.click_on_element_by_xpath(
            driver=driver,
            xpath='//android.widget.Button[@text="Don\'t turn on"]',
        )

        print("Click Not now")
        UtilActionsClick.click_on_element_by_xpath(
            driver=driver,
            xpath='//android.widget.Button[@text="Not now"]',
        )
    except:
        pass

    try:
        print("Click Accept")
        UtilActionsClick.click_on_element_by_xpath(
            driver=driver,
            xpath='//android.widget.Switch[@resource-id="com.google.android.gms:id/sud_items_switch"]',
        )
        UtilActionsClick.click_on_element_by_xpath(
            driver=driver,
            xpath='//android.widget.Button[@text="Accept"]',
        )
    except:
        pass

    try:
        time.sleep(1)
        print("Click chose email")
        UtilActionsClick.click_on_element_by_xpath(
            driver=driver,
            xpath=f'//android.widget.TextView[@resource-id="com.google.android.gm:id/account_address" and @text="{dataSetupDevice.get("email")}"]',
        )
    except:
        pass

    try:
        print("Click take me to gmail")
        UtilActionsGetElements.get_element_by_xpath(
            driver=driver,
            xpath='//android.widget.TextView[@resource-id="com.google.android.gm:id/action_done"]',
        ).click()
    except:
        pass

    try:
        print("Click skip tour")
        UtilActionsGetElements.get_element_by_xpath(
            driver=driver,
            xpath='//android.widget.TextView[@resource-id="com.google.android.gm:id/welcome_tour_skip"]',
        ).click()
        print("Click take me to gmail")
        UtilActionsGetElements.get_element_by_xpath(
            driver=driver,
            xpath='//android.widget.TextView[@resource-id="com.google.android.gm:id/action_done"]',
        ).click()
    except:
        pass

    return True


def setup_data_privacy(driver: WebDriver) -> bool:
    try:
        print("Click 'Data & privacy'")
        UtilActionsGetElements.get_element_wait_by_xpath(
            driver=driver,
            xpath='//android.widget.LinearLayout[@content-desc="Data & privacy"]',
        ).click()
        time.sleep(2)

        print("### Turn of WebActivity ###")
        UtilActionsScroll.scroll_by_vertical(
            driver=driver, number_scroll=1, y_start=1500
        )
        time.sleep(1)

        print("Click 'Web & App Activity'")
        UtilActionsClick.click_on_element_by_xpath(
            driver=driver,
            xpath='//android.widget.TextView[@resource-id="com.google.android.gms:id/text" and @text="Web & App Activity"]',
        )

        print("Waiting for loading")
        UtilActionsGetElements.get_element_wait_by_xpath(
            driver=driver,
            xpath='//android.widget.TextView[@text="Activity controls"]',
        )

        print("Check have turn on")
        isTurnOn = False
        try:
            UtilActionsGetElements.get_element_by_xpath(
                driver=driver,
                xpath='//android.widget.Button[@text="Turn off"]',
                timeout=5,
            )
            isTurnOn = True
        except:
            pass

        print("isTurnOn:::", isTurnOn)

        if isTurnOn:
            time.sleep(1)
            print("Click on btn turn off")
            btnTurnOff = UtilActionsGetElements.get_element_by_xpath(
                driver=driver,
                xpath='//android.widget.Button[@text="Turn off"]',
            )
            UtilActionsClick.click_on_element(driver=driver, element=btnTurnOff)

            time.sleep(2)
            print("Click turn off")
            UtilActionsClick.click_on_loc(
                driver=driver,
                x_loc=btnTurnOff.location["x"],
                y_loc=btnTurnOff.location["y"] - 300,
            )
            UtilActionsGetElements.get_element_wait_by_xpath(
                driver=driver, xpath='//android.widget.Button[@text="Got it"]'
            ).click()
            UtilActionsGetElements.get_element_wait_by_xpath(
                driver=driver, xpath='//android.widget.Button[@text="Got it"]'
            ).click()

            time.sleep(2)
            UtilActionsRedirect.move_back_until_find_element_by_xpath(
                driver=driver,
                xpath='//android.widget.Button[@content-desc="Search"]',
                timeout=5,
            )
        else:
            UtilActionsRedirect.move_back_until_find_element_by_xpath(
                driver=driver,
                xpath='//android.widget.Button[@content-desc="Search"]',
                timeout=5,
            )

        UtilActionsScroll.scroll_by_vertical(driver=driver, y_start=500, y_end=200)

        print("### Turn of Youtube history ###")
        UtilActionsScroll.scroll_vertical_until_find_element_by_xpath(
            driver=driver,
            xpath='//android.widget.TextView[@resource-id="com.google.android.gms:id/text" and @text="YouTube History"]',
        )

        print("Click 'YouTube History'")
        UtilActionsClick.click_on_element_by_xpath(
            driver=driver,
            xpath='//android.widget.TextView[@resource-id="com.google.android.gms:id/text" and @text="YouTube History"]',
        )

        print("Waiting for loading")
        UtilActionsGetElements.get_element_wait_by_xpath(
            driver=driver,
            xpath='//android.widget.TextView[@text="Activity controls"]',
        )
        print("Check have turn on")
        isTurnOn = False
        try:
            UtilActionsGetElements.get_element_by_xpath(
                driver=driver,
                xpath='//android.widget.Button[@text="Turn off"]',
            )
            isTurnOn = True
        except:
            pass

        if isTurnOn:
            time.sleep(1)
            print("Click on btn turn off")
            btnTurnOff = UtilActionsGetElements.get_element_by_xpath(
                driver=driver,
                xpath='//android.widget.Button[@text="Turn off"]',
            )
            UtilActionsClick.click_on_element(driver=driver, element=btnTurnOff)
            UtilActionsGetElements.get_element_wait_by_xpath(
                driver=driver, xpath='//android.widget.Button[@text="Pause"]'
            ).click()
            UtilActionsGetElements.get_element_wait_by_xpath(
                driver=driver, xpath='//android.widget.Button[@text="Got it"]'
            ).click()

            time.sleep(2)
            UtilActionsRedirect.move_back_until_find_element_by_xpath(
                driver=driver,
                xpath='//android.widget.Button[@content-desc="Search"]',
                timeout=5,
            )
        else:
            UtilActionsRedirect.move_back_until_find_element_by_xpath(
                driver=driver,
                xpath='//android.widget.Button[@content-desc="Search"]',
                timeout=5,
            )

        print("---------------> Setup privacy success <---------------")
    except:
        print("---------------> Setup privacy fail <---------------")
        UtilActionsRedirect.move_back_until_find_element_by_xpath(
            driver=driver,
            xpath='//android.widget.Button[@content-desc="Search"]',
            timeout=5,
        )


def setup_security(
    instance: ServiceSetupEmail,
    driver: WebDriver,
) -> bool:
    dataSetupDevice = instance.dataSetupDevice
    keysColSetupDevice = list(dataSetupDevice.keys())

    print("Click 'Security'")
    UtilActionsGetElements.get_element_wait_by_xpath(
        driver=driver,
        xpath='//android.widget.LinearLayout[@content-desc="Security"]',
    ).click()

    ######### Skip password when possible #########
    print("######### Skip password when possible #########")
    time.sleep(2)
    UtilActionsScroll.scroll_by_vertical(driver=driver)

    isOffSkipPassword = False
    try:
        print("Check Skip password have turn off")
        UtilActionsGetElements.get_element_by_xpath(
            driver=driver,
            xpath='//android.widget.TextView[@resource-id="com.google.android.gms:id/text" and @text="Off"]',
        )
        isOffSkipPassword = True
    except:
        pass

    if not isOffSkipPassword:
        print("Click on 'Skip password when possible'")
        UtilActionsClick.click_on_element_by_xpath(
            driver=driver,
            xpath='//android.widget.TextView[@resource-id="com.google.android.gms:id/text" and @text="Skip password when possible"]',
        )

        try:
            print("Close 'Set up screen lock to use passkeys'")
            UtilActionsGetElements.get_element_by_xpath(
                driver=driver,
                xpath='//android.widget.Button[@resource-id="com.google.android.gms:id/cancel_or_use_another_device_button"]',
            ).click()

            print("Click cancel")
            UtilActionsGetElements.get_element_by_xpath(
                driver=driver,
                xpath='//android.widget.Button[@resource-id="com.google.android.gms:id/transport_selection_cancel_button"]',
            ).click()
            time.sleep(3)
        except:
            pass

        try:
            print("Click on 'Try another way'")
            UtilActionsGetElements.get_element_wait_by_xpath(
                driver=driver,
                xpath='//android.widget.Button[@text="Try another way"]',
            ).click()

            print("Click on 'Enter your password'")
            UtilActionsClick.click_on_element_by_xpath(
                driver=driver,
                xpath='//android.widget.TextView[@text="Enter your password"]',
            )

            print("Enter 'password'")
            UtilActionsGetElements.get_element_wait_by_xpath(
                driver=driver, xpath='//android.widget.TextView[@text="Show password"]'
            )
            time.sleep(2)
            UtilActionsGetElements.get_element_wait_by_xpath(
                driver=driver,
                xpath="//android.widget.EditText",
            ).send_keys(dataSetupDevice.get("password_email_current"))
            time.sleep(1)

            print("Click 'Go'")
            UtilActionsClick.click_keyboard_phone_find(driver=driver)
        except:
            pass

        time.sleep(2)
        print("Click for turn off 'Skip password when possible'")
        UtilActionsClick.click_on_element_wait_by_xpath(
            driver=driver,
            xpath='//android.widget.ToggleButton[@text="Toggle skipping your password when possible"]',
        )

        print("Move back")
        UtilActionsRedirect.move_back_until_find_element_by_xpath(
            driver=driver,
            xpath='//android.widget.Button[@content-desc="Search"]',
            timeout=5,
        )

    print("######### Change Password #########")
    UtilActionsScroll.scroll_by_vertical(driver=driver, y_start=500, y_end=2000)
    isChangedEmail = handler_change_password(instance=instance, driver=driver)

    print("######### Recover email #########")
    UtilActionsScroll.scroll_by_vertical(driver=driver, y_start=500, y_end=2000)
    isRecoveredEmail = handler_recover_email(
        instance=instance,
        driver=driver,
    )

    print("######### 2FA email #########")
    UtilActionsScroll.scroll_by_vertical(driver=driver, y_start=500, y_end=2000)
    is2FAEmail = handler_2fa_email(
        instance=instance,
        driver=driver,
    )

    print("######### Signout all device #########")
    UtilActionsScroll.scroll_by_vertical(driver=driver, y_start=500, y_end=2000)
    signout_manager_all_device(driver=driver)

    if isChangedEmail and isRecoveredEmail and is2FAEmail:
        print("---------------> Setup security success")
        indexOfKeyStatusEmail = keysColSetupDevice.index("status_setup_gmail")
        colNameStatusEmail = UtilValues.get_col_name(indexCol=indexOfKeyStatusEmail)

        UtilValues.write_to_google_sheet(
            sheetId=instance.sheetIdSetupDevice,
            sheetName=instance.sheetNameSetupDevice,
            row=instance.sheetIndexSetupDevice,
            col=colNameStatusEmail,
            value=EStatusExecuteCommon.Done.value,
        )

        return True
    else:
        print("---------------> Setup security fail")
        indexOfKeyStatusEmail = keysColSetupDevice.index("status_setup_gmail")
        colNameStatusEmail = UtilValues.get_col_name(indexCol=indexOfKeyStatusEmail)

        UtilValues.write_to_google_sheet(
            sheetId=instance.sheetIdSetupDevice,
            sheetName=instance.sheetNameSetupDevice,
            row=instance.sheetIndexSetupDevice,
            col=colNameStatusEmail,
            value=EStatusExecuteCommon.Error.value,
        )

        return False


def signout_manager_all_device(driver: WebDriver):
    UtilActionsScroll.scroll_vertical_until_find_element_by_xpath(
        driver=driver,
        xpath='//android.widget.TextView[@resource-id="com.google.android.gms:id/link_text"]',
        duration=1000,
    )

    print("Click on 'Password'")
    UtilActionsClick.click_on_element_by_xpath(
        driver=driver,
        xpath='//android.widget.TextView[@resource-id="com.google.android.gms:id/link_text"]',
    )

    labelCurrentSession = UtilActionsGetElements.get_element_by_xpath(
        driver=driver,
        xpath='//android.widget.TextView[@text="Your current session"]',
    )

    while True:
        isHaveClickForSignOut = False
        try:
            listDevicesLogin = UtilActionsGetElements.get_multi_elements_by_xpath(
                driver=driver,
                xpath="(//android.widget.TextView)",
                textContains="Vietnam",
            )

            for deviceLogin in listDevicesLogin:
                if deviceLogin.location["y"] > labelCurrentSession.location["y"]:
                    UtilActionsClick.click_on_element(
                        driver=driver, element=deviceLogin
                    )

                    print("Click signout")
                    UtilActionsClick.click_on_element_by_xpath(
                        driver=driver,
                        xpath='//android.widget.Button[@resource-id="ucj-1"]',
                        xLocReplace=200,
                        yLocReplace=690,
                    )

                    print("Click accept signout")
                    UtilActionsClick.click_on_element_by_xpath(
                        driver=driver,
                        xpath='(//android.widget.Button[@text="Sign out"])[2]',
                        xLocReplace=810,
                        yLocReplace=1300,
                    )
                    time.sleep(5)
                    isHaveClickForSignOut = True
                    break
        except:
            pass

        if not isHaveClickForSignOut:
            break

        UtilActionsRedirect.move_back_until_find_element_by_xpath(
            driver=driver,
            xpath='//android.widget.Button[@content-desc="Search"]',
            timeout=5,
        )


def handler_change_password(instance: ServiceSetupEmail, driver: WebDriver) -> bool:

    dataSetupDevice = instance.dataSetupDevice
    keysColSetupDevice = list(dataSetupDevice.keys())
    currentPassword = dataSetupDevice.get("password_email_current")
    newPassword = dataSetupDevice.get("password_email_new")

    if newPassword:
        UtilActionsScroll.scroll_vertical_until_find_element_by_xpath(
            driver=driver,
            xpath='//android.widget.TextView[@resource-id="com.google.android.gms:id/text" and @text="Password"]',
            duration=1000,
        )

        print("Click on 'Password'")
        UtilActionsClick.click_on_element_by_xpath(
            driver=driver,
            xpath='//android.widget.TextView[@resource-id="com.google.android.gms:id/text" and @text="Password"]',
        )

        try:
            print("Close 'Set up screen lock to use passkeys'")
            UtilActionsGetElements.get_element_by_xpath(
                driver=driver,
                xpath='//android.widget.Button[@resource-id="com.google.android.gms:id/cancel_or_use_another_device_button"]',
                timeout=5,
            ).click()

            print("Click cancel")
            UtilActionsGetElements.get_element_by_xpath(
                driver=driver,
                xpath='//android.widget.Button[@resource-id="com.google.android.gms:id/transport_selection_cancel_button"]',
            ).click()
            time.sleep(3)
        except:
            pass

        try:
            print("Click on 'Try another way'")
            UtilActionsGetElements.get_element_by_xpath(
                driver=driver,
                xpath='//android.widget.Button[@text="Try another way"]',
                timeout=5,
            ).click()

            print("Click on 'Enter your password'")
            UtilActionsClick.click_on_element_by_xpath(
                driver=driver,
                xpath='//android.widget.TextView[@text="Enter your password"]',
            )

            print("Enter 'password'")
            UtilActionsGetElements.get_element_by_xpath(
                driver=driver, xpath='//android.widget.TextView[@text="Show password"]'
            )
            time.sleep(2)
            UtilActionsGetElements.get_element_by_xpath(
                driver=driver,
                xpath="//android.widget.EditText",
            ).send_keys(dataSetupDevice.get("password_email_current"))
            time.sleep(1)

            print("Click 'Go'")
            UtilActionsClick.click_keyboard_phone_find(driver=driver)
        except:
            pass

        try:
            print("Check have authentication password")
            time.sleep(3)
            UtilActionsGetElements.get_element_by_xpath(
                driver=driver,
                xpath='//android.view.View[@content-desc="Terms"]',
                timeout=5,
            )

            print("Enter password")
            UtilActionsGetElements.get_element_by_xpath(
                driver=driver,
                xpath="//android.widget.EditText",
            ).send_keys(currentPassword)
            time.sleep(2)

            print("Click 'Next'")
            time.sleep(1)
            UtilActionsClick.click_on_element_by_xpath(
                driver=driver, xpath='//android.view.View[@resource-id="passwordNext"]'
            )

            # //android.widget.TextView[@text="You used this password recently. Please choose a different one."]
        except:
            pass

        try:
            UtilActionsGetElements.get_element_wait_by_xpath(
                driver=driver, xpath='//android.widget.Button[@text="Change password"]'
            )

            print(f"Enter new password: {newPassword}")
            UtilActionsClick.click_to_paste(driver=driver, y_loc=950, text=newPassword)

            print(f"Re-Enter new password: {newPassword}")
            UtilActionsClick.click_to_paste(driver=driver, y_loc=1510, text=newPassword)

            print("Click change password")
            UtilActionsGetElements.get_element_by_xpath(
                driver=driver, xpath='//android.widget.Button[@text="Change password"]'
            ).click()

        except:
            UtilActionsRedirect.move_back_until_find_element_by_xpath(
                driver=driver,
                xpath='//android.widget.Button[@content-desc="Search"]',
                timeout=5,
            )
            return False

        try:
            print("Click cancel")
            UtilActionsGetElements.get_element_by_xpath(
                driver=driver, xpath='//android.widget.Button[@text="Cancel"]'
            )
            UtilActionsGetElements.get_element_by_xpath(
                driver=driver, xpath='//android.widget.Button[@text="Change password"]'
            ).click()
            print("Waiting for change password....")
            time.sleep(8)
        except:
            print("Password not suitable, change password fail")
            UtilActionsRedirect.move_back_until_find_element_by_xpath(
                driver=driver,
                xpath='//android.widget.Button[@content-desc="Search"]',
                timeout=5,
            )
            return False

        print(
            "############## Update sheet if change password of email successfully ##############"
        )
        indexOfKey = keysColSetupDevice.index("password_email_current")
        colName = UtilValues.get_col_name(indexCol=indexOfKey)

        UtilValues.write_to_google_sheet(
            sheetId=instance.sheetIdSetupDevice,
            sheetName=instance.sheetNameSetupDevice,
            row=instance.sheetIndexSetupDevice,
            col=colName,
            value=newPassword,
        )

        indexOfKeyNew = keysColSetupDevice.index("password_email_new")
        colNameNew = UtilValues.get_col_name(indexCol=indexOfKeyNew)

        UtilValues.write_to_google_sheet(
            sheetId=instance.sheetIdSetupDevice,
            sheetName=instance.sheetNameSetupDevice,
            row=instance.sheetIndexSetupDevice,
            col=colNameNew,
            value="",
        )

        deviceUpdate = ApiDevice(master=instance.master).getOneByDeviceKey(
            deviceKey=instance.deviceKey
        )

        ApiDevice(master=instance.master).updateByDeviceKey(
            deviceKey=instance.deviceKey,
            payload={
                "device_emailInfo": {
                    **deviceUpdate.get("device_emailInfo"),
                    "password": newPassword,
                }
            },
        )

        print("Move back")
        UtilActionsRedirect.move_back_until_find_element_by_xpath(
            driver=driver,
            xpath='//android.widget.Button[@content-desc="Search"]',
            timeout=5,
        )
        return True

    else:
        return True


def handler_recover_email(
    driver: WebDriver,
    instance: ServiceSetupEmail,
) -> bool:
    dataSetupDevice = instance.dataSetupDevice
    keysColSetupDevice = list(dataSetupDevice.keys())
    passWordEmailCurrent = dataSetupDevice.get("password_email_current")
    emailRcvNew = dataSetupDevice.get("email_rcv_new")

    if emailRcvNew:

        UtilActionsScroll.scroll_vertical_until_find_element_by_xpath(
            driver=driver,
            xpath='//android.widget.TextView[@resource-id="com.google.android.gms:id/text" and @text="Recovery email"]',
        )

        print("Click on 'Recover email'")
        UtilActionsClick.click_on_element_by_xpath(
            driver=driver,
            xpath='//android.widget.TextView[@resource-id="com.google.android.gms:id/text" and @text="Recovery email"]',
        )

        try:
            print("Check have authentication password")
            time.sleep(3)
            UtilActionsGetElements.get_element_by_xpath(
                driver=driver,
                xpath='//android.widget.Button[@text="Try another way"]',
            )

            print("Enter password")
            UtilActionsGetElements.get_element_by_xpath(
                driver=driver, xpath="//android.widget.EditText"
            ).send_keys(passWordEmailCurrent)

            print("Click 'Next'")
            UtilActionsGetElements.get_element_by_xpath(
                driver=driver, xpath='//android.widget.Button[@text="Next"]'
            ).click()

        except:
            print("=>>>> Have session login")
            pass

        try:
            UtilActionsGetElements.get_element_wait_by_xpath(
                driver=driver,
                xpath='//android.widget.TextView[@text="Your recovery email"]',
            )

            print("Enter email recover")
            time.sleep(1)
            UtilActionsClick.click_to_paste(
                driver=driver,
                text=emailRcvNew,
                y_loc=1150,
                x_loc=960,
                isRemoveText=True,
            )

            UtilActionsGetElements.get_element_by_xpath(
                driver=driver, xpath='//android.widget.Button[@text="Verify"]'
            ).click()

            try:
                UtilActionsGetElements.get_element_by_xpath(
                    driver=driver,
                    xpath='//android.widget.Button[@text="Send a new code."]',
                )
                UtilActionsRedirect.move_back(driver=driver, number_move=2)
            except:
                UtilActionsRedirect.move_back(driver=driver, number_move=2)

            indexOfKeyEmailRcvOld = keysColSetupDevice.index("email_rcv_old")
            colNameEmailRcvOld = UtilValues.get_col_name(indexCol=indexOfKeyEmailRcvOld)

            UtilValues.write_to_google_sheet(
                sheetId=instance.sheetIdSetupDevice,
                sheetName=instance.sheetNameSetupDevice,
                row=instance.sheetIndexSetupDevice,
                col=colNameEmailRcvOld,
                value=emailRcvNew,
            )

            indexOfKeyEmailRcvOld = keysColSetupDevice.index("email_rcv_new")
            colNameEmailRcvNew = UtilValues.get_col_name(indexCol=indexOfKeyEmailRcvOld)

            UtilValues.write_to_google_sheet(
                sheetId=instance.sheetIdSetupDevice,
                sheetName=instance.sheetNameSetupDevice,
                row=instance.sheetIndexSetupDevice,
                col=colNameEmailRcvNew,
                value="",
            )

            deviceUpdate = ApiDevice(master=instance.master).getOneByDeviceKey(
                deviceKey=instance.deviceKey
            )

            ApiDevice(master=instance.master).updateByDeviceKey(
                deviceKey=instance.deviceKey,
                payload={
                    "device_emailInfo": {
                        **deviceUpdate.get("device_emailInfo"),
                        "emailReceiver": emailRcvNew,
                    }
                },
            )

            time.sleep(3)
            return True

        except:
            print("Some thing went wrong went recover email")
            return False

    else:
        print("======>>>>> Email recover is empty")
        return True


def handler_2fa_email(driver: WebDriver, instance: ServiceSetupEmail):
    dataSetupDevice = instance.dataSetupDevice
    keysColSetupDevice = list(dataSetupDevice.keys())
    passWordEmailCurrent = dataSetupDevice.get("password_email_current")

    email2FA = dataSetupDevice.get("email_2fa")

    if not email2FA:

        print("Move back for get 2FA email")
        UtilActionsRedirect.move_back_until_find_element_by_xpath(
            driver=driver,
            xpath='//android.widget.TextView[@text="Security"]',
        )
        time.sleep(1)
        UtilActionsScroll.scroll_by_vertical(driver=driver, y_start=500, y_end=2000)
        UtilActionsScroll.scroll_by_vertical(driver=driver, number_scroll=2)

        print("Click on 'Authenticator'")
        UtilActionsGetElements.get_element_wait_by_xpath(
            driver=driver,
            xpath='//android.widget.Button[@resource-id="com.google.android.gms:id/action_chip" and @text="Authenticator"]',
        ).click()

        try:
            print("Check have authentication password")
            time.sleep(3)
            UtilActionsGetElements.get_element_by_xpath(
                driver=driver,
                xpath='//android.widget.Button[@text="Try another way"]',
            )

            print("Enter password")
            UtilActionsGetElements.get_element_by_xpath(
                driver=driver, xpath="//android.widget.EditText"
            ).send_keys(passWordEmailCurrent)

            print("Click 'Next'")
            UtilActionsGetElements.get_element_by_xpath(
                driver=driver, xpath='//android.widget.Button[@text="Next"]'
            ).click()

        except:
            print("=>>>> Have session login")
            pass

        print("Click on 'Set up authenticator'")
        UtilActionsGetElements.get_element_wait_by_xpath(
            driver=driver,
            xpath='//android.widget.Button[@text="Set up authenticator"]',
        ).click()

        print("Click on 'Cant scan it'")
        UtilActionsGetElements.get_element_wait_by_xpath(
            driver=driver,
            xpath='//android.widget.Button[@text="Can’t scan it?"]',
        ).click()

        print("Get Code 2FA")
        UtilActionsGetElements.get_element_wait_by_xpath(
            driver=driver,
            xpath='//android.app.Dialog[@text="Set up authenticator app"]',
        )
        UtilActionsClick.click_hold_on_loc(
            driver=driver, x_loc=125, y_loc=540, time_press=3
        )
        time.sleep(1)
        UtilActionsScroll.scroll_by_horizontal(
            driver=driver, y_loc=600, x_start=210, x_end=900
        )
        time.sleep(1)
        print("Click copy 2fa")
        UtilActionsClick.click_on_loc(driver=driver, x_loc=140, y_loc=450)

        code2FA = driver.get_clipboard_text()
        print("code2FA:::", code2FA)

        print("Get code 6 digit")
        code6Digit2FA = Api2FA().get_code(secretKey=code2FA)

        print("Click 'Next'")
        UtilActionsGetElements.get_element_wait_by_xpath(
            driver=driver, xpath='//android.widget.Button[@text="Next"]'
        ).click()

        print("Enter code for confirm")
        UtilActionsGetElements.get_element_wait_by_xpath(
            driver=driver,
            xpath='//android.widget.TextView[@text="Enter the 6-digit code you see in the app"]',
        )
        UtilActionsClick.click_to_paste(driver=driver, text=code6Digit2FA, y_loc=450)

        print("Click verify")
        UtilActionsGetElements.get_element_by_xpath(
            driver=driver, xpath='//android.widget.Button[@text="Verify"]'
        ).click()

        indexOfKeyGmail2FA = keysColSetupDevice.index("email_2fa")
        colNameGmail2FA = UtilValues.get_col_name(indexCol=indexOfKeyGmail2FA)

        UtilValues.write_to_google_sheet(
            sheetId=instance.sheetIdSetupDevice,
            sheetName=instance.sheetNameSetupDevice,
            row=instance.sheetIndexSetupDevice,
            col=colNameGmail2FA,
            value=code2FA,
        )

        deviceUpdate = ApiDevice(master=instance.master).getOneByDeviceKey(
            deviceKey=instance.deviceKey
        )

        ApiDevice(master=instance.master).updateByDeviceKey(
            deviceKey=instance.deviceKey,
            payload={
                "device_emailInfo": {
                    **deviceUpdate.get("device_emailInfo"),
                    "email2fa": code2FA,
                }
            },
        )

    return True


setattr(
    ServiceSetupEmail,
    EActionDevice.DEVICE_ACTION_SETUP_EMAIL.name,
    execute,
)

globals()[EServiceDevice.DEVICE_SERVICE_SETUP_EMAIL.name] = ServiceSetupEmail
