import time
from appium.webdriver.webdriver import WebDriver
from utils.actions import UtilActionsClick


def keycodeHome(driver: WebDriver):
    print("---> Click home <---")
    UtilActionsClick.click_on_loc(driver=driver, x_loc=540, y_loc=2280)


def keycodeMoveBack(driver: WebDriver):
    print("---> Click move back <---")
    UtilActionsClick.click_on_loc(driver=driver, x_loc=820, y_loc=2280)
    time.sleep(1)


def keycodePaste(driver: WebDriver):
    print("---> Paste content <---")
    time.sleep(1)
    driver.press_keycode(279)
    time.sleep(1)


def keycodeEnter(driver: WebDriver):
    print("---> Click enter <---")
    time.sleep(1)
    driver.press_keycode(66)
    time.sleep(1)


def keycodeRemove(driver: WebDriver):
    print("---> Remove text <---")
    time.sleep(1)
    driver.press_keycode(67)
    time.sleep(1)


def keycodeSwitch(driver: WebDriver):
    print("---> Click switch for clear <---")
    time.sleep(1)
    driver.press_keycode(187)
    time.sleep(1)


def keycodeExitApp(driver: WebDriver):
    keycodeHome(driver=driver)
    keycodeHome(driver=driver)


# Clear all application on the phone
def keycodeClearApp(driver: WebDriver):
    print("Go to home screen")
    keycodeHome(driver=driver)
    print("Clear phone applications")
    keycodeSwitch(driver=driver)
    UtilActionsClick.click_on_loc(driver=driver, y_loc=1815)
    keycodeMoveBack(driver=driver)
