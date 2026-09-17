import pytest
import allure
from selenium.webdriver.support import expected_conditions as EC
from pages.inventory_page import InventoryPage
from pages.product_detail_page import ProductDetailPage
from pages.cart_page import CartPage
from utils.config_reader import ConfigReader


@allure.feature("Product Detail")
class TestProductDetail:

    @pytest.fixture(autouse=True)
    def setup(self, driver, login):
        self.driver = driver
        self.inventory_page  = InventoryPage(driver)
        self.detail_page     = ProductDetailPage(driver)
        self.cart_page       = CartPage(driver)
        
    @pytest.mark.smoke
    def go_to_detail(self, product_key):
        """Helper: click a product from inventory."""
        self.inventory_page.click_inventory_item(product_key)

    # ─────────────────────────────────────────
    # DISPLAY
    # ─────────────────────────────────────────
    @pytest.mark.positive
    @pytest.mark.smoke
    @allure.story("Verify product information")
    @pytest.mark.parametrize("product_key", [
        "bike_light",
        "onesie",
        "bolt_tshirt",
    ])
    def test_product_info_displayed(self, product_key):
        expected_name  = ConfigReader.get_product_name(product_key)
        expected_price = ConfigReader.get_product_price(product_key)

        with allure.step(f"Open product detail: {product_key}"):
            self.go_to_detail(product_key)
            assert self.detail_page.wait.until(
                EC.text_to_be_present_in_element(
                    self.detail_page.product_name,
                    expected_name,
                )
            )

        with allure.step("Verify correct product name"):
            assert self.detail_page.get_product_name() == expected_name, \
                f"Incorrect name: expected '{expected_name}'"

        with allure.step("Verify correct product price"):
            assert self.detail_page.get_product_price() == expected_price, \
                f"Incorrect price: expected '{expected_price}'"

        with allure.step("Verify product image is displayed"):
            assert self.detail_page.is_product_image_displayed()

    # ─────────────────────────────────────────
    # ADD TO CART FROM DETAIL PAGE
    # ─────────────────────────────────────────
    @pytest.mark.positive
    @allure.story("Add to cart from Detail page")
    @pytest.mark.parametrize("product_key", [
        "bike_light",
        "onesie",
    ])
    def test_add_to_cart_from_detail(self, product_key):
        self.go_to_detail(product_key)

        with allure.step("Verify Add to Cart button is displayed"):
            assert self.detail_page.is_add_to_cart_displayed()

        with allure.step("Click Add to Cart"):
            self.detail_page.add_to_cart()

        with allure.step("Verify button changes to Remove"):
            assert self.detail_page.is_remove_displayed()

        with allure.step("Verify cart badge equals 1"):
            assert self.inventory_page.get_cart_count() == "1"

    # ─────────────────────────────────────────
    # REMOVE FROM DETAIL PAGE
    # ─────────────────────────────────────────
    @pytest.mark.positive
    @allure.story("Remove from Detail page")
    def test_remove_from_detail(self):
        self.go_to_detail("bike_light")

        with allure.step("Add to cart first"):
            self.detail_page.add_to_cart()
            assert self.detail_page.is_remove_displayed()

        with allure.step("Remove from detail page"):
            self.detail_page.remove_from_cart()

        with allure.step("Verify button changes back to Add to Cart"):
            assert self.detail_page.is_add_to_cart_displayed()

        with allure.step("Verify cart badge disappears"):
            assert not self.inventory_page.is_cart_badge_displayed()

    # ─────────────────────────────────────────
    # BACK TO PRODUCTS
    # ─────────────────────────────────────────
    @pytest.mark.positive
    @allure.story("Back to Products")
    def test_back_to_products(self):
        self.go_to_detail("bike_light")

        with allure.step("Click Back to Products"):
            self.detail_page.back_to_products()

        with allure.step("Verify return to Inventory"):
            assert self.inventory_page.is_title_displayed()

    @pytest.mark.positive
    @allure.story("Cart persists after going back")
    def test_back_after_add_cart_persists(self):
        self.go_to_detail("bike_light")

        with allure.step("Add to cart from detail"):
            self.detail_page.add_to_cart()

        with allure.step("Go back to Inventory"):
            self.detail_page.back_to_products()

        with allure.step("Verify cart badge still equals 1"):
            assert self.inventory_page.get_cart_count() == "1"

    # ─────────────────────────────────────────
    # ADD FROM DETAIL → VERIFY IN CART
    # ─────────────────────────────────────────
    @pytest.mark.positive
    @allure.story("Add from detail page → verify in Cart")
    def test_add_from_detail_verify_in_cart(self):
        expected_name = ConfigReader.get_product_name("bike_light")
        self.go_to_detail("bike_light")

        with allure.step("Add to cart"):
            self.detail_page.add_to_cart()

        with allure.step("Go back to inventory, then open cart"):
            self.detail_page.back_to_products()
            self.inventory_page.click_cart_button()

        with allure.step(f"Verify '{expected_name}' is in cart"):
            assert self.cart_page.is_item_displayed(expected_name)
