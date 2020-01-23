import os

from selenium import webdriver
from utils.settings.settings import PATH_TO_PROJECT, DRIVER, IMPLICITLY_WAIT


class ChromeBrowser:
    def __init__(self):
        driver_path = os.path.join(PATH_TO_PROJECT, 'utils', 'drivers', DRIVER)
        os.chmod(driver_path, 755)
        self.set_up_browser()
        self.driver = webdriver.Chrome(options=self.options, executable_path=driver_path)
        if DRIVER == "chromedriver":
            self.driver.fullscreen_window()
        self.driver.implicitly_wait(IMPLICITLY_WAIT)

    def set_up_browser(self):
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('start-maximized')
        self.options.add_argument('disable-infobars')

    def close(self):
        self.driver.close()
