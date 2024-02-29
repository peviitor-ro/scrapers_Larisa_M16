from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class browser:
    
    peviitor_url = "https://www.peviitor.ro"
    
    def __init__(self, driver, expected_wait):
        self.driver = driver
        self.expected_wait = expected_wait
        
    def open_webpage(self):
        self.driver.get(self.peviitor_url)
        
    def close_browser(self):
        self.driver.quit()
        