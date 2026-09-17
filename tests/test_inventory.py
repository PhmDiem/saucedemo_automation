import pytest
import time
import allure
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from utils.config_reader import ConfigReader

@allure.feature("Inventory - Sort")
class TestInventory:

    @pytest.fixture(autouse=True)
    def setup(self, driver, login):
        self.inventory_page = InventoryPage(driver)

    # SORT
    @pytest.mark.positive
    @pytest.mark.select_sort
    @allure.story("Sort products")
    @pytest.mark.parametrize("sort_option, label", [
        ("az",   "A → Z"),
        ("za",   "Z → A"),
        ("lohi", "Price low to high"),
        ("hilo", "Price high to low"),
    ])
    def test_sort(self, sort_option, label):
        with allure.step(f"Select sort: {label}"):
            self.inventory_page.select_sort(sort_option)

        with allure.step("Verify correct order"):
            if sort_option == "az":
                items = self.inventory_page.get_item_names()
                assert items == sorted(items), f"Sort order is incorrect for {label}"

            elif sort_option == "za":
                items = self.inventory_page.get_item_names()
                assert items == sorted(items, reverse=True), f"Sort order is incorrect for {label}"

            elif sort_option == "lohi":
                prices = self.inventory_page.get_item_prices()
                assert prices == sorted(prices), f"Sort order is incorrect for {label}"

            elif sort_option == "hilo":
                prices = self.inventory_page.get_item_prices()
                assert prices == sorted(prices, reverse=True), f"Sort order is incorrect for {label}"

@allure.feature("Inventory - Cart")
class TestCartInInventory:

    @pytest.fixture(autouse=True)
    def setup(self, driver):
        self.driver = driver
        self.inventory_page = InventoryPage(driver)

    # STANDARD USER — Happy Path
    @pytest.mark.positive
    @allure.story("Add one product - Standard User")
    @pytest.mark.parametrize("product_key", [
        "bike_light", "onesie", "bolt_tshirt", "fleece_jacket"
    ])
    def test_add_single_item(self, login, product_key):
        with allure.step(f"Add product: {product_key}"):
            self.inventory_page.add_to_cart(product_key)

        with allure.step("Verify cart badge equals 1"):
            assert self.inventory_page.get_cart_count() == "1"

        with allure.step("Verify Remove button is displayed"):
            assert self.inventory_page.is_remove_button_displayed(product_key)

    @pytest.mark.positive
    @allure.story("Add multiple products - Standard User")
    @pytest.mark.parametrize("product_list, expected_count", [
        (["onesie", "bolt_tshirt", "fleece_jacket"], "3"),
        (["bike_light", "red_tshirt"], "2"),
    ])
    def test_add_multiple_items(self, login, product_list, expected_count):
        with allure.step(f"Add {len(product_list)} products"):
            for product in product_list:
                self.inventory_page.add_to_cart(product)

        with allure.step(f"Verify cart badge equals {expected_count}"):
            assert self.inventory_page.get_cart_count() == expected_count

    @pytest.mark.positive
    @allure.story("Remove product from cart - Standard User")
    @pytest.mark.parametrize("add_list, remove_key", [
        (["bike_light", "bolt_tshirt"], "bike_light"),
        (["onesie", "fleece_jacket"], "onesie"),
    ])
    def test_remove_item(self, login, add_list, remove_key):
        with allure.step(f"Add {len(add_list)} products"):
            for p in add_list:
                self.inventory_page.add_to_cart(p)

        with allure.step(f"Remove: {remove_key}"):
            self.inventory_page.remove_from_cart(remove_key)

        with allure.step("Verify cart badge decreases by 1"):
            assert self.inventory_page.get_cart_count() == str(len(add_list) - 1)

        with allure.step("Verify Add to Cart button is displayed again"):
            assert self.inventory_page.is_add_to_cart_button_displayed(remove_key)

    @pytest.mark.positive
    @allure.story("Add all products - Standard User")
    def test_add_all_items(self, login):
        products = ConfigReader.get_products()

        with allure.step(f"Add all {len(products)} products"):
            for key in products.keys():
                self.inventory_page.add_to_cart(key)

        with allure.step(f"Verify cart badge equals {len(products)}"):
            assert self.inventory_page.get_cart_count() == str(len(products))

    @pytest.mark.positive
    @allure.story("Cart persists after refresh - Standard User")
    def test_cart_remains_after_refresh(self, login):
        with allure.step("Add two products"):
            self.inventory_page.add_to_cart("bike_light")
            self.inventory_page.add_to_cart("bolt_tshirt")

        with allure.step("Refresh the page"):
            self.driver.refresh()

        with allure.step("Verify cart still contains two products"):
            assert self.inventory_page.get_cart_count() == "2"

    # NO LOGIN — Edge Case
    @pytest.mark.negative
    @allure.story("Access inventory without logging in")
    def test_add_item_without_login(self):
        with allure.step("Open the inventory URL directly"):
            self.driver.get(ConfigReader.get_product_url())

        with allure.step("Verify redirect to login page"):
            assert self.driver.current_url == ConfigReader.get_url()
            assert LoginPage(self.driver).is_login_page_displayed()

    # PROBLEM USER — Known Bugs
    @pytest.mark.bug
    @allure.story("Add to cart known bug - Problem User")
    @pytest.mark.parametrize("product_key, expected_count", [
        ("bike_light", "1"),
        ("bolt_tshirt", None),
    ])
    def test_add_to_cart_problem_user(self, login_as, product_key, expected_count):
        login_as("problem")

        with allure.step(f"Add product: {product_key}"):
            self.inventory_page.add_to_cart(product_key)

        with allure.step("Verify product-specific problem_user cart behavior"):
            # problem_user adds the bike light but fails to add the bolt T-shirt.
            if expected_count is None:
                assert not self.inventory_page.is_cart_badge_displayed(), \
                    "The problem_user bolt T-shirt behavior has changed."
            else:
                assert self.inventory_page.get_cart_count() == expected_count

    # ERROR USER — Error Handling
    @pytest.mark.negative
    @allure.story("Add to cart error handling - Error User")
    @pytest.mark.parametrize("product_key, expected_count", [
        ("bike_light", "1"),
        ("bolt_tshirt", None),
    ])
    def test_add_to_cart_error_user(self, login_as, product_key, expected_count):
        login_as("error")

        with allure.step(f"Add product: {product_key}"):
            self.inventory_page.add_to_cart(product_key)

        with allure.step("Verify product-specific error_user cart behavior"):
            # error_user adds the bike light but fails to add the bolt T-shirt.
            if expected_count is None:
                assert not self.inventory_page.is_cart_badge_displayed(), \
                    "The error_user bolt T-shirt behavior has changed."
            else:
                assert self.inventory_page.get_cart_count() == expected_count

    # PERFORMANCE USER — Response Time
    @pytest.mark.performance
    @allure.story("Measure add-to-cart response time - Performance User")
    def test_add_to_cart_performance_user(self, login_as):
        login_as("performance")

        with allure.step("Measure add-to-cart response time"):
            start = time.time()
            self.inventory_page.add_to_cart("bike_light")
            duration = time.time() - start

            allure.attach(
                f"Duration: {duration:.2f}s",
                name="Performance Result",
                attachment_type=allure.attachment_type.TEXT
            )

        with allure.step("Verify duration is less than 5 seconds"):
            assert duration < 5, f"Too slow: {duration:.2f}s"
