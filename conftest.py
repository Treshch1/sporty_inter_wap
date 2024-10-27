import allure
import pytest

from browsers import ChromeBrowser
from config import BROWSER_TYPE
from env import SCREENS_PATH
from page_objects.application import Application


@pytest.fixture(scope="session")
def browser(request):
    headless = True if request.config.getoption("--headless") else False
    if BROWSER_TYPE == "chromium":
        browser = ChromeBrowser(headless=headless).get_browser()
    else:
        assert False, "Unsupported browser type"
    yield browser
    browser.quit()


@pytest.fixture(scope="session")
def app(browser):
    _app = Application(browser)
    return _app


def pytest_addoption(parser):
    parser.addoption("--headless", action="store_true", default=False)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item):
    outcome = yield
    result = outcome.get_result()
    if (result.when == "call" or result.when == "setup") and (result.failed or result.skipped):
        try:
            if "app" in item.fixturenames:
                web_driver = item.funcargs["app"]
            else:
                print("Fail to take screenshot: no driver fixture found")
                return
            web_driver.browser.save_screenshot(str(SCREENS_PATH.path(item.name)) + ".png")
            allure.attach.file(
                str(SCREENS_PATH.path(item.name)) + ".png",
                name="Screenshot captured",
                attachment_type=allure.attachment_type.PNG,
            )
        except Exception as e:
            print("Failed to take screenshot: {}".format(e))
