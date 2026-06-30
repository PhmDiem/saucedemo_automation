from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class ProductDetailPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.product_name    = (By.XPATH, '//div[@data-test="inventory-item-name"]')
        self.product_desc    = (By.XPATH, '//div[@data-test="inventory-item-desc"]')
        self.product_price   = (By.XPATH, '//div[@data-test="inventory-item-price"]')
        self.product_image   = (By.CLASS_NAME, "inventory_details_img")
        self.add_to_cart_btn = (By.ID, "add-to-cart")
        self.remove_btn      = (By.ID, "remove")
        self.back_btn        = (By.ID, "back-to-products")

    # ── Info ──────────────────────────────
    def is_product_page_displayed(self) -> bool:
        return self.is_displayed(self.product_name)

    def get_product_name(self) -> str:
        return self.get_text(self.product_name)

    def get_product_desc(self) -> str:
        return self.get_text(self.product_desc)

    def get_product_price(self) -> str:
        return self.get_text(self.product_price)

    def is_product_image_displayed(self) -> bool:
        return self.is_displayed(self.product_image)

    # ── Actions ───────────────────────────
    def add_to_cart(self):
        self.click(self.add_to_cart_btn)

    def remove_from_cart(self):
        self.click(self.remove_btn)

    def back_to_products(self):
        self.click(self.back_btn)

    # ── Verify buttons ────────────────────
    def is_add_to_cart_displayed(self) -> bool:
        return self.is_displayed(self.add_to_cart_btn)

    def is_remove_displayed(self) -> bool:
        return self.is_displayed(self.remove_btn)