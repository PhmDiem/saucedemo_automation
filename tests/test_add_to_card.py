import pytest
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from utils.config_reader import ConfigReader

def test_add_single_item_to_cart(driver, login):
    inventory_page = InventoryPage(driver)
    
    inventory_page.add_to_cart("bike_light")
    
    assert inventory_page.get_cart_count() == "1"
    assert inventory_page.is_remove_button_displayed("bike_light")

def test_add_multiple_items_to_cart(driver, login):
    inventory_page = InventoryPage(driver)
    
    inventory_page.add_to_cart("onesie")
    inventory_page.add_to_cart("bolt_tshirt")
    inventory_page.add_to_cart("fleece_jacket")
    
    assert inventory_page.get_cart_count() == "3"

def test_remove_item_from_cart(driver, login):
    inventory_page = InventoryPage(driver)
    
    inventory_page.add_to_cart("bike_light")
    inventory_page.add_to_cart("bolt_tshirt")
    
    assert inventory_page.get_cart_count() == "2"
    
    inventory_page.remove_from_cart("bike_light")
    
    assert inventory_page.get_cart_count() == "1"
    assert inventory_page.is_add_to_cart_button_displayed("bike_light")

def test_add_item_without_login(driver):
    driver.get(ConfigReader.get_product_url())  # Truy cập trực tiếp trang sản phẩm mà không login
    expected_url = ConfigReader.get_url()
    actual_url = driver.current_url
    assert actual_url == expected_url, f"Lỗi redirect! Kỳ vọng: {expected_url} nhưng thực tế lại là: {actual_url}"
        
    login_page = LoginPage(driver)
    assert login_page.is_login_page_displayed()
    
def test_add_all_items_to_cart(driver, login):
    inventory_page = InventoryPage(driver)
    products = ConfigReader.get_products()
    
    for key in products.keys():
        inventory_page.add_to_cart(key)
    
    expected = str(len(products))
    actual = inventory_page.get_cart_count()
    assert actual == expected, f"Kỳ vọng {expected} sản phẩm, nhưng thực tế là {actual}"

def test_cart_remains_after_refresh(driver, login):
    inventory_page = InventoryPage(driver)
    
    inventory_page.add_to_cart("bike_light")
    inventory_page.add_to_cart("bolt_tshirt")
    
    assert inventory_page.get_cart_count() == "2"
    
    driver.refresh()
    
    assert inventory_page.get_cart_count() == "2", "Giỏ hàng bị mất dữ liệu sau refresh"