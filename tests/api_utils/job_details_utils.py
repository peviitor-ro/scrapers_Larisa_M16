from tests.api_utils.push_to_prod import Pushprod
from sites.__utils.peviitor_update import UpdateAPI
from tests.api_utils.utils import TestUtils
from tests.api_utils.job_titles_utils import TitleTestUtils
from tests.api_utils.job_cities_utils import CitiesTestUtils
from tests.api_utils.job_links_utils import LinksTestUtils
from tests.api_utils.job_types_utils import TypeTestUtils
from tests.api_utils.job_count_utils import CountTestUtils
from tests.api_utils.job_company_utils import CompanyTestUtils
from tests.api_utils.job_countries_utils import CountriesTestUtils

import requests

class JobDetails(TestUtils):
    
    def __init__(self):
        self.titleutils = TitleTestUtils()
        self.cityutils = CitiesTestUtils()
        self.linkutils = LinksTestUtils()
        self.typeutils = TypeTestUtils()
        self.countutils = CountTestUtils()
        self.companyutils = CompanyTestUtils()
        self.countryutils = CountriesTestUtils()

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
            
        # Filtered jobs that we will push to prod
        self.filtered_job_titles, self.filtered_job_cities, self.filtered_job_links, self.filtered_job_types, self.filtered_job_countries = title[:], job_city[:], job_link[:], job_type[:], job_country[:]
        
        return title, job_city, job_country, job_link, job_type

    @staticmethod
    def _set_params(company_name, page, country):
        """
        Setting params for peviitor jobs request
        """
        params = {
            'company': company_name,
            'page': page,
            'page_size': '10000',
            'order': 'all',
            'search': '',
        }
        
        return params
    
    @staticmethod
    def _get_request(params):
        """
        Send a get request to get the jobs from future
        """
        updateapi = UpdateAPI()
        updateapi.get_token()
        
        headers = {
            'accept': 'application/json, text/plain, */*',
            'authorization': f'Bearer {updateapi.access_token}',
        }
        
        response = requests.get('https://api.laurentiumarian.ro/jobs/get/', params=params, headers=headers).json()
        if 'results' in response:
            response_data = response['results']
            return response_data
        else:
            return []

    def scrape_peviitor(self, company_name, country):
        """
        Get the job details from the peviitor
        """
        all_future_title, all_future_job_city, all_future_job_country, all_future_job_link, all_future_job_companies, all_future_job_types = [], [], [], [], [], []

        page = 1
        params = JobDetails._set_params(company_name, page, country)
        response_data = JobDetails._get_request(params)
        while response_data:
            all_future_title.extend([title['job_title'] for title in response_data])
            all_future_job_country.extend([self.remove_diacritics(country['country'][0]) for country in response_data])
            all_future_job_link.extend([job_link['job_link'] for job_link in response_data])
            all_future_job_companies.extend([company['company'] for company in response_data])
            all_future_job_types.extend([job_link['remote'] for job_link in response_data])
            
            # Check if the cities list is a nested list
            city_list = [self.remove_diacritics(city['city']) for city in response_data]
            is_nested = all(isinstance(item, list) for item in city_list)
            
            if is_nested:
                all_future_job_city.extend(city_list)
            else:
                all_future_job_city.extend([self.remove_diacritics(city['city'][0]) for city in response_data])

            page += 1
            params = JobDetails._set_params(company_name, page, country)
            response_data = JobDetails._get_request(params)

        return all_future_title, all_future_job_city, all_future_job_country, all_future_job_link, all_future_job_companies, all_future_job_types
    
    def send_to_prod(self, company_name):
        pushprod = Pushprod(company_name)
        pushprod.add_job_details(self.filtered_job_titles, self.filtered_job_cities, self.filtered_job_links, self.filtered_job_types, self.filtered_job_countries)
        pushprod.set_headers()
        pushprod.push_to_prod()
        # print(self.filtered_job_titles, self.filtered_job_cities, self.filtered_job_links, self.filtered_job_types, self.filtered_job_countries)
    
    # Title Section
    def check_job_titles(self, expected_titles, actual_titles):
        self.titleutils.check_job_titles(expected_titles, actual_titles)
        
    def check_special_job_titles(self, expected_titles):
        self.titleutils.check_special_job_titles(expected_titles)
    
    # Cities Section
    def check_job_cities(self, expected_cities, actual_cities, job_titles_scraper, api_job_titles):
        self.cityutils.check_job_cities(expected_cities, actual_cities, job_titles_scraper, api_job_titles)
        
    # Links Section
    def check_job_links(self, expected_links, actual_links):
        self.linkutils.check_job_links(expected_links, actual_links)
    
    def get_http_code(self, job_links):
        return LinksTestUtils().get_http_code(job_links)
        
    def check_code_job_links(self, status_codes_expected_result, status_codes_actual_result):
        self.linkutils.check_code_job_links(status_codes_expected_result, status_codes_actual_result)

    # Type Section
    def check_job_types(self, expected_types, actual_types, job_titles_scraper, api_job_titles):
        self.typeutils.check_job_types(expected_types, actual_types, job_titles_scraper, api_job_titles)
    
    def check_job_format_types(self, job_types_scraper):
        self.typeutils.check_job_format_types(job_types_scraper)
    
    # Count section
    def check_job_count(self, expected_links_count, actual_links_count):
        self.countutils.check_job_count(expected_links_count, actual_links_count)
    
    # Countries section
    def check_job_countries(self, expected_countries, actual_countries, job_titles_scraper, api_job_titles):
        self.countryutils.check_job_countries(self, expected_countries, actual_countries, job_titles_scraper, api_job_titles)
    
    # Company section
    def check_job_company(self, expected_company_name, actual_company_name):
        self.companyutils.check_job_company(expected_company_name, actual_company_name)