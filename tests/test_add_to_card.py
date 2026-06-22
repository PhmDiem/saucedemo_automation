import pytest
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from utils.config_reader import ConfigReader

@pytest.mark.cart
@pytest.mark.add_to_cart
@pytest.mark.parametrize("product_key", [
    "bike_light", "onesie", "bolt_tshirt", "fleece_jacket"])
def test_add_single_item_to_cart(dirver, login, product_key):
    inventory_page = InventoryPage(dirver)
    inventory_page.add_to_cart(product_key)
    
    assert inventory_page.get_cart_count() == "1"
    assert inventory_page.is_remove_button_displayed(product_key)

@pytest.mark.cart
@pytest.mark.add_to_cart
@pytest.mark.parametrize("product_list, expected_count", [
    (["onesie", "bolt_tshirt", "fleece_jacket"], "3"),
    (["bike_light", "red_tshirt"], "2"),])
def test_add_multiple_items_to_cart(dirver, login, product_list, expected_count):
    inventory_page = InventoryPage(dirver)
    for product in product_list:
        inventory_page.add_to_cart(product)
    
    assert inventory_page.get_cart_count() == expected_count

@pytest.mark.cart
@pytest.mark.remove_from_cart
@pytest.mark.parametrize("add_list, remove_key", [
    (["bike_light", "bolt_tshirt"], "bike_light"),
    (["onesie", "fleece_jacket"], "onesie"),])
def test_remove_item_from_cart(dirver, login, add_list, remove_key):
    inventory_page = InventoryPage(dirver)
    # Add items
    for p in add_list:
        inventory_page.add_to_cart(p)
    
    assert inventory_page.get_cart_count() == str(len(add_list))
    
    # Remove
    inventory_page.remove_from_cart(remove_key)
    
    assert inventory_page.get_cart_count() == "1"
    assert inventory_page.is_add_to_cart_button_displayed(remove_key)

@pytest.mark.cart
@pytest.mark.add_to_cart
def test_add_all_items_to_cart(dirver, login):
    inventory_page = InventoryPage(dirver)
    products = ConfigReader.get_products()
    
    for key in products.keys():
        inventory_page.add_to_cart(key)
    
    assert inventory_page.get_cart_count() == str(len(products))

@pytest.mark.cart
@pytest.mark.edge_case
def test_add_item_without_login(driver):
    driver.get(ConfigReader.get_product_url())
    
    assert driver.current_url == ConfigReader.get_url(), "Không redirect về login page"
    
    login_page = LoginPage(driver)
    assert login_page.is_login_page_displayed()

@pytest.mark.cart
@pytest.mark.edge_case
def test_cart_remains_after_refresh(dirver, login):
    inventory_page = InventoryPage(dirver)
    inventory_page.add_to_cart("bike_light")
    inventory_page.add_to_cart("bolt_tshirt")
    
    assert inventory_page.get_cart_count() == "2"
    
    inventory_page.driver.refresh()   # Dùng driver từ page nếu có
    
    assert inventory_page.get_cart_count() == "2", "Giỏ hàng mất dữ liệu sau refresh"