from unidecode import unidecode
from tests.api_utils.utils import TestUtils
import allure

class CitiesTestUtils(TestUtils):

    # Check method for job cities
    def check_job_cities(self, expected_cities, actual_cities, job_titles_scraper, api_job_titles):
        expected_cities, actual_cities, job_titles_scraper, api_job_titles = sorted(expected_cities), sorted(actual_cities), sorted(job_titles_scraper), sorted(api_job_titles)
        if not expected_cities:
            msg = f"Scraper is not grabbing any job cities"
            allure.step(msg)
            raise AssertionError(msg)
        
        msg = "An unknown error occurred"
        
        # Check jobs from scraper against the peviitor api
        scraper_actual_cities, scraper_job_titles = TestUtils().get_different_items(expected_cities, actual_cities, job_titles_scraper)

        if scraper_actual_cities:
            msg = f"Peviitor is missing job cities for the following job titles: {scraper_job_titles}"
            allure.step(msg)
            raise AssertionError(msg)
        else:
            # Check jobs from peviitor against the scraper response
            peviitor_actual_cities, peviitor_job_titles = TestUtils().get_different_items(actual_cities, expected_cities, api_job_titles)
            if peviitor_actual_cities:
                msg = f"Peviitor is having extra job cities for the following job titles: {peviitor_job_titles}"
                allure.step(msg)
                raise AssertionError(msg)

        allure.step(msg)
        assert expected_cities == actual_cities, msg