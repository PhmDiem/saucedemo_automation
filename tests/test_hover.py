import pytest
from pages.inventory_page import InventoryPage
from selenium.webdriver.common.action_chains import ActionChains

@pytest.mark.hover
def test_hover_over_element(driver, login):
    inventory_page = InventoryPage(driver)

    # Lấy nút "Add to cart" cho sản phẩm "backpack" (trả về WebElement)
    add_btn = inventory_page.find_item("backpack")

    actions = ActionChains(driver)
    actions.move_to_element(add_btn).perform()  # Hover vào nút/element
    print('\nĐã hover vào item backpack')

    add_btn.click()  # Click vào nút Add to cart sau khi hover
    print('Đã click vào Add to cart sau khi hover')

    # Kiểm tra nút Remove đã xuất hiện sau khi thêm vào giỏ hàng
    assert inventory_page.is_remove_button_displayed("backpack")