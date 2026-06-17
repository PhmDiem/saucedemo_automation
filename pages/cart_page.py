import pytest
from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class CartPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.cart_items = (By.CLASS_NAME, "cart_item")
        self.continue_shopping_button = (By.ID, "continue-shopping")
    
