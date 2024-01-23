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
        
        # Check if the cities list is a nested list
        job_city = [self.remove_diacritics(city['city']) if isinstance(city['city'], list) else [self.remove_diacritics(city['city'])] for city in scraper_data]
            
        return title, job_city, job_country, job_link

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
        all_future_title, all_future_job_city, all_future_job_country, all_future_job_link = [], [], [], []

        page = 1
        params = TestUtils._set_params(company_name, page, country)
        response_data = TestUtils._get_request(params)
        while response_data:
            all_future_title.extend([title['job_title'][0] for title in response_data])
            all_future_job_country.extend([self.remove_diacritics(country['country'][0]) for country in response_data])
            all_future_job_link.extend([job_link['job_link'][0] for job_link in response_data])
            
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

        return all_future_title, all_future_job_city, all_future_job_country, all_future_job_link
    
    # Remove diacritics from input recursive
    def remove_diacritics(self, item):
        
        # If instance of list remove diacritics recursive
        if isinstance(item, list):
            return [self.remove_diacritics(subitem) for subitem in item]
        else:
            # Remove diacritics from string
            return unidecode(item)
    
    # Utility function for checking missing items
    def get_missing_items(self, list_a, list_b):
        return [item for item in list_a if item not in list_b][:20]

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
    def check_job_cities(self, expected_cities, actual_cities):
        missing_cities = self.get_missing_items(expected_cities, actual_cities)

        if missing_cities:
            msg = f"Peviitor is having extra job cities: {missing_cities}"
        else:
            missing_cities = self.get_missing_items(actual_cities, expected_cities)
            msg = f"Peviitor is missing job cities: {missing_cities}"

        if not expected_cities and not actual_cities:
            msg = f"Scraper is not grabbing any job cities"
            allure.step(msg)
            raise AssertionError(msg)

        allure.step(msg)
        assert expected_cities == actual_cities, msg

    # Check method for job countries
    def check_job_countries(self, expected_countries, actual_countries):
        missing_countries = self.get_missing_items(expected_countries, actual_countries)

        if missing_countries:
            msg = f"Peviitor is having extra job countries: {missing_countries}"
        else:
            missing_countries = self.get_missing_items(actual_countries, expected_countries)
            msg = f"Peviitor is missing job countries: {missing_countries}"

        if not expected_countries and not actual_countries:
            msg = f"Scraper is not grabbing any job countries"
            allure.step(msg)
            raise AssertionError(msg)

        allure.step(msg)
        assert expected_countries == actual_countries, msg

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
        
