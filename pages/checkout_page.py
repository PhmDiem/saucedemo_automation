from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class CheckoutStepOnePage(BasePage):
    """Checkout Step 1 — Điền thông tin"""

    def __init__(self, driver):
        super().__init__(driver)
        self.first_name_input  = (By.ID, "first-name")
        self.last_name_input   = (By.ID, "last-name")
        self.postal_code_input = (By.ID, "postal-code")
        self.continue_button   = (By.ID, "continue")
        self.cancel_button     = (By.ID, "cancel")
        self.error_message     = (By.XPATH, '//h3[@data-test="error"]')

    def is_checkout_step_one_displayed(self) -> bool:
        return self.is_displayed(self.first_name_input)

    def enter_information(self, first_name, last_name, postal_code):
        self.send_keys(self.first_name_input, first_name)
        self.send_keys(self.last_name_input, last_name)
        self.send_keys(self.postal_code_input, postal_code)

    def click_continue(self):
        self.click(self.continue_button)

    def click_cancel(self):
        self.click(self.cancel_button)

    def get_error_message(self) -> str:
        return self.get_text(self.error_message)

    def is_error_displayed(self) -> bool:
        return self.is_displayed(self.error_message)


class CheckoutStepTwoPage(BasePage):
    """Checkout Step 2 — Order Summary"""

    def __init__(self, driver):
        super().__init__(driver)
        self.item_name    = (By.CLASS_NAME, "inventory_item_name")
        self.item_price   = (By.CLASS_NAME, "inventory_item_price")
        self.subtotal     = (By.CLASS_NAME, "summary_subtotal_label")
        self.tax          = (By.CLASS_NAME, "summary_tax_label")
        self.total        = (By.CLASS_NAME, "summary_total_label")
        self.finish_button = (By.ID, "finish")
        self.cancel_button = (By.ID, "cancel")
        self.complete_header = (By.CLASS_NAME, "complete-header")

    def is_checkout_step_two_displayed(self) -> bool:
        return self.is_displayed(self.total)

    def get_item_name(self) -> str:
        return self.get_text(self.item_name)

    def get_item_price(self) -> str:
        return self.get_text(self.item_price)

    def get_subtotal(self) -> str:
        """VD: 'Item total: $9.99'"""
        return self.get_text(self.subtotal)

    def get_tax(self) -> str:
        """VD: 'Tax: $0.80'"""
        return self.get_text(self.tax)

    def get_total(self) -> str:
        """VD: 'Total: $10.79'"""
        return self.get_text(self.total)

    def get_subtotal_value(self) -> float:
        """Lấy số từ 'Item total: $9.99' → 9.99"""
        return float(self.get_subtotal().replace("Item total: $", ""))

    def get_tax_value(self) -> float:
        """Lấy số từ 'Tax: $0.80' → 0.80"""
        return float(self.get_tax().replace("Tax: $", ""))

    def get_total_value(self) -> float:
        """Lấy số từ 'Total: $10.79' → 10.79"""
        return float(self.get_total().replace("Total: $", ""))

    def click_finish(self):
        self.click(self.finish_button)

    def click_cancel(self):
        self.click(self.cancel_button)

    def is_order_complete(self) -> bool:
        return self.is_displayed(self.complete_header)