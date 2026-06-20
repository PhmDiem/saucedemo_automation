import pytest
import allure
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from utils.config_reader import ConfigReader

@pytest.mark.positive
@pytest.mark.login
@pytest.mark.parametrize("user_type, expected_success", [
    ("standard", True),
    ("problem", True),
    ("performance", True),
    ("error", True),
    ("visual", True)
])
@allure.title("Login thành công")
def test_login_success (driver, user_type, expected_success):
    login_page = LoginPage(driver)
    inventory_page = InventoryPage(driver)
    users = ConfigReader.get_user(user_type)
    
    login_page.login(users["username"], users["password"])

    if expected_success:
        assert inventory_page.is_title_displayed()
    else:
        assert login_page.is_error_message_displayed()

@pytest.mark.negative
@pytest.mark.login
@pytest.mark.parametrize("user_type, expected_success", [
    ("locked_out", False),
    ("wrong_username", False),
    ("wrong_password", False),
    ("empty_username", False),
    ("empty_password", False),
    ("empty_both", False),
    ("space_username", False),
    ("space_password", False),
    ("space_both", False)
])
@allure.title("Login không thành công")
def test_login_failed (driver, user_type, expected_success):
    login_page = LoginPage(driver)
    inventory_page = InventoryPage(driver)
    users = ConfigReader.get_user(user_type)
    
    login_page.login(users["username"], users["password"])

    if expected_success:
        assert inventory_page.is_title_displayed()
    else:
        assert login_page.is_error_message_displayed()