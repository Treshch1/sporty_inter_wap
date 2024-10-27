from page_objects.base_page import BaseComponent, Element


class TextInput(BaseComponent):
    def __init__(self, input_field: Element):
        self.input_field = input_field

    def set_value(self, value):
        self.input_field.clear()
        self.input_field.send_keys(value)

    def extend_value(self, value):
        self.input_field.send_keys(value)

    def get_text(self):
        return self.input_field.text

    def get_value(self, timeout=None):
        return self.input_field.get_attribute("value", timeout=timeout)

    def get_placeholder(self):
        return self.input_field.get_attribute("placeholder")

    def clear_value(self):
        self.input_field.clear()

    def is_displayed(self):
        return self.input_field.is_displayed()

    def is_element_exists(self):
        return self.input_field.is_element_exists()
