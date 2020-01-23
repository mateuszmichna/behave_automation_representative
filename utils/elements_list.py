import random
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

from utils.custom_element import CustomElement
from utils.settings.local_settings import EXPLICITLY_WAIT


class ElementsList(list):
    def __init__(self, driver, locator=None, locator_type=By.CSS_SELECTOR, wait=EXPLICITLY_WAIT, elements_list=None,
                 is_visible=True):
        """
        Each object of this class is will be a list of CustomElements objects based on given locator.
        :param driver: driver
        :param locator: "div[class*='something']"
        :param locator_type: By.XPATH (By can be imported from selenium.webdriver.common.by)
        :param elements_list: if you have elements_list from .find_elements()
                                method you can put them here to convert to ElementsList object
        :param is_visible: true will cause that WebDriverWait will be looking for any visible elements,
                            with false WebdriverWait will be looking for elements located in DOM
        """
        super().__init__()
        if elements_list:
            elements = elements_list
        elif is_visible is False:
            elements = WebDriverWait(driver, wait).until(
                ec.presence_of_all_elements_located((locator_type, locator)))
        else:
            elements = WebDriverWait(driver, wait).until(
                ec.visibility_of_any_elements_located((locator_type, locator)))
        for element in elements:
            self.append(CustomElement(driver, element_id=element.id))
        if not elements_list:
            self.locator_type = locator_type
            self.locator = locator
        self.driver = driver

    def click_all_elements(self):
        """
        This method clicks on each element on list.
        :return: self (ElementsList)
        """
        for element in self:
            element.click()
        return self

    def get_nth_element(self, which_element: int) -> CustomElement:
        """
        :return: returns element with desired index (CustomElement object)
        """
        return self[which_element - 1]

    def get_random_elements(self, number_of_elements: int):
        """
        :param number_of_elements: how many elements should be returned
        :return: ElementsList object containing 3 random elements from origin list
        """
        custom_list_length = len(self)
        if number_of_elements > custom_list_length:
            number_of_elements = custom_list_length
        random_list = random.sample(self, number_of_elements)
        return ElementsList(self.driver, elements_list=random_list)

    def wait_for_all_elements_visibility(self, wait=EXPLICITLY_WAIT):
        """
        Additional wait where all elements of given locator are visible.
        :return: ElementsList object
        """
        elements_list = WebDriverWait(self.driver, wait).until(
            ec.visibility_of_all_elements_located((self.locator_type, self.locator)))
        return ElementsList(self.driver, elements_list=elements_list)

    def delayed_wait_for_any_element_visibility(self, delay: int = 1, wait=EXPLICITLY_WAIT):
        """
        This is additional WebdriverWait mixed with time.sleep() wait.
        Sometimes occurs situation when part of elements of some locator are rendered,
        but this is not a full list of them. So we want to wait for first ones,
        and then wait some more time for the rest of them.
        :param delay: number of seconds to wait between two WebdriverWaits
        :return: ElementsList object
        """
        WebDriverWait(self.driver, wait).until(
            ec.visibility_of_any_elements_located((self.locator_type, self.locator)))
        time.sleep(delay)
        elements_list = WebDriverWait(self.driver, wait).until(
            ec.visibility_of_any_elements_located((self.locator_type, self.locator)))
        return ElementsList(self.driver, elements_list=elements_list)

    def get_random_element(self) -> CustomElement:
        """
        :return: single, random CustomElement object from origin list
        """
        return random.choice(self)

    def get_attributes_list(self, attribute):
        """
        :param attribute: attribute name like "class", "id", "href", "aria-label"
        :return: list of strings when each string is a value from desired attribute of each element from origin list
        """
        return [element.get_attribute(attribute) for element in self]

    def get_texts_list(self):
        """
        :return: list of strings when each string is a text of each element from origin list
        """
        return [element.text for element in self]

    def get_length(self):
        """
        :return: length of the list
        """
        return len(self)

    def get_element_by_text(self, given_text) -> CustomElement:
        """
        :param given_text: text to find in elements
        :return: First element from list that has in its text given value.
        """
        text_list = []
        for element in self:
            text_list.append(element.text)
            if element.text == given_text:
                return element
        raise Exception(f"Wrong object name. We needed {given_text}, but list contains only values: {text_list}")

    def get_elements_by_text(self, given_text):
        """
        :param given_text: text to find in elements
        :return: List of elements (ElementsList object) that have in its text given value.
        """
        elements_list = []
        text_list = []
        for element in self:
            text_list.append(element.text)
            if element.text == given_text:
                elements_list.append(element)
        if not self:
            raise Exception("List is empty so we can't take text from anything.")
        if not elements_list:
            raise Exception(f"Wrong object name. We needed {given_text}, but list contains only values: {text_list}")
        return ElementsList(self.driver, elements_list=elements_list)

    def get_element_by_attribute(self, attribute, given_attribute, partial_value=False) -> CustomElement:
        """
        :param attribute: attribute name in which we will search given value
        :param given_attribute: attribute value to search
        :param partial_value: if False we search for perfect match of an attribute
                                if True we search for given text in an attribute
        :return: First element from list (CustomElement object) that has desired value in specified attribute
        """
        text_list = []
        if partial_value is True:
            for element in self:
                text_list.append(element.text)
                element_attribute = element.get_attribute(attribute).replace('"', '')
                if given_attribute in element_attribute:
                    return element
        else:
            for element in self:
                text_list.append(element.text)
                element_attribute = element.get_attribute(attribute).replace('"', '')
                if given_attribute == element_attribute:
                    return element
        raise Exception(f"Wrong object name. We needed {given_attribute}, but list contains only values: {text_list}")

    def get_elements_by_attribute(self, attribute, given_attribute, partial_value=False):
        """
        :param attribute: attribute name in which we will search given value
        :param given_attribute: attribute value to search
        :param partial_value: if False we search for perfect match of an attribute
                                if True we search for given text in an attribute
        :return: ElementsList object that contains elements with desired value in specified attribute
        """
        elements_list = []
        if partial_value is True:
            for element in self:
                element_attribute = element.get_attribute(attribute).replace('"', '')
                if given_attribute in element_attribute:
                    elements_list.append(element)
            return ElementsList(self.driver, elements_list=elements_list)
        else:
            for element in self:
                element_attribute = element.get_attribute(attribute).replace('"', '')
                if given_attribute == element_attribute:
                    elements_list.append(element)
            return ElementsList(self.driver, elements_list=elements_list)

    def get_element_by_inner_text(self, given_text, inner_locator, locator_type=By.CSS_SELECTOR,
                                  partial_value=False) -> CustomElement:
        """
        :param given_text: text to find in inner element
        :param inner_locator: locator of inner element of a parent element
        :param locator_type: locator type of inner element
        :param partial_value: if False we search for perfect match of an attribute
                                if True we search for given text in an attribute
        :return: First element from list that has in its inner element text with given value.
        """
        text_list = []
        if partial_value is True:
            for element in self:
                inner_element = element.get_inner_element(inner_locator, locator_type)
                text_list.append(inner_element.text)
                if given_text in inner_element.text:
                    return element
        else:
            for element in self:
                inner_element = element.get_inner_element(inner_locator, locator_type)
                text_list.append(inner_element.text)
                if given_text == inner_element.text:
                    return element
        raise Exception(f"Wrong object name. We needed {given_text}, but list contains only values: {text_list}")

    def get_elements_by_inner_text(self, given_text, inner_locator, locator_type=By.CSS_SELECTOR, partial_value=False):
        """
        :param given_text: text to find in inner elements
        :param inner_locator: locator of inner element of a parent element
        :param locator_type: locator type of inner element
        :param partial_value: if False we search for perfect match of an attribute
                                if True we search for given text in an attribute
        :return: List of elements (ElementsList object) that have in its inner element text with given value.
        """
        elements_list = []
        if partial_value is True:
            for element in self:
                inner_element = element.get_inner_element(inner_locator, locator_type)
                if given_text in inner_element.text:
                    elements_list.append(element)
        else:
            for element in self:
                inner_element = element.get_inner_element(inner_locator, locator_type)
                if given_text == inner_element.text:
                    elements_list.append(element)
        return ElementsList(self.driver, elements_list=elements_list)

    def get_element_by_inner_attribute(self, attribute, given_attribute, inner_locator,
                                       locator_type=By.CSS_SELECTOR, partial_value=False) -> CustomElement:
        """
        :param attribute: attribute name in which we will search given value
        :param given_attribute: attribute value to search
        :param inner_locator: locator of inner element of a parent element
        :param locator_type: locator type of inner element
        :param partial_value: if False we search for perfect match of an attribute
                                if True we search for given text in an attribute
        :return: First element from list (CustomElement object),
                that haa inner element with desired value in specified attribute
        """
        text_list = []
        if partial_value is True:
            for element in self:
                inner_element = element.get_inner_element(inner_locator, locator_type)
                inner_element_attribute = inner_element.get_attribute(attribute).replace('"', '')
                text_list.append(inner_element_attribute)
                if given_attribute in inner_element_attribute:
                    return element
        else:
            for element in self:
                inner_element = element.get_inner_element(inner_locator, locator_type)
                inner_element_attribute = inner_element.get_attribute(attribute).replace('"', '')
                text_list.append(inner_element_attribute)
                if given_attribute == inner_element_attribute:
                    return element
        raise Exception(f"Wrong object name. We needed {given_attribute}, but list contains only values: {text_list}")

    def get_elements_by_inner_attribute(self, attribute, given_attribute, inner_locator, locator_type=By.CSS_SELECTOR,
                                        partial_value=False):
        """
        :param attribute: attribute name in which we will search given value
        :param given_attribute: attribute value to search
        :param inner_locator: locator of inner element of a parent element
        :param locator_type: locator type of inner element
        :param partial_value: if False we search for perfect match of an attribute
                                if True we search for given text in an attribute
        :return: List of elements (CustomElement object),
                that have inner element with desired value in specified attribute
        """
        elements_list = []
        if partial_value is True:
            for element in self:
                inner_element = element.get_inner_element(inner_locator, locator_type)
                inner_element_attribute = inner_element.get_attribute(attribute).replace('"', '')
                if given_attribute in inner_element_attribute:
                    elements_list.append(element)
        else:
            for element in self:
                inner_element = element.get_inner_element(inner_locator, locator_type)
                inner_element_attribute = inner_element.get_attribute(attribute).replace('"', '')
                if given_attribute == inner_element_attribute:
                    elements_list.append(element)
        return ElementsList(self.driver, elements_list=elements_list)

    def get_inner_elements_list(self, inner_locator, locator_type=By.CSS_SELECTOR):
        """
        :param inner_locator: locator of inner element of a parent element
        :param locator_type: locator of inner element of a parent element
        :return: list of inner elements for each element from parent list
        """
        elements_list = []
        for element in self:
            inner_element = element.get_inner_element(inner_locator, locator_type)
            elements_list.append(inner_element)
        return ElementsList(self.driver, elements_list=elements_list)
