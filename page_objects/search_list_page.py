import time
import random

from page_objects.base_page import BasePage, Elements


class SearchListPage(BasePage):
    articles = Elements('article')
    aspect = Elements('.tw-aspect')

    def smooth_scroll(self, x=0, y=500):
        for i in range(x, y, 50):
            self.browser.execute_script(f"window.scrollTo(0, {i});")
            time.sleep(0.05)

    def wait_for_page_loading(self):
        self.wait(lambda b: self.articles.find())

    def open_random_streamer(self):
        random.choice(self.articles.find()).click()
