from selenium.common.exceptions import ElementClickInterceptedException, ElementNotInteractableException


class wait_is_clickable_and_click:
    def __init__(self, element):
        self.element = element

    def __call__(self, driver):
        try:
            self.element.click()
            return True
        except ElementClickInterceptedException:
            return False
        except ElementNotInteractableException:
            return False
