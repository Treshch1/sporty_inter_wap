from page_objects.base_page import BasePage, Element


class StreamPage(BasePage):
    loading_spinner = Element('div.tw-loading-spinner')
    start_watching_button = Element('[data-a-target="content-classification-gate-overlay-start-watching-button"]')
    chat_section = Element('[data-test-selector="chat-scrollable-area__message-container"]')

    def wait_for_video_loading(self):
        self.wait(lambda b: self.chat_section.is_displayed())
        if self.start_watching_button.is_element_exists():
            self.start_watching_button.click()
        self.wait(lambda b: not self.loading_spinner.is_element_exists())
