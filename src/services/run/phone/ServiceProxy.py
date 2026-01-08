import time, random
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

from apis.lib.ApiProxy import ApiProxy


class ServiceProxy:
    def __init__(self, master: any, driver: WebDriver, account: TypeAccount) -> None:
        self.master = master
        self.driver = driver
        self.account = account

    def proxy_922(self) -> None:
        driver = self.driver
        master = self.master
        account = self.account
        emailProxy = "mrson2828@gmail.com"
        passwordProxy = "Canh668668@@//"

        time.sleep(2)
        UtilActionsScroll.scroll_by_vertical(driver=driver, y_start=2000, y_end=300)

        time.sleep(1)
        UtilActionsClick.click_on_loc(driver=driver, y_loc=170)

        UtilActionsGetElements.get_element_wait_by_xpath(
            driver=driver,
            xpath='//android.widget.EditText[@resource-id="com.samsung.android.app.galaxyfinder:id/edit_search"]',
        ).send_keys("922 S5 Proxy")

        print("Click on titleProxy")
        titleProxy = UtilActionsGetElements.get_element_wait_by_xpath(
            driver=driver,
            xpath='//android.widget.TextView[@content-desc="922 S5 Proxy"]',
        )
        UtilActionsClick.click_on_element(driver=driver, element=titleProxy)

        try:
            print("Check have login")
            time.sleep(3)
            UtilActionsGetElements.get_element_by_xpath(
                driver=driver,
                xpath='//android.widget.EditText[@resource-id="com.firenet.proxy922:id/et_email"]',
            ).send_keys(emailProxy)
            print("Enter email")

            time.sleep(1)
            UtilActionsGetElements.get_element_by_xpath(
                driver=driver,
                xpath='//android.widget.EditText[@resource-id="com.firenet.proxy922:id/et_pass"]',
            ).send_keys(passwordProxy)
            print("Enter password")

            time.sleep(1)
            UtilActionsGetElements.get_element_by_xpath(
                driver=driver,
                xpath='//android.widget.TextView[@resource-id="com.firenet.proxy922:id/tv_login"]',
            ).click()
            print("Click login")

            try:
                time.sleep(1)
                UtilActionsGetElements.get_element_by_xpath(
                    driver=driver,
                    xpath='//android.widget.Button[@resource-id="com.android.permissioncontroller:id/permission_allow_button"]',
                ).click()
            except:
                pass

            try:
                time.sleep(2)
                UtilActionsGetElements.get_element_by_xpath(
                    driver=driver,
                    xpath='//android.widget.Button[@resource-id="android:id/autofill_save_no"]',
                ).click()
            except:
                pass

            isLoginSuccess = False
            try:
                print("Check account have correct")
                UtilActionsGetElements.get_element_by_xpath(
                    driver=driver,
                    xpath='//android.view.ViewGroup[@resource-id="com.firenet.proxy922:id/cl_main_proxy"]',
                )
                isLoginSuccess = True
            except:
                pass

            if not isLoginSuccess:
                return print("Login fail")

        except:
            print("===>>> App have login")
            pass

        print("Click for search proxy")
        UtilActionsGetElements.get_element_wait_by_xpath(
            driver=driver,
            xpath='//android.widget.RelativeLayout[@resource-id="com.firenet.proxy922:id/rl_to_search"]',
        ).click()

        print("Click for search United States")
        time.sleep(2)
        UtilActionsGetElements.get_element_wait_by_xpath(
            driver=driver,
            xpath='//android.widget.RelativeLayout[@resource-id="com.firenet.proxy922:id/rl_search"]',
        ).click()

        print("Click on 'United States'")
        time.sleep(2)
        UtilActionsClick.click_on_element_wait_by_xpath(
            driver=driver,
            xpath='//android.widget.TextView[@resource-id="com.firenet.proxy922:id/tv_name" and @text="United States"]',
        )

        print("Click on chose proxy item")
        time.sleep(3)
        listProxy = UtilActionsGetElements.get_multi_elements_by_xpath(
            driver=driver,
            xpath='//android.widget.GridView[@resource-id="com.firenet.proxy922:id/rv_ip"]/android.widget.LinearLayout',
        )
        itemProxy = random.choice(listProxy)
        itemProxy.click()

        print("Click connect")
        time.sleep(2)
        UtilActionsGetElements.get_element_wait_by_xpath(
            driver=driver,
            xpath='//android.view.ViewGroup[@resource-id="com.firenet.proxy922:id/cl_main_proxy"]',
        ).click()

        try:
            time.sleep(1)
            UtilActionsGetElements.get_element_by_xpath(
                driver=driver,
                xpath='//android.widget.Button[@resource-id="android:id/button1"]',
            ).click()
        except:
            pass

        print("Close the app '922 S5 Proxy'")
        HelperKeycode.keycodeClearApp(driver=driver)

    def proxy_super(self) -> None:
        driver = self.driver
        master = self.master
        account = self.account

        proxyName = "test"
        proxyIp = "46.232.117.143"
        proxyPort = "49155"
        proxyProtocol = "HTTP"
        proxyUsername = "mrson2828"
        proxyPassword = "3V5tRBQA2Q"

        print("Check proxy have working")
        isProxyLive = ApiProxy().check_proxy(
            proxy_ip=proxyIp,
            proxy_port=proxyPort,
            proxy_username=proxyUsername,
            proxy_password=proxyPassword,
        )
        if(not isProxyLive):
            return print("Proxy not available, pls try again!!!")

        time.sleep(2)
        UtilActionsScroll.scroll_by_vertical(driver=driver, y_start=2000, y_end=300)

        time.sleep(1)
        UtilActionsClick.click_on_loc(driver=driver, y_loc=170)

        UtilActionsGetElements.get_element_wait_by_xpath(
            driver=driver,
            xpath='//android.widget.EditText[@resource-id="com.samsung.android.app.galaxyfinder:id/edit_search"]',
        ).send_keys("Super Proxy")

        print("Click on titleProxy")
        titleProxy = UtilActionsGetElements.get_element_wait_by_xpath(
            driver=driver,
            xpath='//android.widget.TextView[@content-desc="Super Proxy"]',
        )
        UtilActionsClick.click_on_element(driver=driver, element=titleProxy)
        time.sleep(3)

        stringItemProxy = f"""//android.view.View[@content-desc="{proxyName}
{proxyIp}:{proxyPort}
{proxyProtocol}"]"""
        print("stringItemProxy:::", stringItemProxy)
        try:
            print("Click on item for connect proxy")
            UtilActionsGetElements.get_element_by_xpath(
                driver=driver, xpath=stringItemProxy
            ).click()

            count = 0
            maxCount = 5
            while count < maxCount:
                try:
                    print("----> Click start")
                    UtilActionsGetElements.get_element_by_xpath(
                        driver=driver,
                        xpath='//android.widget.Button[@content-desc="Start"]',
                    ).click()
                    count += 1

                    try:
                        time.sleep(1)
                        UtilActionsGetElements.get_element_by_xpath(
                            driver=driver,
                            xpath='//android.widget.Button[@resource-id="android:id/button1"]',
                        ).click()
                    except:
                        pass
                except:
                    break

            if count == maxCount:
                print("Some thing went wrong for connect")
            print("Close the app 'Super proxy'")
            HelperKeycode.keycodeClearApp(driver=driver)
            return
        except:
            pass

        try:
            print("Click stop proxy")
            UtilActionsGetElements.get_element_by_xpath(
                driver=driver, xpath='//android.widget.Button[@content-desc="Stop"]'
            ).click()

            time.sleep(1)
            HelperKeycode.keycodeMoveBack(driver=driver)

            print("Click connect proxy")
            UtilActionsGetElements.get_element_wait_by_xpath(
                driver=driver, xpath=stringItemProxy
            ).click()

            count = 0
            maxCount = 5
            while count < maxCount:
                try:
                    print("----> Click start")
                    UtilActionsGetElements.get_element_by_xpath(
                        driver=driver,
                        xpath='//android.widget.Button[@content-desc="Start"]',
                    ).click()
                    count += 1

                    try:
                        time.sleep(1)
                        UtilActionsGetElements.get_element_by_xpath(
                            driver=driver,
                            xpath='//android.widget.Button[@resource-id="android:id/button1"]',
                        ).click()
                    except:
                        pass
                except:
                    break

            if count == maxCount:
                print("Some thing went wrong for connect")
            print("Close the app 'Super proxy'")
            HelperKeycode.keycodeClearApp(driver=driver)
            return
        except:
            pass

        try:
            print("Check start proxy")
            UtilActionsGetElements.get_element_by_xpath(
                driver=driver, xpath='//android.widget.Button[@content-desc="Start"]'
            )

            time.sleep(1)
            HelperKeycode.keycodeMoveBack(driver=driver)

            print("Click connect proxy")
            UtilActionsGetElements.get_element_wait_by_xpath(
                driver=driver, xpath=stringItemProxy
            ).click()

            count = 0
            maxCount = 5
            while count < maxCount:
                try:
                    print("----> Click start")
                    UtilActionsGetElements.get_element_by_xpath(
                        driver=driver,
                        xpath='//android.widget.Button[@content-desc="Start"]',
                    ).click()
                    count += 1

                    try:
                        time.sleep(1)
                        UtilActionsGetElements.get_element_by_xpath(
                            driver=driver,
                            xpath='//android.widget.Button[@resource-id="android:id/button1"]',
                        ).click()
                    except:
                        pass
                except:
                    break

            if count == maxCount:
                print("Some thing went wrong for connect")
            print("Close the app 'Super proxy'")
            HelperKeycode.keycodeClearApp(driver=driver)
            return
        except:
            pass

        print("Click add proxy")
        UtilActionsGetElements.get_element_wait_by_xpath(
            driver=driver,
            xpath='//android.widget.Button[@content-desc="Add proxy"]',
        ).click()

        print("Waiting for loading....")
        UtilActionsGetElements.get_element_wait_by_xpath(
            driver=driver,
            xpath='//android.widget.FrameLayout[@resource-id="android:id/content"]/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.view.View[1]/android.view.View/android.view.View[1]/android.widget.Button[2]',
        )

        print("# Enter proxy name")
        time.sleep(2)
        UtilActionsClick.click_keyboard_phone_remove(driver=driver, time_press=2)
        UtilActionsClick.click_keyboard_phone(driver=driver, string_entry=proxyName)
        time.sleep(1)
        UtilActionsClick.click_keyboard_phone_find(driver=driver)

        print("# Change Protocol")
        UtilActionsGetElements.get_element_wait_by_xpath(
            driver=driver, xpath='//android.widget.EditText[@text="SOCKS5"]'
        ).click()
        UtilActionsGetElements.get_element_wait_by_xpath(
            driver=driver, xpath='//android.view.View[@content-desc="HTTP"]'
        ).click()

        print("# Enter ip")
        UtilActionsGetElements.get_element_wait_by_xpath(
            driver=driver,
            xpath='//android.widget.FrameLayout[@resource-id="android:id/content"]/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.view.View[1]/android.view.View/android.view.View[2]/android.widget.EditText[3]',
        ).click()
        time.sleep(1)
        UtilActionsClick.click_keyboard_phone(driver=driver, string_entry=proxyIp)
        time.sleep(1)
        UtilActionsClick.click_keyboard_phone_find(driver=driver)

        print("# Enter port")
        UtilActionsGetElements.get_element_wait_by_xpath(
            driver=driver,
            xpath='//android.widget.FrameLayout[@resource-id="android:id/content"]/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View[2]/android.widget.EditText[4]',
        ).send_keys(proxyPort)
        time.sleep(1)
        UtilActionsClick.click_on_loc(driver=driver, x_loc=940, y_loc=1750)

        print("# Change Authentication method")
        UtilActionsGetElements.get_element_wait_by_xpath(
            driver=driver, xpath='//android.widget.EditText[@text="None"]'
        ).click()
        UtilActionsGetElements.get_element_wait_by_xpath(
            driver=driver,
            xpath='//android.view.View[@content-desc="Username/Password"]',
        ).click()

        print("# Enter username")
        UtilActionsGetElements.get_element_wait_by_xpath(
            driver=driver,
            xpath='//android.widget.FrameLayout[@resource-id="android:id/content"]/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.view.View[1]/android.view.View/android.view.View[2]/android.widget.EditText[6]',
        ).click()
        time.sleep(1)
        UtilActionsClick.click_keyboard_phone(driver=driver, string_entry=proxyUsername)
        time.sleep(1)
        UtilActionsClick.click_keyboard_phone_find(driver=driver)

        print("# Enter password")
        time.sleep(1)
        UtilActionsClick.click_keyboard_phone(driver=driver, string_entry=proxyPassword)
        time.sleep(1)
        UtilActionsClick.click_keyboard_phone_find(driver=driver)

        print("# Change DNS Resolution")
        UtilActionsGetElements.get_element_wait_by_xpath(
            driver=driver,
            xpath='//android.widget.EditText[@text="Proxy"]',
        ).click()
        UtilActionsGetElements.get_element_wait_by_xpath(
            driver=driver,
            xpath='//android.view.View[@content-desc="Cloudflare DNS"]',
        ).click()

        print("Click save")
        UtilActionsGetElements.get_element_wait_by_xpath(
            driver=driver,
            xpath='//android.widget.FrameLayout[@resource-id="android:id/content"]/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.view.View[1]/android.view.View/android.view.View[1]/android.widget.Button[2]',
        ).click()

        count = 0
        maxCount = 5
        while count < maxCount:
            try:
                print("----> Click start")
                UtilActionsGetElements.get_element_by_xpath(
                    driver=driver,
                    xpath='//android.widget.Button[@content-desc="Start"]',
                ).click()
                count += 1

                try:
                    UtilActionsGetElements.get_element_by_xpath(
                        driver=driver,
                        xpath='//android.widget.Button[@resource-id="android:id/button1"]',
                    ).click()
                except:
                    pass
            except:
                break

        if count == maxCount:
            return print("Some thing went wrong for connect")

        print("Close the app 'Super proxy'")
        HelperKeycode.keycodeClearApp(driver=driver)
