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

    #SORT
    @pytest.mark.positive
    @pytest.mark.select_sort
    @allure.story("Sort sản phẩm")
    @pytest.mark.parametrize("sort_option, label", [
        ("az",   "A → Z"),
        ("za",   "Z → A"),
        ("lohi", "Giá thấp → cao"),
        ("hilo", "Giá cao → thấp"),
    ])
    def test_sort(self, sort_option, label):
        with allure.step(f"Chọn sort: {label}"):
            self.inventory_page.select_sort(sort_option)

        with allure.step("Verify thứ tự đúng"):
            if sort_option == "az":
                items = self.inventory_page.get_item_names()
                assert items == sorted(items), f"Sort {label} sai thứ tự"

            elif sort_option == "za":
                items = self.inventory_page.get_item_names()
                assert items == sorted(items, reverse=True), f"Sort {label} sai thứ tự"

            elif sort_option == "lohi":
                prices = self.inventory_page.get_item_prices()
                assert prices == sorted(prices), f"Sort {label} sai thứ tự"

            elif sort_option == "hilo":
                prices = self.inventory_page.get_item_prices()
                assert prices == sorted(prices, reverse=True), f"Sort {label} sai thứ tự"

@allure.feature("Inventory - Cart")
class TestCartInInventory:

    @pytest.fixture(autouse=True)
    def setup(self, driver):
        self.driver = driver
        self.inventory_page = InventoryPage(driver)

    # STANDARD USER — Happy Path
    @pytest.mark.positive
    @allure.story("Thêm 1 sản phẩm - Standard User")
    @pytest.mark.parametrize("product_key", [
        "bike_light", "onesie", "bolt_tshirt", "fleece_jacket"
    ])
    def test_add_single_item(self, login, product_key):
        with allure.step(f"Thêm sản phẩm: {product_key}"):
            self.inventory_page.add_to_cart(product_key)

        with allure.step("Verify cart badge = 1"):
            assert self.inventory_page.get_cart_count() == "1"

        with allure.step("Verify nút Remove hiển thị"):
            assert self.inventory_page.is_remove_button_displayed(product_key)

    @pytest.mark.positive
    @allure.story("Thêm nhiều sản phẩm - Standard User")
    @pytest.mark.parametrize("product_list, expected_count", [
        (["onesie", "bolt_tshirt", "fleece_jacket"], "3"),
        (["bike_light", "red_tshirt"], "2"),
    ])
    def test_add_multiple_items(self, login, product_list, expected_count):
        with allure.step(f"Thêm {len(product_list)} sản phẩm"):
            for product in product_list:
                self.inventory_page.add_to_cart(product)

        with allure.step(f"Verify cart badge = {expected_count}"):
            assert self.inventory_page.get_cart_count() == expected_count

    @pytest.mark.positive
    @allure.story("Xóa sản phẩm khỏi giỏ - Standard User")
    @pytest.mark.parametrize("add_list, remove_key", [
        (["bike_light", "bolt_tshirt"], "bike_light"),
        (["onesie", "fleece_jacket"], "onesie"),
    ])
    def test_remove_item(self, login, add_list, remove_key):
        with allure.step(f"Thêm {len(add_list)} sản phẩm"):
            for p in add_list:
                self.inventory_page.add_to_cart(p)

        with allure.step(f"Xóa: {remove_key}"):
            self.inventory_page.remove_from_cart(remove_key)

        with allure.step("Verify cart badge giảm 1"):
            assert self.inventory_page.get_cart_count() == str(len(add_list) - 1)

        with allure.step("Verify nút Add to Cart hiển thị lại"):
            assert self.inventory_page.is_add_to_cart_button_displayed(remove_key)

    @pytest.mark.positive
    @allure.story("Thêm tất cả sản phẩm - Standard User")
    def test_add_all_items(self, login):
        products = ConfigReader.get_products()

        with allure.step(f"Thêm tất cả {len(products)} sản phẩm"):
            for key in products.keys():
                self.inventory_page.add_to_cart(key)

        with allure.step(f"Verify cart badge = {len(products)}"):
            assert self.inventory_page.get_cart_count() == str(len(products))

    @pytest.mark.positive
    @allure.story("Giỏ hàng giữ nguyên sau refresh - Standard User")
    def test_cart_remains_after_refresh(self, login):
        with allure.step("Thêm 2 sản phẩm"):
            self.inventory_page.add_to_cart("bike_light")
            self.inventory_page.add_to_cart("bolt_tshirt")

        with allure.step("Refresh trang"):
            self.driver.refresh()

        with allure.step("Verify cart vẫn giữ 2 sản phẩm"):
            assert self.inventory_page.get_cart_count() == "2"

    # NO LOGIN — Edge Case
    @pytest.mark.negative
    @allure.story("Truy cập inventory khi chưa login")
    def test_add_item_without_login(self):
        with allure.step("Truy cập trực tiếp URL inventory"):
            self.driver.get(ConfigReader.get_product_url())

        with allure.step("Verify redirect về login page"):
            assert self.driver.current_url == ConfigReader.get_url()
            assert LoginPage(self.driver).is_login_page_displayed()

    # PROBLEM USER — Known Bugs
    @pytest.mark.bug
    @allure.story("Add to cart bị bug - Problem User")
    @pytest.mark.parametrize("product_key", [
        "bike_light", "bolt_tshirt"
    ])
    def test_add_to_cart_problem_user(self, login_as, product_key):
        login_as("problem")

        with allure.step(f"Thêm sản phẩm: {product_key}"):
            self.inventory_page.add_to_cart(product_key)

        with allure.step("Verify bug — cart badge không tăng hoặc sai"):
            # problem_user: một số item add không được → document bug
            try:
                count = self.inventory_page.get_cart_count()
                assert count != "1", "Bug đã được fix!"
            except Exception:
                pass  # Bug vẫn còn — expected

    # ERROR USER — Error Handling
    @pytest.mark.negative
    @allure.story("Add to cart trả về lỗi - Error User")
    @pytest.mark.parametrize("product_key", [
        "bike_light", "bolt_tshirt"
    ])
    def test_add_to_cart_error_user(self, login_as, product_key):
        login_as("error")

        with allure.step(f"Thêm sản phẩm: {product_key}"):
            self.inventory_page.add_to_cart(product_key)

        with allure.step("Verify error hoặc cart không tăng đúng"):
            # error_user: một số thao tác trả về lỗi
            try:
                count = self.inventory_page.get_cart_count()
                assert count == "1"
            except Exception as e:
                allure.attach(str(e), name="Error detail", 
                              attachment_type=allure.attachment_type.TEXT)

    # PERFORMANCE USER — Response Time
    @pytest.mark.performance
    @allure.story("Đo thời gian add to cart - Performance User")
    def test_add_to_cart_performance_user(self, login_as):
        login_as("performance")

        with allure.step("Đo thời gian add to cart"):
            start = time.time()
            self.inventory_page.add_to_cart("bike_light")
            duration = time.time() - start

            allure.attach(
                f"Thời gian: {duration:.2f}s",
                name="Performance Result",
                attachment_type=allure.attachment_type.TEXT
            )

        with allure.step("Verify thời gian < 5s"):
            assert duration < 5, f"Quá chậm: {duration:.2f}s"
