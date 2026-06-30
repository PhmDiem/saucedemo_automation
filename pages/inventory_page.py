from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from utils.config_reader import ConfigReader
from selenium.webdriver.support.ui import Select

class InventoryPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

        self.title = (By.XPATH, '//span[@class="title"]')
        self.sort_container = (By.XPATH, '//select[@class="product_sort_container"]')
        self.inventory_items = (By.CLASS_NAME, "inventory_item")
        self.number_of_items_in_cart = (By.CLASS_NAME, "shopping_cart_badge")
        self.cart_button = (By.ID, "shopping_cart_container")

    def is_title_displayed(self):
        return self.is_displayed(self.title)
    
    def select_sort(self, sort_option: str):
        dropdown = Select(self.driver.find_element(*self.sort_container))
        dropdown.select_by_value(sort_option)

    def get_item_names(self) -> list[str]:
        elements = self.driver.find_elements(By.CLASS_NAME, "inventory_item_name")
        return [el.text for el in elements]

    def get_item_prices(self) -> list[float]:
        elements = self.driver.find_elements(By.CLASS_NAME, "inventory_item_price")
        return [float(el.text.replace("$", "")) for el in elements]    

    def get_inventory_items(self):
        return self.wait_visible(self.inventory_items)
    
    def find_item(self, product_key):
        product = ConfigReader.get_product(product_key)
        item_link = (By.ID, product["add_to_cart_id"])
        return self.find_element(item_link)
    
    def is_inventory_item_displayed(self, product_key):
        product = ConfigReader.get_product(product_key)
        if not product:
            raise ValueError(f"Không tìm thấy sản phẩm: {product_key}")
        
        item_link = (By.ID, product["add_to_cart_id"])
        return self.is_displayed(item_link)

    def click_inventory_item(self, product_key):
        product = ConfigReader.get_product(product_key)
        if not product:
            raise ValueError(f"Không tìm thấy sản phẩm: {product_key}")

        item_link = (By.ID, product["add_to_cart_id"].replace("add-to-cart", "item"))
        self.click(item_link)

    def add_to_cart(self, product_key):
        """Thêm sản phẩm vào giỏ hàng"""
        product = ConfigReader.get_product(product_key)
        if not product:
            raise ValueError(f"Không tìm thấy sản phẩm: {product_key}")
        
        add_btn = (By.ID, product["add_to_cart_id"])
        self.click(add_btn)
        return True
    
    def is_add_to_cart_button_displayed(self, product_key):
        """Kiểm tra xem nút thêm vào giỏ hàng có hiển thị hay không"""
        product = ConfigReader.get_product(product_key)
        if not product:
            raise ValueError(f"Không tìm thấy sản phẩm: {product_key}")
        
        add_btn = (By.ID, product["add_to_cart_id"])
        return self.is_displayed(add_btn)
    
    def remove_from_cart(self, product_key):
        """Xóa sản phẩm khỏi giỏ hàng"""
        product = ConfigReader.get_product(product_key)
        if not product:
            raise ValueError(f"Không tìm thấy sản phẩm: {product_key}")
        
        remove_btn = (By.ID, product["remove_id"])
        self.click(remove_btn)
        return True
    
    def is_remove_button_displayed(self, product_key):
        """Kiểm tra xem nút xóa có hiển thị hay không"""
        product = ConfigReader.get_product(product_key)
        if not product:
            raise ValueError(f"Không tìm thấy sản phẩm: {product_key}")
        
        remove_btn = (By.ID, product["remove_id"])
        return self.is_displayed(remove_btn)

    def get_cart_count(self):
        return self.get_text(self.number_of_items_in_cart)

    def is_cart_badge_displayed(self):
        return self.is_displayed(self.number_of_items_in_cart)

    def click_cart_button(self):
        self.click(self.cart_button)