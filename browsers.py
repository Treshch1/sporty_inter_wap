from selenium.webdriver import Chrome, Firefox
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions


class ChromeBrowser:
    def __init__(self, headless=False):
        self.headless = headless
        self.browser = None

    def get_browser(self) -> Chrome:
        options = ChromeOptions()
        mobile_emulation = {"deviceName": "iPhone 12 Pro",}
        options.add_experimental_option("mobileEmulation", mobile_emulation)

        if self.headless:
            options.add_argument("--headless")
            # 2 arguments below are needed to run tests in docker environment
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            self.browser = Chrome(options=options)
        else:
            self.browser = Chrome(options=options)
            self.browser.maximize_window()

        self.browser.set_page_load_timeout(30)
        return self.browser
