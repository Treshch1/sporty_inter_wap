from selenium.webdriver.firefox.webdriver import WebDriver

from page_objects.base_page import BasePage
from page_objects.header_page import HeaderPageObject
from page_objects.home_page import HomePageObject
from page_objects.search_list_page import SearchListPage
from page_objects.stream_page import StreamPage


class Application(BasePage):
    URL = ""

    def __init__(self, browser: WebDriver):
        super().__init__(browser)
        self.homepage = HomePageObject(browser)
        self.header = HeaderPageObject(browser)
        self.search_list = SearchListPage(browser)
        self.stream = StreamPage(browser)
