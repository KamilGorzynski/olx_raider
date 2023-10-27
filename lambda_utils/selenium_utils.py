import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

from lambda_utils.const import OLX_LINK, IS_LOCAL


def get_selenium_driver():
    options = Options()
    options.binary_location = (
        "./headless-chromium" if IS_LOCAL else "/opt/chrome/chrome"
    )
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--single-process")
    options.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(
        "./chromedriver" if IS_LOCAL else "/opt/chromedriver", options=options
    )


def get_html(driver):
    driver.get(OLX_LINK)
    wait = WebDriverWait(driver, 20)
    element = EC.visibility_of_element_located(
        (By.CSS_SELECTOR, "#onetrust-accept-btn-handler")
    )
    wait.until(element).click()
    return driver.page_source
