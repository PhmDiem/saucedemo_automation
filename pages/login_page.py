import pytest
from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class LoginPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.username_input = (By.ID, "user-name")
        self.password_input = (By.ID, "password")
        self.login_button = (By.ID, "login-button")
        self.error_mgs= (By.XPATH, '//div[@class="error-message-container error"]')
        
    def login(self, username, password):
        self.send_keys(self.username_input, username)
        self.send_keys(self.password_input, password)
        self.click(self.login_button)

    def is_login_page_displayed(self):
        return self.is_displayed(self.login_button)  

    def is_error_message_displayed(self):
        return self.is_displayed(self.error_mgs)