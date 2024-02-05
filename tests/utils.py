from unidecode import unidecode
import requests
import allure

class TestUtils:

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

    @staticmethod
    def _set_params(company_name, page, country):
        """
        Setting params for peviitor jobs request
        """
        params = {
            'company': company_name,
            'country': country,
            'page': page,
        }
        return params
    
    @staticmethod
    def _get_request(params):
        """
        Send a get request to get the jobs from future
        """
        response = requests.get('https://api.peviitor.ro/v3/search/', params=params).json()
        if 'response' in response and 'docs' in response['response']:
            response_data = response['response']['docs']
            return response_data
        else:
            return []

    def scrape_peviitor(self, company_name, country):
        """
        Get the job details from the peviitor
        """
        all_future_title, all_future_job_city, all_future_job_country, all_future_job_link, all_future_job_companies, all_future_job_types = [], [], [], [], [], []

        page = 1
        params = TestUtils._set_params(company_name, page, country)
        response_data = TestUtils._get_request(params)
        while response_data:
            all_future_title.extend([title['job_title'][0] for title in response_data])
            all_future_job_country.extend([self.remove_diacritics(country['country'][0]) for country in response_data])
            all_future_job_link.extend([job_link['job_link'][0] for job_link in response_data])
            all_future_job_companies.extend([company['company'][0] for company in response_data])
            all_future_job_types.extend([job_link['remote'][0] for job_link in response_data])
            
            # Check if the cities list is a nested list
            city_list = [self.remove_diacritics(city['city']) for city in response_data]
            is_nested = all(isinstance(item, list) for item in city_list)
            
            if is_nested:
                all_future_job_city.extend(city_list)
            else:
                all_future_job_city.extend([self.remove_diacritics(city['city'][0]) for city in response_data])

            page += 1
            params = TestUtils._set_params(company_name, page, country)
            response_data = TestUtils._get_request(params)

        return all_future_title, all_future_job_city, all_future_job_country, all_future_job_link, all_future_job_companies, all_future_job_types
    
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
    def get_different_items(self, expected_list, actual_list, job_titles):
        # Check if actual list is empty
        if not actual_list:
            return expected_list, job_titles
        
        dummy_actual_list = actual_list[:]

        for expected_index, expected_item in enumerate(expected_list):

            # Check if actual list is empty otherwise pop
            if not dummy_actual_list:
                return expected_list[expected_index:], job_titles[expected_index:]
            
            dummy_actual_list.pop(0)
        
        return [], []

    # Check method for job titles
    def check_job_titles(self, expected_titles, actual_titles):
        missing_titles = self.get_missing_items(expected_titles, actual_titles)

        if missing_titles:
            msg = f"Peviitor is having extra job titles: {missing_titles}"
        else:
            missing_titles = self.get_missing_items(actual_titles, expected_titles)
            msg = f"Peviitor is missing job titles: {missing_titles}"

        if not expected_titles and not actual_titles:
            msg = f"Scraper is not grabbing any job titles"
            allure.step(msg)
            raise AssertionError(msg)
        
        allure.step(msg)
        assert expected_titles == actual_titles, msg
        
    # Check method for job cities
    def check_job_cities(self, expected_cities, actual_cities, job_titles_scraper, api_job_titles):
        if not expected_cities:
            msg = f"Scraper is not grabbing any job cities"
            allure.step(msg)
            raise AssertionError(msg)
        
        msg = "An unknown error occurred"
        
        # Check jobs from scraper against the peviitor api
        scraper_actual_cities, scraper_job_titles = self.get_different_items(expected_cities, actual_cities, job_titles_scraper)

        if scraper_actual_cities:
            msg = f"Peviitor is missing job cities for the following job titles: {scraper_job_titles}"
            allure.step(msg)
            raise AssertionError(msg)
        else:
            # Check jobs from peviitor against the scraper response
            peviitor_actual_cities, peviitor_job_titles = self.get_different_items(actual_cities, expected_cities, api_job_titles)
            if peviitor_actual_cities:
                msg = f"Peviitor is having extra job cities for the following job titles: {peviitor_job_titles}"
                allure.step(msg)
                raise AssertionError(msg)

        allure.step(msg)
        assert expected_cities == actual_cities, msg

    # Check method for job countries
    def check_job_countries(self, expected_countries, actual_countries, job_titles_scraper, api_job_titles):
        if not expected_countries:
            msg = f"Scraper is not grabbing any job countries"
            allure.step(msg)
            raise AssertionError(msg)

        msg = "An unknown error occured"

        # Check job countries from scraper against the peviitor api
        scraper_actual_countries, scraper_job_titles = self.get_different_items(expected_countries, actual_countries, job_titles_scraper)

        if scraper_actual_countries:
            msg = f"Peviitor is missing job countries for the following job titles: {scraper_job_titles}"
            allure.step(msg)
            raise AssertionError(msg)
        else:
            # Check job countries from peviitor against the scraper response
            peviitor_actual_countries, peviitor_job_titles = self.get_different_items(actual_countries, expected_countries, api_job_titles)
            if peviitor_actual_countries:
                msg = f"Peviitor is having extra job countries for the following titles: {peviitor_job_titles}"
                allure.step(msg)
                raise AssertionError(msg)

        allure.step(msg)
        assert expected_countries == actual_countries, msg

    # Check method for job types
    def check_job_types(self, expected_types, actual_types, job_titles_scraper, api_job_titles):
        if not expected_types:
            msg = f"Scraper is not grabbing any job types"
            allure.step(msg)
            raise AssertionError(msg)
        
        msg = "An unknown error occured"
        
        # Check job types from scraper against the peviitor api
        scraper_actual_types, scraper_job_titles = self.get_different_items(expected_types, actual_types, job_titles_scraper)
        
        if scraper_actual_types:
            msg = f"Peviitor is missing job types for the following jobs: {scraper_job_titles}"
            allure.step(msg)
            raise AssertionError(msg)
        else:
            # Check job types from peviitor against the scraper response
            peviitor_actual_countries, peviitor_job_titles = self.get_different_items(actual_types, expected_types, api_job_titles)
            if peviitor_actual_countries:
                msg = f"Peviitor is having extra job types for the following titles: {peviitor_job_titles}"
                allure.step(msg)
                raise AssertionError(msg)
        
        allure.step(msg)
        assert expected_types == actual_types, msg

    # Check method for job links
    def check_job_links(self, expected_links, actual_links):
        missing_links = self.get_missing_items(expected_links, actual_links)

        if missing_links:
            msg = f"Peviitor is having extra job links: {missing_links}"
        else:
            missing_links = self.get_missing_items(actual_links, expected_links)
            msg = f"Peviitor is missing job links: {missing_links}"
        
        if not expected_links and not actual_links:
            msg = f"Scraper is not grabbing any job links"
            allure.step(msg)
            raise AssertionError(msg)

        allure.step(msg)
        assert expected_links == actual_links, msg
        
    # Check number of jobs using the job links count
    def check_job_count(self, expected_links_count, actual_links_count):

        if expected_links_count < actual_links_count:
            msg = f"Peviitor is having extra jobs not available on company website"
        else:
            msg = f"Company website contains more jobs than on peviitor"
        
        if not expected_links_count and not actual_links_count:
            msg = f"Scraper is not grabbing any job links"
            allure.step(msg)
            raise AssertionError(msg)

        allure.step(msg)
        assert expected_links_count == actual_links_count, msg
        
    # get http codes for links
    @staticmethod
    def get_http_code(job_links):
        # Set headers for useragent
        headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_8_8; like Mac OS X) AppleWebKit/535.14 (KHTML, like Gecko) Chrome/49.0.3028.253 Mobile Safari/603.0',
        }
        
        # Get status code for every link in list
        return [requests.get(link, headers=headers).status_code for link in job_links]

    # Check method for job links
    def check_code_job_links(self, status_codes_expected_result, status_codes_actual_result):
        http_codes = self.get_missing_items(status_codes_expected_result, status_codes_actual_result)
        msg = ""

        if not http_codes:
            msg = f"Some job links from scraper do not return 200 http status code: {http_codes}"
            allure.step(msg)
        
        if not status_codes_expected_result and not status_codes_actual_result:
            msg = f"Scraper is not grabbing any job links"
            allure.step(msg)
            raise AssertionError(msg)

        if not msg:
            msg = f"An unexpected error occured {status_codes_expected_result} {status_codes_actual_result}"
        assert status_codes_expected_result == status_codes_actual_result, msg
        
    # Check company job name in the response
    def check_job_company(self, expected_company_name: list, actual_company_name: list):
        
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
        