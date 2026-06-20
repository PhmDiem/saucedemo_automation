import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from utils.config_reader import ConfigReader
from datetime import datetime
import allure
import os

@pytest.fixture(scope="function")
def driver():
    driver = webdriver.Firefox()
    driver.maximize_window()
    driver.implicitly_wait(ConfigReader.get_timeout())
    driver.get(ConfigReader.get_url())
    yield driver
    driver.quit()

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    # Chỉ chụp và attach khi test fail
    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver")
        if driver is not None:
            try:
                # Tạo folder screenshots
                screenshot_dir = "screenshots"
                os.makedirs(screenshot_dir, exist_ok=True)

                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                file_name = f"{item.name}_{timestamp}.png"
                screenshot_path = os.path.join(screenshot_dir, file_name)

                # Chụp ảnh
                driver.save_screenshot(screenshot_path)

                # Attach vào Allure Report
                with open(screenshot_path, "rb") as image_file:
                    allure.attach(
                        image_file.read(),
                        name="Screenshot on Failure",
                        attachment_type=allure.attachment_type.PNG
                    )

                print(f"Đã chụp và attach screenshot: {file_name}")

            except Exception as e:
                print(f"Không thể chụp screenshot: {e}")    

@pytest.fixture
def login(driver):
    from pages.login_page import LoginPage
    login_page = LoginPage(driver)
    login_page.login(ConfigReader.get_user("standard")["username"], ConfigReader.get_user("standard")["password"])
    return driver