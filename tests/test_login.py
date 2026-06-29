import pytest
import allure
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from utils.config_reader import ConfigReader

@allure.feature("Authentication")
class TestLogin:

    @pytest.fixture(autouse=True)
    def setup(self, driver):
        self.driver = driver
        self.login_page = LoginPage(driver)
        self.inventory_page = InventoryPage(driver)

    def do_login(self, user_type):
        users = ConfigReader.get_user(user_type)
        self.login_page.login(users["username"], users["password"])

    @pytest.mark.positive
    @pytest.mark.login
    @allure.story("Login thành công")
    @pytest.mark.parametrize("user_type", [
        "standard",
        "problem",
        "performance",
        "error",
        "visual"
    ])
    def test_login_success(self, user_type):
        with allure.step(f"Login với user: {user_type}"):
            self.do_login(user_type)

        with allure.step("Verify chuyển sang trang Inventory"):
            assert self.inventory_page.is_title_displayed(), \
                f"[{user_type}] Expect inventory page nhưng vẫn ở login"

    @pytest.mark.negative
    @pytest.mark.login
    @allure.story("Login thất bại")
    @pytest.mark.parametrize("user_type, expected_error", [
        ("locked_out",     "Sorry, this user has been locked out."),
        ("wrong_username", "Username and password do not match"),
        ("wrong_password", "Username and password do not match"),
        ("empty_username", "Username is required"),
        ("empty_password", "Password is required"),
        ("empty_both",     "Username is required"),
        ("space_username", "Username and password do not match"),
        ("space_password", "Username and password do not match"),
        ("space_both",     "Username and password do not match"),
    ])
    def test_login_failed(self, user_type, expected_error):
        with allure.step(f"Login với user: {user_type}"):
            self.do_login(user_type)

        with allure.step(f"Verify error: '{expected_error}'"):
            actual_error = self.login_page.get_error_message()
            assert expected_error in actual_error, \
                f"[{user_type}] Expected: '{expected_error}' | Got: '{actual_error}'"