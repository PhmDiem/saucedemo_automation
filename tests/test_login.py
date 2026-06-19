import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from utils.config_reader import ConfigReader

@pytest.mark.parametrize("user_type, expected_success", [
    ("standard", True),
    ("locked_out", False),
    ("problem", True),
    ("performance", True),
    ("error", False),
    ("visual", True),
])

def test_login_from_json(driver, user_type, expected_success):
    login_page = LoginPage(driver)
    inventory_page = InventoryPage(driver)
    users = ConfigReader.get_user(user_type)
    
    login_page.login(users["username"], users["password"])
    
    if expected_success:
        assert inventory_page.is_title_displayed()
    else:
        assert login_page.is_error_message_displayed()