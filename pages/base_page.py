from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException
from utils.config_reader import ConfigReader

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, ConfigReader.get_explicit_wait())

    def find_element(self, locator):
        try:
            return self.wait.until(EC.presence_of_element_located(locator))
        except TimeoutException as e:
            raise AssertionError(f"Element {locator} not found within timeout: {e}")

    def find_elements(self, locator):
        return self.wait.until(EC.visibility_of_all_elements_located(locator))

    def send_keys(self, locator, text):
        self.find_element(locator).send_keys(text)

    def is_displayed(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator)).is_displayed()
    
    def is_element_visible(self, locator):
        """Check whether an element is visible; return False when not found."""
        try:
            return EC.visibility_of_element_located(locator)(self.driver) is not False
        except (NoSuchElementException, StaleElementReferenceException, TimeoutException):
            return False
    
    def get_text(self, locator):
        return self.find_element(locator).text

    def click(self, locator):
        self.wait.until(EC.element_to_be_clickable(locator)).click()
