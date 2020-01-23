import os

from selenium import webdriver

from utils.settings.settings import PATH_TO_PROJECT, DRIVER, IMPLICITLY_WAIT


class FirefoxBrowser:

    def __init__(self):
        firefox_binary = "C:/Program Files/Mozilla Firefox/firefox.exe"
        driver_path = os.path.join(PATH_TO_PROJECT, 'utils', 'drivers', DRIVER)
        os.chmod(driver_path, 755)
        self.driver = webdriver.Firefox(executable_path=driver_path, firefox_binary=firefox_binary)
        self.set_up_browser()

    def set_up_browser(self):
        self.driver.maximize_window()
        self.driver.implicitly_wait(IMPLICITLY_WAIT)

    def close(self):
        self.driver.close()

