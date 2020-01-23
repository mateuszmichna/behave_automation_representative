import os

from selenium import webdriver

from utils.settings.settings import PATH_TO_PROJECT, DRIVER, IMPLICITLY_WAIT


class EdgeBrowser:

    def __init__(self):
        driver_path = ''
        os.chmod(driver_path, 755)
        self.driver = webdriver.Edge(executable_path=driver_path, )
        self.set_up_browser()

    def set_up_browser(self):
        self.driver.maximize_window()
        self.driver.implicitly_wait(IMPLICITLY_WAIT)

    def close(self):
        self.driver.close()
