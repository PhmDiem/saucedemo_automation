import pytest
from selenium import webdriver
from tempfile import TemporaryDirectory
from utils.config_reader import ConfigReader
from pages.login_page import LoginPage
from datetime import datetime
import allure
import os

@pytest.fixture(scope="function")
def driver():
    options = webdriver.ChromeOptions()
    temp_profile = TemporaryDirectory(prefix="sauce_demo_")

    if ConfigReader.is_headless():
        options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=options)

    if not ConfigReader.is_headless():
        driver.maximize_window()

    options.add_argument(f"--user-data-dir={temp_profile.name}")

    prefs = {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.password_manager_leak_detection": False,
        "autofill.profile_enabled": False,
        "autofill.credit_card_enabled": False,
    }

    options.add_experimental_option("prefs", prefs)
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--disable-features=PasswordCheck")
    options.add_argument("--disable-features=PasswordManagerOnboarding")
    options.add_argument("--disable-features=AutofillServerCommunication")
    options.add_argument("--no-default-browser-check")
    options.add_argument("--no-first-run")

    driver = None
    try:
        driver = webdriver.Chrome(options=options)
        driver.implicitly_wait(ConfigReader.get_implicit_wait())
        driver.set_page_load_timeout(ConfigReader.get_explicit_wait())
        driver.maximize_window()
        driver.get(ConfigReader.get_url())
        yield driver
    finally:
        if driver is not None:
            try:
                driver.quit()
            except Exception:
                pass
        try:
            temp_profile.cleanup()
        except Exception:
            pass

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
    """Login mặc định standard_user"""
    user = ConfigReader.get_user("standard")
    LoginPage(driver).login(user["username"], user["password"])

@pytest.fixture
def login_as(driver):
    """Login với user_type tùy chọn"""
    def _login(user_type):
        user = ConfigReader.get_user(user_type)
        LoginPage(driver).login(user["username"], user["password"])
    return _login