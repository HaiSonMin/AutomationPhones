from appium.webdriver.webdriver import WebDriver
from utils.actions import (
    UtilActionsClick,
    UtilActionsScroll,
    UtilActionsGetElements,
)
import time
from appium.webdriver.common.appiumby import AppiumBy
from helpers import HelperKeycode


def enable_flight_mode(driver: WebDriver):

    HelperKeycode.keycodeHome(driver=driver)
    time.sleep(1)

    print("Scrolling to settings")
    UtilActionsScroll.scroll_by_vertical(driver=driver, y_start=45, y_end=1200)
    time.sleep(2)

    print("Clicking settings")
    UtilActionsClick.click_on_loc(driver=driver, y_loc=215, x_loc=1002)
    time.sleep(2)

    print("Clicking search")
    UtilActionsGetElements.get_element_by_xpath(
        driver=driver, xpath='//android.widget.Button[@content-desc="Search settings"]'
    ).click()
    time.sleep(2)

    print("Typing Connection")
    UtilActionsGetElements.get_element_by_classname(
        driver=driver, classname="android.widget.EditText"
    ).send_keys("Connections")
    time.sleep(10)

    print("Clicking Connections")
    UtilActionsClick.click_on_loc(driver=driver, y_loc=403, x_loc=635)
    time.sleep(2)

    print("Clicking Flight mode")
    UtilActionsGetElements.get_element_by_xpath(
        driver=driver, xpath='//android.widget.Switch[@content-desc="Airplane mode"]'
    ).click()
    time.sleep(30)

    print("Turning off Flight mode")
    UtilActionsGetElements.get_element_by_xpath(
        driver=driver, xpath='//android.widget.Switch[@content-desc="Airplane mode"]'
    ).click()

    print("Going back to home")
    HelperKeycode.keycodeHome(driver=driver)


def setting_switch_wifi_4g(driver: WebDriver, mobile_data: bool):
    try:
        HelperKeycode.keycodeHome(driver=driver)
        time.sleep(1)

        print("Scrolling to settings")
        UtilActionsScroll.scroll_by_vertical(
            driver=driver, number_scroll=1, y_start=45, y_end=1200
        )
        time.sleep(2)

        print("Clicking settings")
        UtilActionsClick.click_on_loc(driver=driver, y_loc=215, x_loc=1002)
        time.sleep(2)

        print("Clicking search")
        search_button = UtilActionsGetElements.get_element_by_xpath(
            driver=driver,
            xpath='//android.widget.Button[@content-desc="Search settings"]',
        )
        if search_button:
            search_button.click()
        time.sleep(2)

        print("Typing Connection")
        search_input = UtilActionsGetElements.get_element_by_classname(
            driver=driver, classname="android.widget.EditText"
        )
        if search_input:
            search_input.send_keys("Connections")
        time.sleep(20)

        print("Clicking Connections")
        UtilActionsClick.click_on_loc(driver=driver, y_loc=403, x_loc=635)
        time.sleep(2)

        if mobile_data:
            print("Turning off Wi-Fi")
            wifi_switch = UtilActionsGetElements.get_element_by_xpath(
                driver=driver, xpath='//android.widget.Switch[@content-desc="Wi-Fi"]'
            )
            if wifi_switch:
                wifi_switch.click()

            print("Clicking Mobile network")
            mobile_network = UtilActionsGetElements.get_element_by_xpath(
                driver=driver,
                xpath='//android.widget.TextView[@resource-id="android:id/title" and @text="Data usage"]',
            )
            if mobile_network:
                mobile_network.click()
            time.sleep(2)

            print("Clicking Mobile data")
            btn_on = UtilActionsGetElements.get_element_by_xpath(
                driver=driver,
                xpath='(//android.widget.Switch[@resource-id="android:id/switch_widget"])[1]',
            )
            if btn_on:
                btn_on.click()
            time.sleep(2)

        try:
            open_connection = UtilActionsGetElements.get_element_by_xpath(
                driver=driver,
                xpath='//android.widget.TextView[@resource-id="android:id/summary" and @text="Connect to Wi-Fi networks."]',
            )

            if open_connection:
                print("Turning on Wi-Fi")
                wifi_switch = UtilActionsGetElements.get_element_by_xpath(
                    driver=driver,
                    xpath='//android.widget.Switch[@content-desc="Wi-Fi"]',
                )
                if wifi_switch:
                    wifi_switch.click()
            else:
                print("Wi-Fi is already on or connection option not found")
        except:
            print("Wi-Fi is already on or connection option not found")

        print("Going back to home")
        HelperKeycode.keycodeHome(driver=driver)
    except Exception as e:
        print(f"An error occurred: {e}")
