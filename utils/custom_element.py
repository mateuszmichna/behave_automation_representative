import time

from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

from utils.helpers import Helpers
from utils.settings.local_settings import EXPLICITLY_WAIT
from utils.settings.settings import LOCATOR_SEARCHING_METHOD


class CustomElement(WebElement):
    def __init__(self, driver, locator=None, locator_type=LOCATOR_SEARCHING_METHOD, wait=EXPLICITLY_WAIT, element_id=None,
                 w3c=False, is_visible=True):
        """
        :param driver: driver
        :param locator: "div[class*='something']"
        :param locator_type: By.XPATH (By can be imported from selenium.webdriver.common.by)
        :param element_id: if you have element from .find_element() method
                            you can put it here to convert to CustomElement object
        :param is_visible: true will cause that WebDriverWait will be looking for visible element,
                            with false WebdriverWait will be looking for element located in DOM
        """
        if locator and is_visible is False:
            element = WebDriverWait(driver, wait).until(
                ec.presence_of_element_located((locator_type, locator)))
            id_ = element.id
        elif locator:
            element = WebDriverWait(driver, wait).until(
                ec.visibility_of_element_located((locator_type, locator)))
            id_ = element.id
        else:
            id_ = element_id
        super().__init__(driver, id_, w3c)
        if not element_id:
            self.locator_type = locator_type
            self.locator = locator
        self.driver = driver

    def get_inner_element(self, locator, locator_type=LOCATOR_SEARCHING_METHOD):
        """
        :param locator: locator of inner element
        :param locator_type: locator type of inner element
        :return: element(CustomElement object) that is inside parent element
        """
        element = self.find_element(locator_type, locator)
        return CustomElement(self.driver, element_id=element.id)

    def get_inner_elements_list(self, locator, locator_type=LOCATOR_SEARCHING_METHOD):
        """
        The outcome of this method should be put into
        constructor of ElementsList in order to get access to proper methods
        :param locator: locator of inner element
        :param locator_type: locator type of inner element
        :return: list of elements(ElementsList object) that are inside parent element
        """
        return self.find_elements(locator_type, locator)

    def multiple_click(self, how_many_clicks):
        """
        Method that clicks several times in element
        :param how_many_clicks: number of clicks
        :return: self
        """
        for _ in range(how_many_clicks):
            self.click()
        return self

    def wait_for_clickable(self, wait=EXPLICITLY_WAIT):
        """
        Method that waits until the element will be clickable.
        :return: self
        """
        element = WebDriverWait(self.driver, wait).until(
            ec.element_to_be_clickable((self.locator_type, self.locator)))
        return CustomElement(self.driver, element_id=element.id)

    def delayed_wait_for_visibility(self, seconds=1, wait=EXPLICITLY_WAIT):
        """
        Method that waits fixed amount of time and then waits
        for a visible element based on original locator.
        :param seconds: amount of time in seconds to wait
        :return: visible element based on original locator
        """
        time.sleep(seconds)
        element = WebDriverWait(self.driver, wait).until(
            ec.visibility_of_element_located((self.locator_type, self.locator)))
        return CustomElement(self.driver, element_id=element.id)

    def delayed_wait_for_visibility_of_element(self, seconds=1, wait=EXPLICITLY_WAIT):
        """
        Method that waits fixed amount of time and then waits
        for a visible element based on an element id.
        :param seconds: amount of time in seconds to wait
        :return: visible element based on an element id
        """
        time.sleep(seconds)
        return WebDriverWait(self.parent, wait).until(ec.visibility_of(self))

    def wait_for_invisibility_of_element(self, wait=EXPLICITLY_WAIT):
        """
        Wait until previously found element become invisible based on element itself.
        """
        WebDriverWait(self.driver, wait).until(ec.invisibility_of_element(self))

    def wait_for_invisibility_of_locator(self, wait=EXPLICITLY_WAIT):
        """
        Wait until previously found element become invisible
        based on locator used previously to find origin element.
        """
        WebDriverWait(self.driver, wait).until(
            ec.invisibility_of_element_located((self.locator_type, self.locator)))

    def wait_for_staleness(self, wait=EXPLICITLY_WAIT):
        """
        Wait until previously found element is no longer attached to the DOM
        """
        WebDriverWait(self.driver, wait).until(ec.staleness_of(self))

    def send_keys_with_clear(self, text):
        """
        Clears the field and then send text.
        :param text: text to put in element
        :return: text
        """
        self.clear()
        self.send_keys(text)
        return text

    def click_clear_send_keys(self, text):
        """
        Click on field, clears the field and then send text.
        :param text: text to put in element
        :return: text
        """
        self.click()
        self.send_keys_with_clear(text)
        return text

    def click_clear_send_keys_enter(self, text):
        """
        Click on field, clears the field, send text and hit ENTER key.
        :param text: text to put in element
        :return: text
        """
        self.click()
        self.send_keys_with_clear(text)
        self.send_keys(Keys.ENTER)
        return text

    def hover_over(self):
        """
        Hover over the element
        """
        ActionChains(self.driver).move_to_element(self).perform()

    def get_numeric_from_element_text(self):
        """
        :return: Get text from the element and pulls numeric values out of it.
        """
        return Helpers().get_numeric_from_string(self.text)

    def get_numeric_from_element_attribute(self, attribute_name):
        """
        :param attribute_name: name of the attribute
        :return: Get text from the element's attribute and pulls numeric values out of it.
        """
        return Helpers().get_numeric_from_string(self.get_attribute(attribute_name))

    def parse_element_text(self, parsing_format, which_fragment):
        """
        Gets text from element and parses it in desired format.
        :param parsing_format: "{}: {}/{}"
                                from
                                "This is my score: 4/10"
                                results in dividing text like this:
                                "{This is my score}: {4}/{10}"
                                So we have three fragments: "This is my score", "4", and "10"
        :param which_fragment: index of a fragment we want to pull out
        :return: parsed text
        """
        return Helpers().parse_text(self.text, parsing_format, which_fragment)

    def parse_element_attribute(self, attribute_name, parsing_format, which_fragment):
        """
        Gets text from element's attribute and parses it in desired format.
        :param attribute_name: name of attribute to parse
        :param parsing_format: "{}: {}/{}"
                                from
                                "This is my score: 4/10"
                                results in dividing text like this:
                                "{This is my score}: {4}/{10}"
                                So we have three fragments: "This is my score", "4", and "10"
        :param which_fragment: index of a fragment we want to pull out
        :return: parsed text
        """
        return Helpers().parse_text(self.get_attribute(attribute_name), parsing_format, which_fragment)

    def set_atribute_value_via_js(self, value_to_set, atribute_to_set):
        """
        Sets attribute to desired value using js command.
        """
        element = self.driver.create_web_element(self.id)
        return self.driver.execute_script(f"arguments[0].setAttribute('{atribute_to_set}', '{value_to_set}');", element)

    def send_keys_to_code_mirror_element_via_js(self, value_to_enter):
        """
        Sends keys to the element using js command.
        """
        element = self.driver.create_web_element(self.id)
        return self.driver.execute_script(f"arguments[0].CodeMirror.setValue('{value_to_enter}');", element)

    def click_via_js(self):
        """
        Clicks element using js command.
        """
        element = self.driver.create_web_element(self.id)
        return self.driver.execute_script("arguments[0].click();", element)

    def open_link_in_new_tab(self):
        return ActionChains(self.driver).key_down(Keys.CONTROL).click(self).key_up(Keys.CONTROL).perform()
