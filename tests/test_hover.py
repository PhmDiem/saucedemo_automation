import pytest
from selenium import webdriver
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from selenium.webdriver.common.action_chains import ActionChains

def test_hover_over_element(driver):
    login_page = LoginPage(driver)
    login_page.enter_username("standard_user")
    login_page.enter_password("secret_sauce")
    login_page.click_login_button()
    
    inventory_page = InventoryPage(driver)
    item = inventory_page.wait_visible(inventory_page.item_1)

    actions = ActionChains(driver)
    actions.move_to_element(item).perform()  # Hover vào item đầu tiên
    print('\nĐã hover vào item đầu tiên')

    add_to_cart_btn = inventory_page.wait_clickable(inventory_page.add_to_cart_1)
    add_to_cart_btn.click()  # Click vào nút Add to cart sau khi hover
    print('Đã click vào Add to cart sau khi hover')
    assert inventory_page.is_displayed(inventory_page.remove_1)  # Kiểm tra