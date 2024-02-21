from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
import pytest

# Set the location and name of the HTML report
def pytest_configure(config):
    config.option.htmlpath = '.\\Reports\\report_selenium.html'

# Set the HTML Report title Name
def pytest_html_report_title(report):
    report.title = "Full Selenium Test Run"

@pytest.fixture(scope="module")
def driver():
    # Set up the service object
    service = Service(ChromeDriverManager().install())
    
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    
    # For running tests in headless uncomment this
    chrome_options.add_argument('--headless')
    
    # Create the webdriver using the service object
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.maximize_window()
    return driver

@pytest.fixture(scope="module")
def expected_wait(driver):
    return WebDriverWait(driver, 10)