import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from utils.config_reader import ConfigReader

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.implicitly_wait(ConfigReader.get_timeout())
    driver.get(ConfigReader.get_url())
    yield driver
    driver.quit()

@pytest.fixture
def login(driver):
    from pages.login_page import LoginPage
    login_page = LoginPage(driver)
    login_page.enter_username(ConfigReader.get_user("standard")["username"])
    login_page.enter_password(ConfigReader.get_user("standard")["password"])
    login_page.click_login_button()
    return driver