from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class CheckoutPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.first_name_input = (By.ID, "first-name")
        self.last_name_input = (By.ID, "last-name")
        self.postal_code_input = (By.ID, "postal-code")
        self.continue_button = (By.ID, "continue")
        self.finish_button = (By.ID, "finish")
        self.checkout_complete_message = (By.CLASS_NAME, "complete-header")
        
    def is_checkout_page_displayed(self):
        return self.is_displayed(self.first_name_input)

    def enter_checkout_information(self, first_name, last_name, postal_code):
        self.send_keys(self.first_name_input, first_name)
        self.send_keys(self.last_name_input, last_name)
        self.send_keys(self.postal_code_input, postal_code)

    def complete_checkout(self):
        self.click(self.continue_button)
        self.click(self.finish_button)

    def is_checkout_complete_message_displayed(self):
        return self.is_displayed(self.checkout_complete_message)