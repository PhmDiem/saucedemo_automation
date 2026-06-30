import pytest
import allure
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

    def go_to_detail(self, product_key):
        """Helper: click vào sản phẩm từ inventory"""
        self.inventory_page.click_inventory_item(product_key)

    # ─────────────────────────────────────────
    # HIỂN THỊ
    # ─────────────────────────────────────────
    @pytest.mark.positive
    @pytest.mark.smoke
    @allure.story("Verify thông tin sản phẩm")
    @pytest.mark.parametrize("product_key", [
        "bike_light",
        "onesie",
        "bolt_tshirt",
    ])
    def test_product_info_displayed(self, product_key):
        expected_name  = ConfigReader.get_product_name(product_key)
        expected_price = ConfigReader.get_product_price(product_key)

        with allure.step(f"Vào trang detail: {product_key}"):
            self.go_to_detail(product_key)
            assert self.detail_page.is_product_page_displayed()

        with allure.step("Verify tên sản phẩm đúng"):
            assert self.detail_page.get_product_name() == expected_name, \
                f"Tên sai: expected '{expected_name}'"

        with allure.step("Verify giá sản phẩm đúng"):
            assert self.detail_page.get_product_price() == expected_price, \
                f"Giá sai: expected '{expected_price}'"

        with allure.step("Verify ảnh hiển thị"):
            assert self.detail_page.is_product_image_displayed()

    # ─────────────────────────────────────────
    # ADD TO CART TỪ DETAIL PAGE
    # ─────────────────────────────────────────
    @pytest.mark.positive
    @allure.story("Add to cart từ Detail page")
    @pytest.mark.parametrize("product_key", [
        "bike_light",
        "onesie",
    ])
    def test_add_to_cart_from_detail(self, product_key):
        self.go_to_detail(product_key)

        with allure.step("Verify nút Add to Cart hiển thị"):
            assert self.detail_page.is_add_to_cart_displayed()

        with allure.step("Click Add to Cart"):
            self.detail_page.add_to_cart()

        with allure.step("Verify nút đổi sang Remove"):
            assert self.detail_page.is_remove_displayed()

        with allure.step("Verify cart badge = 1"):
            assert self.inventory_page.get_cart_count() == "1"

    # ─────────────────────────────────────────
    # REMOVE TỪ DETAIL PAGE
    # ─────────────────────────────────────────
    @pytest.mark.positive
    @allure.story("Remove từ Detail page")
    def test_remove_from_detail(self):
        self.go_to_detail("bike_light")

        with allure.step("Add to cart trước"):
            self.detail_page.add_to_cart()
            assert self.detail_page.is_remove_displayed()

        with allure.step("Remove từ detail page"):
            self.detail_page.remove_from_cart()

        with allure.step("Verify nút đổi lại Add to Cart"):
            assert self.detail_page.is_add_to_cart_displayed()

        with allure.step("Verify cart badge biến mất"):
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

        with allure.step("Verify về trang Inventory"):
            assert self.inventory_page.is_title_displayed()

    @pytest.mark.positive
    @allure.story("Back sau khi add — cart giữ nguyên")
    def test_back_after_add_cart_persists(self):
        self.go_to_detail("bike_light")

        with allure.step("Add to cart từ detail"):
            self.detail_page.add_to_cart()

        with allure.step("Back về Inventory"):
            self.detail_page.back_to_products()

        with allure.step("Verify cart badge vẫn = 1"):
            assert self.inventory_page.get_cart_count() == "1"

    # ─────────────────────────────────────────
    # ADD TỪ DETAIL → VÀO CART VERIFY
    # ─────────────────────────────────────────
    @pytest.mark.positive
    @allure.story("Add từ detail page → verify trong Cart")
    def test_add_from_detail_verify_in_cart(self):
        expected_name = ConfigReader.get_product_name("bike_light")
        self.go_to_detail("bike_light")

        with allure.step("Add to cart"):
            self.detail_page.add_to_cart()

        with allure.step("Back về inventory rồi vào cart"):
            self.detail_page.back_to_products()
            self.inventory_page.click_cart_button()

        with allure.step(f"Verify '{expected_name}' có trong cart"):
            assert self.cart_page.is_item_displayed(expected_name)