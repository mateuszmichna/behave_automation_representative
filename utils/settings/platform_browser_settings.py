import sys

from selenium.webdriver.common.by import By

from utils.settings.local_settings import SELECTED_BROWSER

LINUX_PLATFORM = 'Linux'
MACOS_PLATFORM = 'OS X'
WINDOWS_PLATFORM = 'Windows'
DRIVERS = {
    LINUX_PLATFORM: {
        'chrome': 'chromedriver',
        'firefox': 'geckodriver',
        'edge': 'msedgedriver',
    },
    MACOS_PLATFORM: {
        'chrome': 'chromedriver',
        'firefox': 'geckodriver',
        'edge': 'msedgedriver',
    },
    WINDOWS_PLATFORM: {
        'chrome': 'chromedriver.exe',
        'firefox': 'geckodriver.exe',
        'edge': 'msedgedriver.exe',
    },
}


def get_platform():
    platforms = {
        'linux1': LINUX_PLATFORM,
        'linux2': LINUX_PLATFORM,
        'darwin': MACOS_PLATFORM,
        'win32': WINDOWS_PLATFORM
    }
    if sys.platform not in platforms:
        return sys.platform

    return platforms[sys.platform]


def get_browser():
    if SELECTED_BROWSER == '':
        raise Exception('Browser not specified in platform_browser_settings.py')
    if SELECTED_BROWSER == 'chrome' or SELECTED_BROWSER == 'edge' or SELECTED_BROWSER == 'firefox':
        pass

    else:
        raise Exception('Wrong name of browser in platform_browser_settings.py')
    return SELECTED_BROWSER


def get_driver_by_platform_name_and_browser(platform_name, browser):
    driver = DRIVERS.get(platform_name, {}).get(browser)
    if not driver:
        raise Exception("Couldn't find a driver")
    return driver


def get_preferable_locator_searching_method(method):
    methods = {
        "id": By.ID,
        "xpath": By.XPATH,
        "link text": By.LINK_TEXT,
        "partial link text": By.PARTIAL_LINK_TEXT,
        "name": By.NAME,
        "tag name": By.TAG_NAME,
        "class name": By.CLASS_NAME,
        "css selector": By.CSS_SELECTOR,
    }
    return methods[method]
