import pytest
import allure
from utils.config_reader import ConfigReader
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage

@allure.feature("Cart")
class TestCart:

    @pytest.fixture(autouse=True)
    def setup(self, driver, login):
        self.driver = driver
        self.inventory_page = InventoryPage(driver)
        self.cart_page = CartPage(driver)

    # Verify item hiển thị đúng trong cart
    @pytest.mark.smoke
    def test_item_displayed_in_cart(self):
        self.inventory_page.add_to_cart("bike_light")
        self.inventory_page.click_cart_button()

        item_name = ConfigReader.get_product_name("bike_light")
        assert self.cart_page.is_item_displayed(item_name), f"Không hiển thị item '{item_name}' trong cart"

    # Verify tên, giá đúng trong cart
    def test_item_info_correct_in_cart(self):
        self.inventory_page.add_to_cart("bike_light")
        self.inventory_page.click_cart_button()

        assert self.cart_page.get_item_name("bike_light") == "Sauce Labs Bike Light"
        assert self.cart_page.get_item_price("bike_light") == "$9.99"

    # Remove từ trong Cart page (khác với remove từ Inventory)
    def test_remove_item_from_cart_page(self):
        self.inventory_page.add_to_cart("bike_light")
        self.inventory_page.click_cart_button()

        self.cart_page.remove_item("bike_light")

        assert not self.cart_page.is_item_displayed("bike_light")

    # Verify continue shopping → về inventory
    def test_continue_shopping(self):
        self.inventory_page.click_cart_button()
        self.cart_page.click_continue_shopping()

        assert self.inventory_page.is_title_displayed()

    # Verify checkout button
    def test_proceed_to_checkout(self):
        self.inventory_page.add_to_cart("bike_light")
        self.inventory_page.click_cart_button()

        self.cart_page.click_checkout()

        assert self.checkout_page.is_checkout_page_displayed()