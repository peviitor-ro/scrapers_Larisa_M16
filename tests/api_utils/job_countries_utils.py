from tests.api_utils.utils import TestUtils
import allure

class CountriesTestUtils(TestUtils):

    # Check method for job countries
    def check_job_countries(self, mainobj, expected_countries, actual_countries, job_titles_scraper, api_job_titles):
        if not expected_countries:
            msg = f"Scraper is not grabbing any job countries"
            allure.step(msg)
            raise AssertionError(msg)

        msg = "An unknown error occured"

        # Check job countries from scraper against the peviitor api
        scraper_actual_countries, scraper_job_titles = TestUtils().get_different_items(expected_countries, actual_countries, job_titles_scraper)

        if scraper_actual_countries:
            msg = f"Peviitor is missing job countries for the following job titles: {scraper_job_titles}"
            for scraper_job_country in scraper_actual_countries:
                for validator_job_country_index, validator_job_country in enumerate(mainobj.filtered_job_countries):
                    if scraper_job_country == validator_job_country:
                        mainobj.filtered_job_countries[validator_job_country_index] = 'REMOVED_JOB'
            allure.step(msg)
            raise AssertionError(msg)
        else:
            # Check job countries from peviitor against the scraper response
            peviitor_actual_countries, peviitor_job_titles = TestUtils().get_different_items(actual_countries, expected_countries, api_job_titles)
            if peviitor_actual_countries:
                msg = f"Peviitor is having extra job countries for the following titles: {peviitor_job_titles}"
                allure.step(msg)
                raise AssertionError(msg)

        allure.step(msg)
        assert expected_countries == actual_countries, msg
