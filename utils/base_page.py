import time
from urllib.parse import urlparse

from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from utils.custom_element import CustomElement
from utils.elements_list import ElementsList
from utils.settings.local_settings import EXPLICITLY_WAIT
from utils.settings.settings import LOCATOR_SEARCHING_METHOD


class BasePage(object):

    def __init__(self, driver: WebDriver):
        self.driver = driver

    # -------------------------------------------------------------------------------------------------------
    # elements
    def get_element(self,
                    locator=None,
                    locator_type=LOCATOR_SEARCHING_METHOD,
                    element_id=None,
                    w3c=False,
                    is_visible=True):
        """
        :param locator: "div[class*='something']"
        :param locator_type: By.XPATH (By can be imported from selenium.webdriver.common.by)
        :param element_id: if you have element from .find_element() method
                          you can put it here to convert to CustomElement object
        :param is_visible: true will cause that WebDriverWait will be looking for visible element,
                          with false WebdriverWait will be looking for element located in DOM
        :return: CustomElement object
        """
        return CustomElement(self.driver, locator=locator, locator_type=locator_type,
                             element_id=element_id, w3c=w3c, is_visible=is_visible)

    def get_elements_list(self,
                          locator=None,
                          locator_type=LOCATOR_SEARCHING_METHOD,
                          elements_list=None,
                          is_visible=True):
        """
        :param locator: "div[class*='something']"
        :param locator_type: By.XPATH (By can be imported from selenium.webdriver.common.by)
        :param elements_list: if you have elements_list from .find_elements()
                              method you can put them here to convert to ElementsList object
        :param is_visible: true will cause that WebDriverWait will be looking for any visible elements,
                          with false WebdriverWait will be looking for elements located in DOM
        :return: ElementsList object
        """
        return ElementsList(self.driver, locator=locator, locator_type=locator_type,
                            elements_list=elements_list, is_visible=is_visible)

    def get_element_by_xpath_text(self, partial_xpath_locator, text, is_visible=True):
        """
        !!!This is only for use in case when we need to handle multiple elements defined by one locator,
        but with different text value in them.!!!

        :param partial_xpath_locator: '//div' or '//div[contains(@class, "button")]//span
        :param text: text to search for in elements defined by locator
        :param is_visible: true will cause that WebDriverWait will be looking for visible element,
                          with false WebdriverWait will be looking for element located in DOM
        :return: CustomElement object
        """
        locator = f'{partial_xpath_locator}[contains(text(), "{text}")]'
        return CustomElement(self.driver, locator=locator, locator_type=By.XPATH, is_visible=is_visible)

    # -------------------------------------------------------------------------------------------------------
    # page
    def get_page(self, url):
        """
        Opens desired url
        """
        self.driver.get(url)
        return url

    def refresh_page(self):
        """
        Refreshes the page
        """
        self.driver.refresh()

    def back_page(self):
        """
        Simulates clicking on a browser back button.
        """
        self.driver.back()

    # -------------------------------------------------------------------------------------------------------
    # url
    def read_page_url(self):
        """
        Gets current url as a string
        """
        return self.driver.current_url

    def parse_current_url(self):
        """
        Parse current URL into 6 components:
        <scheme>://<netloc>/<path>;<params>?<query>#<fragment>
        :return: a 6-tuple: (scheme, netloc, path, params, query, fragment).
        """
        url = self.read_page_url()
        return urlparse(url)

    def read_page_netloc_from_current_url(self):
        """
        :return: a string with netloc from current url: i.e. "automationpractice.com"
        """
        parsed_url = self.parse_current_url()
        return parsed_url.netloc

    @staticmethod
    def read_page_netloc_from_given_url(given_url):
        """
        :return: a string with netloc from given url:
                i.e. "dev.lifecents.com" from "http://automationpractice.com/"
        """
        parsed_url = urlparse(given_url)
        return parsed_url.netloc

    def read_page_path_from_current_url(self):
        """
        :return: a string with path from current url:
                i.e. "/index.php?id_category=8&controller=category"
                from "http://automationpractice.com/index.php?id_category=8&controller=category"
        """
        parsed_url = self.parse_current_url()
        return parsed_url.path

    def get_last_nth_chars_from_url(self, nth):
        """
        :return: a string with last nth characters from current url:
        """
        return self.read_page_url()[-nth:]

    # -------------------------------------------------------------------------------------------------------
    # windows and tabs
    def set_tab(self, window_index):
        """
        :param window_index: which window we want to set
        :return: window object that we can switch to using switch_to_tab method
        """
        test = self.driver.window_handles[window_index]
        return test

    def switch_to_tab(self, which_tab):
        """
        :param which_tab: window object that we want to switch to
        """
        return self.driver.switch_to_window(which_tab)

    def open_new_tab(self):
        """
        Opens a new tab using js command
        """
        return self.driver.execute_script("window.open()")

    def close_current_tab(self):
        """
        Closes currently open and focused tab
        """
        return self.driver.close()

    def open_new_tab_and_close_previous(self):
        """
        Opens a new tab and closes previously focused tab
        """
        self.open_new_tab()
        new_window = self.set_tab(1)
        self.close_current_tab()
        return self.switch_to_tab(new_window)

    def set_focus_on_first_tab(self):
        """
        Set focus on first tab if there is more than one.
        """
        if len(self.driver.window_handles) > 1:
            first_tab = self.set_tab(0)
            self.switch_to_tab(first_tab)

    # -------------------------------------------------------------------------------------------------------
    # waits

    # wait below should be remove from properly built test
    @staticmethod
    def waits(seconds):
        """
        Using this there is no need to import time library each time.
        :param seconds: how many seconds should wait
        """
        return time.sleep(seconds)

    def wait_for_number_of_tabs(self, number_of_tabs, wait=EXPLICITLY_WAIT):
        """
        Waits for certain number of tabs in the browser
        :param number_of_tabs: on how many tabs have to wait
        """
        return WebDriverWait(self.driver, wait).until(EC.number_of_windows_to_be(number_of_tabs))

    def wait_for_url_to_appear(self):
        """
        Sometimes page opens, but if we read url it will be empty string.
        This method waits until the url will be present.
        """
        url = ""
        while url == "":
            url = self.read_page_netloc_from_current_url()
            self.waits(0.1)

    # -------------------------------------------------------------------------------------------------------
    # sets
    def send_special_key(self, key):
        """
        Method for sending special keys such as ENTER, TAB, PAGE_UP, PAGE_DOWN etc.
        :param key: Key in format Keys.ENTER or Keys.TAB
                    (Keys can be imported from selenium.webdriver.common.keys)
        """
        ActionChains(self.driver).send_keys(key).perform()

    # -------------------------------------------------------------------------------------------------------
    # others
    @staticmethod
    def convert_empty_value_in_string(string):
        """
        This method converts "empty" string to empty string "".
        This is a method for use in behave steps implementation,
        when we want to have empty value in example table.
        Behave doesn't support leaving cell in example table empty.
        :param string: string to convert
        :return: string value after "parsing"
        """
        if string == "empty":
            string = ""
        return string

    # -------------------------------------------------------------------------------------------------------
    # scrolls

    def scroll_to_position(self, position):
        return self.driver.execute_script("window.scrollTo(0, %s);" % position)

    def scroll_to_element(self, element):
        return self.driver.execute_script("return arguments[0].scrollIntoView();", element)

    def scroll_to_bottom(self):
        return self.scroll_to_position('document.body.scrollHeight')

    def scroll_to_top(self):
        return self.scroll_to_position(0)

    def scroll_by(self, by):
        return self.driver.execute_script("window.scrollBy(0, {}); return window.scrollY;".format(by))
