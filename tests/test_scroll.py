import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from selenium.webdriver.common.by import By

def test_scroll_to_element(driver):
    login_page = LoginPage(driver)
    login_page.enter_username("standard_user")
    login_page.enter_password("secret_sauce")
    login_page.click_login_button()
    
    inventory_page = InventoryPage(driver)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    print('\nĐã scroll đến cuối trang inventory')

    first_item = inventory_page.find_element(inventory_page.item_1)
    driver.execute_script("arguments[0].scrollIntoView(true);", first_item)
    print('Đã scroll đến item đầu tiên')
    assert inventory_page.is_displayed(inventory_page.item_1)
