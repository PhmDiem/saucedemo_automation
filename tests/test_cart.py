import pytest
import allure
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutStepOnePage
from utils.config_reader import ConfigReader


@allure.feature("Cart")
class TestCart:

    @pytest.fixture(autouse=True)
    def setup(self, driver, login):
        self.driver = driver
        self.inventory_page = InventoryPage(driver)
        self.cart_page = CartPage(driver)
        self.checkout_step_one = CheckoutStepOnePage(driver)

    # ── Hiển thị item trong cart ──────────
    @pytest.mark.positive
    @allure.story("Verify item hiển thị trong cart")
    def test_item_displayed_in_cart(self):
        self.inventory_page.add_to_cart("bike_light")
        self.inventory_page.click_cart_button()

        item_name = ConfigReader.get_product_name("bike_light")

        with allure.step(f"Verify item '{item_name}' hiển thị trong cart"):
            assert self.cart_page.is_item_displayed(item_name), \
                f"Không hiển thị item '{item_name}' trong cart"

    # ── Verify tên và giá đúng ────────────
    @pytest.mark.positive
    @allure.story("Verify tên và giá đúng trong cart")
    def test_item_info_correct_in_cart(self):
        self.inventory_page.add_to_cart("bike_light")
        self.inventory_page.click_cart_button()

        item_name = ConfigReader.get_product_name("bike_light")
        item_price = ConfigReader.get_product_price("bike_light")

        with allure.step(f"Verify tên: '{item_name}'"):
            assert self.cart_page.get_item_name(item_name) == item_name

        with allure.step(f"Verify giá: '{item_price}'"):
            assert self.cart_page.get_item_price(item_name) == item_price

    # ── Remove từ Cart page ───────────────
    @pytest.mark.positive
    @allure.story("Remove item từ Cart page")
    def test_remove_item_from_cart_page(self):
        self.inventory_page.add_to_cart("bike_light")
        self.inventory_page.click_cart_button()

        item_name = ConfigReader.get_product_name("bike_light")

        with allure.step(f"Remove item: '{item_name}'"):
            self.cart_page.remove_item(item_name)

        with allure.step("Verify item không còn trong cart"):
            assert self.cart_page.is_cart_empty(), \
                f"Item '{item_name}' vẫn còn trong cart sau khi remove"

    # ── Continue Shopping ─────────────────
    @pytest.mark.positive
    @allure.story("Continue shopping về Inventory")
    def test_continue_shopping(self):
        self.inventory_page.click_cart_button()

        with allure.step("Click Continue Shopping"):
            self.cart_page.click_continue_shopping()

        with allure.step("Verify về trang Inventory"):
            assert self.inventory_page.is_title_displayed()

    # ── Proceed to Checkout ───────────────
    @pytest.mark.positive
    @allure.story("Chuyển sang trang Checkout")
    def test_proceed_to_checkout(self):
        self.inventory_page.add_to_cart("bike_light")
        self.inventory_page.click_cart_button()

        with allure.step("Click Checkout"):
            self.cart_page.click_checkout()

        with allure.step("Verify chuyển sang trang Checkout"):
            assert self.checkout_step_one.is_checkout_step_one_displayed()  