import pytest
from pages.inventory_page import InventoryPage

@pytest.mark.select_sort
class TestInventory:
    def test_sort_a_to_z(self, driver, login):
        inventory_page = InventoryPage(driver)
        inventory_page.select_sort("az")
        items = inventory_page.get_item_names()
        assert items == sorted(items)

    def test_sort_z_to_a(self, driver, login):
        inventory_page = InventoryPage(driver)
        inventory_page.select_sort("za")
        items = inventory_page.get_item_names()
        assert items == sorted(items, reverse=True)

    def test_sort_price_low_to_high(self, driver, login):
        inventory_page = InventoryPage(driver)
        inventory_page.select_sort("lohi")
        prices = inventory_page.get_item_prices()
        assert prices == sorted(prices)

    def test_sort_price_high_to_low(self, driver, login):
        inventory_page = InventoryPage(driver)
        inventory_page.select_sort("hilo")
        prices = inventory_page.get_item_prices()
        assert prices == sorted(prices, reverse=True)