from tests.TestJobsValidator.api_utils.utils import TestUtils
from tests.TestJobsValidator.api_utils.get_county_city import get_proper_county
import allure

class CountyTestUtils(TestUtils):

    # Check method for job counties
    def check_job_counties(self, actual_counties, job_titles):
        # Itterate over actual counties and get_proper_county > county list or none if one was not found
        
        msg = "Unknown error occured"
        
        missing_counties = []
        missing_counties_job_titles = []
        
        for county_list, job_title in zip(actual_counties, job_titles):
            if not get_proper_county(county_list):
                missing_counties.append(county_list)
                missing_counties_job_titles.append(job_title)
        
        if missing_counties:
            msg = f"Test found mismatching job counties for the following jobs: {missing_counties_job_titles}"

        if not actual_counties and not job_titles:
            msg = f"Cannot grab any job counties or job titles from the validator"
            allure.step(msg)
            raise AssertionError(msg)
        
        allure.step(msg)
        assert missing_counties == [], msg