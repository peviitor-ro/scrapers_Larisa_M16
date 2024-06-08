from tests.TestJobsValidator.api_utils.utils import TestUtils
import allure

class CountriesTestUtils(TestUtils):

    # Check method for job countries
    def check_job_countries(self, mainobj, job_countries):
        msg = "An unknown error occured"
        expected_job_country_formats = ["România", "Romania"]
        
        for job_country in job_countries:
            if job_country not in expected_job_country_formats:
                msg = f"One of the job countries is not within the expected job country formats"
                for scraper_job_country_index, scraper_job_country in enumerate(mainobj.filtered_job_countries):
                    if job_country == scraper_job_country:
                        mainobj.filtered_job_countries[scraper_job_country_index] = 'REMOVED_JOB'
                raise AssertionError(msg)
        
        assert job_countries, msg
