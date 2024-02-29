from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException


class Peviitor:
    
    search_input_css = "div.input-container > input"
    search_job_css = "button[class='btn-yellow btn']"
    job_count_class = "bold"
    load_jobs_css = "section.load-more > button"
    job_titles_class = "position"
    job_company_css = "p[class='company']"
    job_location_class = "location"
    job_url_css = "div.button-position > a"

    def __init__(self, expected_wait):
        """
        Setting up the expected wait which will wait for all elements to load
        """
        self.expected_wait = expected_wait
        
    def search_company(self, company):
        """
        Search for a company by name, this will enter the name in the input field
        """
        self.expected_wait.until(EC.presence_of_element_located((By.CSS_SELECTOR , self.search_input_css))).send_keys(company)
    
    def click_on_search(self):
        """
        Click on the search button
        """
        self.expected_wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR , self.search_job_css))).click()
    
    def get_jobs_number(self):
        """
        Get the number of jobs of the company
        """
        return self.expected_wait.until(EC.visibility_of_element_located((By.CLASS_NAME , self.job_count_class))).text

    def load_all_jobs(self):
        """
        Load all jobs by pressing the load more button until it dissapears
        """
        try:
            while True:
                load_jobs_btn = self.expected_wait.until(EC.presence_of_element_located((By.CSS_SELECTOR , self.load_jobs_css)))
                load_jobs_btn.click()
        except (StaleElementReferenceException, TimeoutException):
            pass
        
    def get_all_job_titles(self):
        """
        Get all the job titles on the page
        """
        job_titles = self.expected_wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME , self.job_titles_class)))
        return [job_title.text for job_title in job_titles], job_titles
    
    def get_all_job_companies(self):
        """
        Get all the job companies on the page
        """
        job_companies = self.expected_wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR , self.job_company_css)))
        return [job_company.text for job_company in job_companies], job_companies

    def get_all_job_locations(self):
        """
        Get all the job locations on the page
        """
        job_locations = self.expected_wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME , self.job_location_class)))
        return [[job_location.text] for job_location in job_locations], job_locations
    
    def get_all_job_urls(self):
        """
        Get all the job urls on the page
        """
        job_urls = self.expected_wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR , self.job_url_css)))
        return [job_url.get_attribute("href") for job_url in job_urls], job_urls
