from tests.TestJobsValidator.api_utils.utils import TestUtils
from tests.TestJobsValidator.api_utils.get_county_city import get_proper_city
import allure

class CitiesTestUtils(TestUtils):

    # Check method for job cities
    def check_job_cities(self, actual_cities, job_titles):
        # Itterate over actual cities and get_proper_city > city list or none if one was not found
        
        msg = "Unknown error occured"
        
        missing_cities = []
        missing_cities_job_titles = []
        
        for city_list, job_title in zip(actual_cities, job_titles):
            if not get_proper_city(city_list):
                missing_cities.append(city_list)
                missing_cities_job_titles.append(job_title)
        
        if missing_cities:
            msg = f"Test found mismatching job cities for the following jobs: {missing_cities_job_titles}"

        if not actual_cities and not job_titles:
            msg = f"Cannot grab any job cities or job titles from the validator"
            allure.step(msg)
            raise AssertionError(msg)
        
        allure.step(msg)
        assert missing_cities == [], msg