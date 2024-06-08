from tests.TestJobsValidator.api_utils.push_to_prod import Pushprod
from tests.TestJobsValidator.api_utils.peviitor_update import UpdateAPI
from tests.TestJobsValidator.api_utils.utils import TestUtils
from tests.TestJobsValidator.api_utils.job_titles_utils import TitleTestUtils
from tests.TestJobsValidator.api_utils.job_cities_utils import CitiesTestUtils
from tests.TestJobsValidator.api_utils.job_links_utils import LinksTestUtils
from tests.TestJobsValidator.api_utils.job_types_utils import TypeTestUtils
from tests.TestJobsValidator.api_utils.job_countries_utils import CountriesTestUtils
import allure
import time

import requests

class JobDetails(TestUtils):
    
    def __init__(self):
        self.titleutils = TitleTestUtils()
        self.cityutils = CitiesTestUtils()
        self.linkutils = LinksTestUtils()
        self.typeutils = TypeTestUtils()
        self.countryutils = CountriesTestUtils()


    @staticmethod
    def _set_params(company_name, page=1):
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
    def _get_request(company_name):
        """
        Send a get request to get the jobs from future
        """
        updateapi = UpdateAPI()
        updateapi.get_token()
        
        headers = {
            'accept': 'application/json, text/plain, */*',
            'authorization': f'Bearer {updateapi.access_token}',
        }
        
        params = JobDetails._set_params(company_name)
        
        response = requests.get('https://api.laurentiumarian.ro/jobs/get/', params=params, headers=headers).json()
        
        # List to store all results
        all_results = []

        # Process initial response
        if 'results' in response:
            response_data = response['results']
            all_results.extend(response_data)  # Append initial results to the list
        else:
            allure.attach("No 'results' in initial response.", name="Initial response check", attachment_type=allure.attachment_type.TEXT)

        # Loop to process subsequent pages if they exist
        while 'next' in response and response['next'] is not None:
            params['page'] += 1
            response = requests.get('https://api.laurentiumarian.ro/jobs/get/', params=params, headers=headers).json()
            
            if 'results' in response:
                response_data = response['results']
                all_results.extend(response_data)  # Append results to the list
            else:
                allure.attach("No 'results' in response.", name=f"Page {params['page']} response check", attachment_type=allure.attachment_type.TEXT)
                break
        
        time.sleep(0.5)
        # allure.attach(f"Total results collected: {len(all_results)}", name="Results summary", attachment_type=allure.attachment_type.TEXT)
        # allure.attach(f"Total job title results collected: {len([title['job_title'] for title in all_results])}", name="Results summary", attachment_type=allure.attachment_type.TEXT)
        return all_results

    def scrape_peviitor(self, company_name):
        """
        Get the job details from the peviitor
        """
        all_future_title, all_future_job_city, all_future_job_country, all_future_job_link, all_future_job_companies, all_future_job_types = [], [], [], [], [], []

        response_data = JobDetails._get_request(company_name)
        
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
    def check_job_cities(self, job_cities, job_titles):
        self.cityutils.check_job_cities(job_cities, job_titles)
        
    # Links Section
    def check_job_link_content(self, links, job_titles):
        self.linkutils.check_job_link_content(self, links, job_titles)
        
    # Job type section
    def check_job_format_types(self, job_types_validator):
        self.typeutils.check_job_format_types(job_types_validator)
    
    # Countries section
    def check_job_countries(self, job_countries):
        self.countryutils.check_job_countries(self, job_countries)
    