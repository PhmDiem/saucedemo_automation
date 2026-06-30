import pytest
import allure
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutStepOnePage, CheckoutStepTwoPage
from utils.config_reader import ConfigReader


@allure.feature("Checkout")
class TestCheckout:

    @pytest.fixture(autouse=True)
    def setup(self, driver, login):
        self.driver = driver
        self.inventory_page  = InventoryPage(driver)
        self.cart_page       = CartPage(driver)
        self.step_one        = CheckoutStepOnePage(driver)
        self.step_two        = CheckoutStepTwoPage(driver)

    def go_to_step_one(self, product_key="bike_light"):
        """Helper: add item → vào cart → checkout"""
        self.inventory_page.add_to_cart(product_key)
        self.inventory_page.click_cart_button()
        self.cart_page.click_checkout()

    def go_to_step_two(self, first_name="John", last_name="Doe", postal="12345"):
        """Helper: điền form → sang step 2"""
        self.step_one.enter_information(first_name, last_name, postal)
        self.step_one.click_continue()

    # ─────────────────────────────────────────
    # STEP 1 — Form
    # ─────────────────────────────────────────
    @pytest.mark.positive
    @allure.story("Step 1 - Hiển thị form checkout")
    def test_step_one_displayed(self):
        self.go_to_step_one()

        with allure.step("Verify form checkout hiển thị"):
            assert self.step_one.is_checkout_step_one_displayed()

    @pytest.mark.negative
    @allure.story("Step 1 - Bỏ trống các field")
    @pytest.mark.parametrize("first_name, last_name, postal, expected_error", [
        ("",      "Doe",  "12345", "First Name is required"),
        ("John",  "",     "12345", "Last Name is required"),
        ("John",  "Doe",  "",      "Postal Code is required"),
        ("",      "",     "",      "First Name is required"),
    ])
    def test_step_one_missing_fields(self, first_name, last_name, postal, expected_error):
        self.go_to_step_one()

        with allure.step(f"Điền form thiếu field"):
            self.step_one.enter_information(first_name, last_name, postal)
            self.step_one.click_continue()

        with allure.step(f"Verify error: '{expected_error}'"):
            assert self.step_one.is_error_displayed()
            assert expected_error in self.step_one.get_error_message()

    @pytest.mark.positive
    @allure.story("Step 1 - Cancel về Cart")
    def test_step_one_cancel(self):
        self.go_to_step_one()

        with allure.step("Click Cancel"):
            self.step_one.click_cancel()

        with allure.step("Verify về trang Cart"):
            assert self.cart_page.is_item_displayed(
                ConfigReader.get_product_name("bike_light")
            )

    # ─────────────────────────────────────────
    # STEP 2 — Summary
    # ─────────────────────────────────────────
    @pytest.mark.positive
    @allure.story("Step 2 - Hiển thị order summary")
    def test_step_two_displayed(self):
        self.go_to_step_one()
        self.go_to_step_two()

        with allure.step("Verify order summary hiển thị"):
            assert self.step_two.is_checkout_step_two_displayed()

    @pytest.mark.positive
    @allure.story("Step 2 - Verify tên và giá sản phẩm")
    def test_step_two_item_info(self):
        self.go_to_step_one("bike_light")
        self.go_to_step_two()

        expected_name  = ConfigReader.get_product_name("bike_light")
        expected_price = ConfigReader.get_product_price("bike_light")

        with allure.step(f"Verify tên: '{expected_name}'"):
            assert self.step_two.get_item_name() == expected_name

        with allure.step(f"Verify giá: '{expected_price}'"):
            assert self.step_two.get_item_price() == expected_price

    @pytest.mark.positive
    @allure.story("Step 2 - Verify tổng tiền đúng")
    def test_step_two_total_correct(self):
        self.go_to_step_one("bike_light")
        self.go_to_step_two()

        with allure.step("Verify subtotal + tax = total"):
            subtotal = self.step_two.get_subtotal_value()
            tax      = self.step_two.get_tax_value()
            total    = self.step_two.get_total_value()

            assert round(subtotal + tax, 2) == total, \
                f"Tổng sai: {subtotal} + {tax} != {total}"

    @pytest.mark.positive
    @allure.story("Step 2 - Cancel về Inventory")
    def test_step_two_cancel(self):
        self.go_to_step_one()
        self.go_to_step_two()

        with allure.step("Click Cancel"):
            self.step_two.click_cancel()

        with allure.step("Verify về trang Inventory"):
            assert self.inventory_page.is_title_displayed()

    # ─────────────────────────────────────────
    # COMPLETE ORDER
    # ─────────────────────────────────────────
    @pytest.mark.positive
    @allure.story("Hoàn thành đơn hàng")
    def test_complete_order(self):
        self.go_to_step_one("bike_light")
        self.go_to_step_two()

        with allure.step("Click Finish"):
            self.step_two.click_finish()

        with allure.step("Verify đơn hàng hoàn thành"):
            assert self.step_two.is_order_complete(), \
                "Không hiển thị màn hình xác nhận đơn hàng"