from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class CartPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.cart_items          = (By.CLASS_NAME, "cart_item")
        self.continue_shopping_button = (By.ID, "continue-shopping")
        self.checkout_button     = (By.ID, "checkout")

    def _item_name_locator(self, item_name: str):
        """Tìm item theo tên trong cart"""
        return (By.XPATH, f'//div[@class="inventory_item_name"][text()="{item_name}"]')

    def _item_price_locator(self, item_name: str):
        """Tìm giá của item theo tên"""
        return (By.XPATH, 
            f'//div[@class="inventory_item_name"][text()="{item_name}"]'
            f'/ancestor::div[@class="cart_item_label"]'
            f'//div[@class="inventory_item_price"]'
        )

    def is_item_displayed(self, item_name: str) -> bool:
        return self.is_displayed(self._item_name_locator(item_name))

    def get_item_name(self, item_name: str) -> str:
        return self.get_text(self._item_name_locator(item_name))

    def get_item_price(self, item_name: str) -> str:
        return self.get_text(self._item_price_locator(item_name))

    def remove_item(self, item_name: str):
        remove_locator = (By.XPATH,
            f'//div[@class="inventory_item_name"][text()="{item_name}"]'
            f'/ancestor::div[@class="cart_item_label"]'
            f'//button[contains(@id, "remove")]'
        )
        self.click(remove_locator)

    def click_continue_shopping(self):
        self.click(self.continue_shopping_button)

    def click_checkout(self):
        self.click(self.checkout_button)

    def is_cart_empty(self) -> bool:
        items = self.driver.find_elements(*self.cart_items)
        return len(items) == 0