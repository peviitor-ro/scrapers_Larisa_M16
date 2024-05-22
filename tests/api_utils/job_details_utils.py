from tests.api_utils.push_to_prod import Pushprod
from tests.api_utils.peviitor_update import UpdateAPI
from tests.api_utils.utils import TestUtils
from tests.api_utils.job_titles_utils import TitleTestUtils
from tests.api_utils.job_cities_utils import CitiesTestUtils
from tests.api_utils.job_links_utils import LinksTestUtils
from tests.api_utils.job_types_utils import TypeTestUtils
from tests.api_utils.job_countries_utils import CountriesTestUtils

import requests

class JobDetails(TestUtils):
    
    def __init__(self):
        self.titleutils = TitleTestUtils()
        self.cityutils = CitiesTestUtils()
        self.linkutils = LinksTestUtils()
        self.typeutils = TypeTestUtils()
        self.countryutils = CountriesTestUtils()


    @staticmethod
    def _set_params(company_name):
        """
        Setting params for peviitor jobs request
        """
        params = {
            'company': company_name,
            'page': 1,
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

    def scrape_peviitor(self, company_name):
        """
        Get the job details from the peviitor
        """
        all_future_title, all_future_job_city, all_future_job_country, all_future_job_link, all_future_job_companies, all_future_job_types = [], [], [], [], [], []

        params = JobDetails._set_params(company_name)
        response_data = JobDetails._get_request(params)
        
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


        self.filtered_job_titles, self.filtered_job_cities, self.filtered_job_links, self.filtered_job_types, self.filtered_job_countries = all_future_title[:], all_future_job_city[:] ,all_future_job_link[:], all_future_job_types[:], all_future_job_country[:]
        return all_future_title[:], all_future_job_city[:], all_future_job_link[:], all_future_job_types[:], all_future_job_country[:]
    
    def send_to_prod(self, company_name):
        pushprod = Pushprod(company_name)
        pushprod.add_job_details(self.filtered_job_titles, self.filtered_job_cities, self.filtered_job_links, self.filtered_job_types, self.filtered_job_countries)
        pushprod.set_headers()
        pushprod.push_to_prod()

    # Title Section
    def check_special_job_titles(self, expected_titles):
        self.titleutils.check_special_job_titles(expected_titles)
    
    # Cities Section
    def check_job_cities(self, job_cities):
        self.cityutils.check_job_cities(job_cities)
        
    # Links Section
    def check_job_link_content(self, links, job_titles):
        self.linkutils.check_job_link_content(self, links, job_titles)
        
    # Job type section
    def check_job_format_types(self, job_types_validator):
        self.typeutils.check_job_format_types(job_types_validator)
    
    # Countries section
    def check_job_countries(self, job_countries):
        self.countryutils.check_job_countries(self, job_countries)
    