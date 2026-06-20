import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from selenium.webdriver.common.by import By
from utils.config_reader import ConfigReader

@pytest.mark.scroll
def test_scroll_to_element(driver, login):   
    inventory_page = InventoryPage(driver)

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    print('\nĐã scroll đến cuối trang inventory')

    first_item = inventory_page.find_item("backpack")
    driver.execute_script("arguments[0].scrollIntoView(true);", first_item)
    print('Đã scroll đến item đầu tiên')
    assert inventory_page.is_inventory_item_displayed("backpack")
