from tests.api_utils.utils import TestUtils
import allure


class TypeTestUtils:

    # Check method for job types
    def check_job_types(self, expected_types, actual_types, job_titles_scraper, api_job_titles):
        
        if not expected_types:
            msg = f"Scraper is not grabbing any job types"
            allure.step(msg)
            raise AssertionError(msg)
        
        msg = "An unknown error occured"
        
        expected_types, actual_types, job_titles_scraper, api_job_titles = sorted(expected_types), sorted(actual_types), sorted(job_titles_scraper), sorted(api_job_titles)
        
        # Check job types from scraper against the peviitor api
        scraper_actual_types, scraper_job_titles = TestUtils().get_different_items(expected_types, actual_types, job_titles_scraper)
        
        if scraper_actual_types:
            msg = f"Peviitor is missing job types for the following jobs: {scraper_job_titles}"
            allure.step(msg)
            raise AssertionError(msg)
        else:
            # Check job types from peviitor against the scraper response
            peviitor_actual_countries, peviitor_job_titles = TestUtils().get_different_items(actual_types, expected_types, api_job_titles)
            if peviitor_actual_countries:
                msg = f"Peviitor is having extra job types for the following titles: {peviitor_job_titles}"
                allure.step(msg)
                raise AssertionError(msg)
        
        allure.step(msg)
        assert expected_types == actual_types, msg
    
    def check_job_format_types(self, job_types_scraper):
        msg = "An unknown error occured"
        expected_job_type_formats = ["hybrid", "remote", "on-site"]
        
        for job_type in job_types_scraper:
            if job_type not in expected_job_type_formats:
                msg = f"One of the job format types is not within the expected job type formats"
                # for scraper_job_type_index, scraper_job_type in enumerate(mainobj.filtered_job_types):
                #     if job_type == scraper_job_type:
                #         mainobj.filtered_job_titles[scraper_job_type_index] = 'REMOVED_JOB'
                raise AssertionError(msg)
        
        assert job_types_scraper, msg