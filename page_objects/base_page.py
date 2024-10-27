import time
import urllib

from typing import Union

from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common import by
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from config import BASE_URL
from custom_expected_conditions import wait_is_clickable_and_click


WAIT_TIME_DEFAULT = 5  # in seconds


class BaseComponent:
    def __get__(self, obj: Union["BasePage", "BaseComponent"], objtype=None):
        if isinstance(obj, BasePage):
            self.page = obj
        elif isinstance(obj, BaseComponent):
            self.page = obj.page
        return self

    def __getattribute__(self, item):
        attr = super().__getattribute__(item)
        if isinstance(attr, (Element, Elements, BaseComponent)):
            attr.page = self.page
        return attr

    def wait(self, body, timeout=5):
        return WebDriverWait(self.page.browser, timeout).until(body)


class Element:
    By = by.By  # Just a shortcut

    def __init__(self, value, by=By.CSS_SELECTOR, wait=WAIT_TIME_DEFAULT):
        self.value = value
        self.by = by
        self.wait = wait

    def __get__(self, obj: Union["BasePage", BaseComponent], objtype=None):
        if isinstance(obj, BasePage):
            self.page = obj
        elif isinstance(obj, BaseComponent):
            self.page = obj.page
        return self

    def _find_element(self, page, timeout):
        timeout = timeout if timeout is not None else self.wait
        if timeout:
            return WebDriverWait(page.browser, timeout).until(
                expected_conditions.presence_of_element_located((self.by, self.value))
            )
        else:
            return page.browser.find_element(by=self.by, value=self.value)

    def find(self, *, timeout=None):
        return self._find_element(self.page, timeout)

    def click(self, *, timeout=None, timeout_before_click=None, timeout_after_click=None):
        """
        wait_is_clickable_and_click fixed random failed tests which are affected by some objects
        that appears for small amount of time during clicking some elements
        Example: clicking elements in the result list can be blocked by the spinner displaying
        """
        timeout = timeout if timeout is not None else self.wait

        try:
            element = self.find(timeout=timeout)
            if timeout_before_click:
                time.sleep(timeout_before_click)
            WebDriverWait(self.page.browser, timeout).until(wait_is_clickable_and_click(element=element))
        except StaleElementReferenceException:
            self.click(timeout=timeout)

        if timeout_after_click:
            time.sleep(timeout_after_click)

    def clear(self, *, timeout=None):
        self.find(timeout=timeout).clear()

    def send_keys(self, value, *, timeout=None):
        self.find(timeout=timeout).send_keys(value)

    def is_selected(self, *, timeout=None):
        """
        Sometimes element that has been found is not present on the page anymore due to FE components updating
        this timing issue is fixed by handling StaleElementReferenceException and trying the same action again
        """
        try:
            return self.find(timeout=timeout).is_selected()
        except StaleElementReferenceException:
            return self.is_selected(timeout=timeout)

    def is_displayed(self, *, timeout=None):
        """
        Sometimes element that has been found is not present on the page anymore due to FE components updating
        this timing issue is fixed by handling StaleElementReferenceException and trying the same action again
        """
        try:
            return self.find(timeout=timeout).is_displayed()
        except StaleElementReferenceException:
            return self.is_displayed(timeout=timeout)

    def find_element_by_id(self, id_selector, *, timeout=None):
        return self.find(timeout=timeout).find_element_by_id(id_selector)

    def find_element_by_xpath(self, xpath, *, timeout=None):
        try:
            return self.find(timeout=timeout).find_element_by_xpath(xpath)
        except StaleElementReferenceException:
            return self.find_element_by_xpath(xpath, timeout=timeout)

    def find_elements_by_xpath(self, xpath, *, timeout=None):
        return self.find(timeout=timeout).find_elements_by_xpath(xpath)

    def find_element_by_css_selector(self, css_selector, *, timeout=None):
        try:
            return self.find(timeout=timeout).find_element_by_css_selector(css_selector)
        except StaleElementReferenceException:
            return self.find_element_by_css_selector(css_selector, timeout=timeout)

    def find_elements_by_css_selector(self, css_selector, *, timeout=None):
        return self.find(timeout=timeout).find_elements_by_css_selector(css_selector)

    def get_attribute(self, name, *, timeout=None):
        try:
            return self.find(timeout=timeout).get_attribute(name)
        except StaleElementReferenceException:
            return self.get_attribute(name, timeout=timeout)

    def hover(self, *, timeout=None):
        hover = ActionChains(self.page.browser).move_to_element(self.find(timeout=timeout))
        hover.perform()

    def is_element_exists(self, *, timeout=0):
        try:
            self.find(timeout=timeout)
        except (NoSuchElementException, TimeoutException):
            return False
        return True

    def is_clickable(self, *, timeout=0):
        # Check that element exists
        self.find(timeout=timeout)
        try:
            self.click(timeout=timeout)
        except TimeoutException:
            return False
        return True

    def is_enabled(self, *, timeout=None):
        return self.find(timeout=timeout).is_enabled()

    def click_with_offset(self, *, xoffset: int, yoffset: int, timeout=None):
        builder = (
            ActionChains(self.page.browser)
            .move_to_element_with_offset(to_element=self.find(timeout=timeout), xoffset=xoffset, yoffset=yoffset)
            .click()
        )
        builder.perform()

    def scroll_to_element(self, top=True, timeout=None):
        self.page.browser.execute_script(
            f'arguments[0].scrollIntoView({"true" if top else "false"});', self.find(timeout=timeout)
        )

    def waiting(self, body, timeout=5):
        return WebDriverWait(self.page.browser, timeout).until(body)

    @property
    def text(self):
        """
        To text with other timeout settings use next construction in tests
        element.find(timeout=needed_timeout).text

        Sometimes element that has been found is not present on the page anymore due to FE components updating
        this timing issue is fixed by handling StaleElementReferenceException and trying the same action again
        """
        try:
            return self.find(timeout=10).text
        except StaleElementReferenceException:
            return self.find(timeout=10).text

    @property
    def size(self):
        return self.find(timeout=10).size


class Elements:
    By = by.By  # Just a shortcut

    def __init__(self, value, by=By.CSS_SELECTOR, wait=WAIT_TIME_DEFAULT):
        self.value = value
        self.by = by
        self.wait = wait

    def __get__(self, obj: Union["BasePage", BaseComponent], objtype=None):
        if isinstance(obj, BasePage):
            self.page = obj
        elif isinstance(obj, BaseComponent):
            self.page = obj.page
        return self

    def _find_elements(self, page, timeout):
        timeout = timeout if timeout is not None else self.wait
        if timeout:
            try:
                WebDriverWait(page.browser, timeout).until(
                    expected_conditions.presence_of_element_located((self.by, self.value))
                )
                return page.browser.find_elements(by=self.by, value=self.value)
            except TimeoutException:
                return []
        else:
            return page.browser.find_elements(by=self.by, value=self.value)

    def find(self, *, timeout=None):
        return self._find_elements(self.page, timeout)

    def find_displayed(self, *, timeout=None):
        displayed_list = []
        for element in self.find(timeout=timeout):
            if element.is_displayed():
                displayed_list.append(element)
        return displayed_list

    def count(self, *, timeout=None):
        return len(self.find(timeout=timeout))

    def count_displayed(self, *, timeout=None):
        return len(self.find_displayed(timeout=timeout))

    def element_with_text(self, text, timeout=None):
        for element in self.find(timeout=timeout):
            if element.text == text:
                return element

    @property
    def first_element(self):
        element = Element(self.value, self.by, self.wait)
        element.page = self.page
        return element

    @property
    def first_visible_element(self):
        for element in self.find():
            if element.is_displayed():
                return element


class BasePage:
    def __init__(self, browser: WebDriver):
        self.browser = browser
        self.page = self

    def __getattribute__(self, item):
        attr = super().__getattribute__(item)
        if isinstance(attr, (Element, Elements, BaseComponent)):
            attr.page = self.page
        return attr

    def visit(self, **kwargs):
        if kwargs:
            query_params_string = "?" + urllib.parse.urlencode(kwargs, doseq=True)
        else:
            query_params_string = ""
        self.browser.get(BASE_URL + self.URL + query_params_string)

    def wait(self, body, timeout=5):
        return WebDriverWait(self.browser, timeout).until(body)
