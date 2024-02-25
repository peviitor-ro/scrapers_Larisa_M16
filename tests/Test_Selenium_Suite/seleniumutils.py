from unidecode import unidecode
from peviitor import Peviitor
from browser import browser as webbrowser
import allure

class TestUtils:
    
    def __init__(self, company_name):
        # Element to scroll if an error occours
        self.element_to_scroll = None
        self.company_name = company_name

    def scrape_jobs(self, scraper_data):
        """
        Get the job details from the scrapped page
        """
        title = [title['job_title'] for title in scraper_data]
        job_country = [self.remove_diacritics(country['country']) for country in scraper_data]
        job_link = [job_link['job_link'] for job_link in scraper_data]
        job_type = [job_type['remote'] for job_type in scraper_data]
        
        # Check if the cities list is a nested list
        job_city = [self.remove_diacritics(city['city']) if isinstance(city['city'], list) else [self.remove_diacritics(city['city'])] for city in scraper_data]
            
        return title, job_city, job_country, job_link, job_type
    
    # Remove diacritics from input recursive
    def remove_diacritics(self, item):
        
        # If instance of list remove diacritics recursive
        if isinstance(item, list):
            return [self.remove_diacritics(subitem) for subitem in item]
        else:
            # Remove diacritics from string
            return unidecode(item)
    
    # Utility function for checking missing items
    def get_missing_items(self, expected_list, actual_list):
        return [item for item in expected_list if item not in actual_list][:20]
    
    # Utility function for checking cities/country
    def get_different_items(self, expected_list, actual_list, job_titles, expected_elements=None):
        # Check if actual list is empty
        if not actual_list:
            return expected_list, job_titles
        
        dummy_actual_list = actual_list[:]

        for expected_index, expected_item in enumerate(expected_list):

            # Check if actual list is empty otherwise pop
            if not dummy_actual_list:
                if not expected_elements:
                    return expected_list[expected_index:], job_titles[expected_index:]
                else:
                    return expected_list[expected_index:], job_titles[expected_index:], expected_elements[expected_index:]
            
            dummy_actual_list.pop(0)
        
        if not expected_elements:
            return [], []
        
        return [], [], []
    
    def open_browser(self, driver, expected_wait):
        # driver = driver
        
        self.driver = driver
        self.browser = webbrowser(driver, expected_wait)
        self.browser.open_webpage()  # Open the webpage before each test
        
        self.peviitor = Peviitor(expected_wait)
    
    def close_browser(self):
        self.browser.close_browser()  # Close the browser after each test
        
    def make_screenshot(self):
        # Use execute_script to scroll the element into view
        if self.element_to_scroll:

            self.driver.execute_script("arguments[0].scrollIntoView(true);", self.element_to_scroll[0])
            allure.attach(self.driver.get_screenshot_as_png(), name=f"{self.company_name}_title_ui", attachment_type=allure.attachment_type.PNG)

    # Function to interact with the browser and get job information.
    def get_jobs_selenium(self):
        self.peviitor.search_company(self.company_name)
        self.peviitor.click_on_search()
        self.peviitor.load_all_jobs()

        job_titles = self.peviitor.get_all_job_titles()
        job_cities = self.peviitor.get_all_job_locations()
        job_urls = self.peviitor.get_all_job_urls()
        job_companies = self.peviitor.get_all_job_companies()
        
        job_titles_elem = job_titles[1]
        job_cities_elem = job_cities[1]
        job_urls_elem = job_urls[1]
        job_companies_elem = job_companies[1]
        
        return job_titles[0], job_cities[0], job_urls[0], job_companies[0], job_titles_elem, job_cities_elem, job_urls_elem, job_companies_elem

    # Check method for checking job titles from scraper against peviitor ui jobs
    def check_scraper_job_titles(self, expected_titles, actual_titles):
        if not expected_titles and not actual_titles:
            msg = f"Scraper is not grabbing any job titles"
            allure.step(msg)
            raise AssertionError(msg)
        
        msg = "An unknown error occured"
    
        missing_titles = self.get_missing_items(expected_titles, actual_titles)
        
        if missing_titles:
            msg = f"Peviitor is missing job titles: {missing_titles}"
        
        allure.step(msg)
            
        if len(actual_titles) < len(expected_titles):
            assert sorted(expected_titles) == sorted(actual_titles), f"There are more jobs on the scraper than peviitor: {expected_titles}"
        else:
            assert True

    # Check method for job titles from ui against scraper jobs
    def check_peviitor_job_titles(self, expected_titles, actual_titles, expected_elements):
        if not expected_titles and not actual_titles:
            msg = f"Scraper is not grabbing any job titles"
            allure.step(msg)
            raise AssertionError(msg)
        
        msg = "An unknown error occured"
        
        peviitor_actual_titles, peviitor_expected_elements = self.get_different_items(expected_titles, actual_titles, expected_elements)

        if peviitor_actual_titles:
            msg = f"Peviitor is having extra job titles: {peviitor_actual_titles}"
        
        allure.step(msg)
        
        # If the data does not match make screenshot where bugs
        if sorted(expected_titles) != sorted(actual_titles):
            self.element_to_scroll = peviitor_expected_elements
            self.make_screenshot()
        
        if len(actual_titles) > len(expected_titles):
            assert True
        else:
            assert sorted(expected_titles) == sorted(actual_titles), f"There are less jobs on peviitor than on the company website: {actual_titles}"

        
    # Check method for job cities
    def check_scraper_job_cities(self, expected_cities, actual_cities, api_job_titles, expected_elements):
        if not expected_cities:
            msg = f"Scraper is not grabbing any job cities"
            allure.step(msg)
            raise AssertionError(msg)
        
        msg = "An unknown error occurred"
        

        # Check jobs from peviitor against the scraper response
        scraper_actual_cities, scraper_job_titles, peviitor_expected_elements = self.get_different_items(actual_cities, expected_cities, api_job_titles, expected_elements)
        if scraper_actual_cities:
            msg = f"Peviitor is having extra job cities for the following job titles: {scraper_job_titles}"

        allure.step(msg)
            
        assert sorted(expected_cities) == sorted(actual_cities), msg
        
    # Check method for job cities
    def check_peviitor_job_cities(self, expected_cities, actual_cities, job_titles_peviitor, expected_elements):
        if not expected_cities:
            msg = f"peviitor is not grabbing any job cities"
            allure.step(msg)
            raise AssertionError(msg)
        
        msg = "An unknown error occurred"
        
        # Check jobs from peviitor against the peviitor api
        peviitor_actual_cities, peviitor_job_titles, peviitor_expected_elements = self.get_different_items(expected_cities, actual_cities, job_titles_peviitor, expected_elements)

        if peviitor_actual_cities:
            msg = f"Peviitor is missing job cities for the following job titles: {peviitor_job_titles}"
            
        allure.step(msg)
        
        # # If the data does not match make screenshot where bugs
        if sorted(expected_cities) != sorted(actual_cities):
            self.element_to_scroll = peviitor_expected_elements
            self.make_screenshot()
            
        assert sorted(expected_cities) == sorted(actual_cities), msg

    # # Check method for job types
    # def check_scraper_job_types(self, expected_types, actual_types, job_titles_scraper):
    #     if not expected_types:
    #         msg = f"Scraper is not grabbing any job types"
    #         allure.step(msg)
    #         raise AssertionError(msg)
        
    #     msg = "An unknown error occured"
        
    #     # Check job types from scraper against the peviitor api
    #     scraper_actual_types, scraper_job_titles = self.get_different_items(expected_types, actual_types, job_titles_scraper)
        
    #     if scraper_actual_types:
    #         msg = f"Peviitor is missing job types for the following jobs: {scraper_job_titles}"
        
    #     allure.step(msg)
    #     assert sorted(expected_types) == sorted(actual_types), msg

    # # Check method for job types
    # def check_peviitor_job_types(self, expected_types, actual_types, job_titles_peviitor, expected_elements):
    #     if not expected_types:
    #         msg = f"Scraper is not grabbing any job types"
    #         allure.step(msg)
    #         raise AssertionError(msg)
        
    #     msg = "An unknown error occured"

    #     # Check job types from peviitor against the scraper response
    #     peviitor_actual_cities, peviitor_job_titles, peviitor_expected_elements = self.get_different_items(actual_types, expected_types, job_titles_peviitor, expected_elements)
    #     if peviitor_actual_cities:
    #         msg = f"Peviitor is having extra job types for the following titles: {peviitor_job_titles}"
        
    #     # # If the data does not match make screenshot where bugs
    #     if sorted(expected_types) != sorted(actual_types):
    #         self.element_to_scroll = peviitor_expected_elements
    #         self.make_screenshot()
        
    #     allure.step(msg)
    #     assert sorted(expected_types) == sorted(actual_types), msg

    # Check method for job links
    def check_scraper_job_links(self, expected_links, actual_links):
        if not expected_links and not actual_links:
            msg = f"Scraper is not grabbing any job links"
            allure.step(msg)
            raise AssertionError(msg)
        
        msg = "An unknown error occured"

        missing_links = self.get_missing_items(expected_links, actual_links)
        if missing_links:
            msg = f"Peviitor is missing job links: {missing_links}"

        allure.step(msg)
        assert sorted(expected_links) == sorted(actual_links), msg

    # Check method for job links
    def check_peviitor_job_links(self, expected_links, actual_links, job_titles, expected_elements):
        if not expected_links and not actual_links:
            msg = f"Scraper is not grabbing any job links"
            allure.step(msg)
            raise AssertionError(msg)
        
        msg = "An unknown error occured"
        
        # self.get_different_items(expected_links, actual_links, job_titles, expected_elements)
        # missing_links = self.get_missing_items(expected_links, actual_links)
        peviitor_actual_links, peviitor_job_titles, peviitor_expected_elements = self.get_different_items(expected_links, actual_links, job_titles, expected_elements)

        if peviitor_actual_links:
            msg = f"Peviitor is having extra job links: {peviitor_actual_links}"

        allure.step(msg)
        
        # If the data does not match make screenshot where bugs
        if sorted(expected_links) != sorted(actual_links):
            self.element_to_scroll = peviitor_expected_elements
            self.make_screenshot()
        
        assert sorted(expected_links) == sorted(actual_links), msg
        
    # Check number of jobs using the job links count
    def check_job_count(self, expected_links_count, actual_links_count):
        
        if not expected_links_count and not actual_links_count:
            msg = f"Scraper is not grabbing any job links"
            allure.step(msg)
            raise AssertionError(msg)

        if expected_links_count < actual_links_count:
            msg = f"Peviitor is having extra jobs not available on company website"
        else:
            msg = f"Company website contains more jobs than on peviitor"

        allure.step(msg)
        assert expected_links_count == actual_links_count, msg
        
    # Check company job name in the response
    def check_ui_job_company(self, expected_company_name: list, actual_company_name: list):
        
        # Lowercase all items in list to ensure proper comparison
        expected_company_name, actual_company_name = [name.lower() for name in expected_company_name], [name.lower() for name in actual_company_name]
        
        # If no actual company name is in the API
        if not actual_company_name:
            msg = f"No results display the company name within the API Response"
            allure.step(msg)
            raise AssertionError(msg)
        
        # If the actual company name in the api does not correspond to expected company name raise error
        for actual_name, expected_name in zip(actual_company_name, expected_company_name):
            if actual_name != expected_name:
                msg = f"Company name does not match for one of the job results from the API Response"
                allure.step(msg)
                raise AssertionError(msg)
        
        assert expected_company_name == actual_company_name, "An unknown error occured in the API job company name test case"
        