import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from utils.config_reader import ConfigReader

def test_login_valid_user(driver):
    login_page = LoginPage(driver)
    login_page.enter_username(ConfigReader.get_user("standard")["username"])
    login_page.enter_password(ConfigReader.get_user("standard")["password"])
    login_page.click_login_button()

    inventory_page = InventoryPage(driver)
    assert inventory_page.is_title_displayed()
