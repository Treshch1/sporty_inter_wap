from components.text_input import TextInput
from page_objects.base_page import BasePage, Element, Elements


class HeaderPageObject(BasePage):

    search_button = Element('a[aria-label="Search"]')
    search_input = TextInput(input_field=Element('input[type="search"]'))
    suggestions_items = Elements('li a.tw-link')

    def search_and_select_first_search_item(self, search_text):
        self.search_button.click()
        self.search_input.set_value(search_text)
        # Wait for all search elements loading
        self.wait(lambda b: self.suggestions_items.count() > 1)
        self.suggestions_items.element_with_text(search_text).click()
