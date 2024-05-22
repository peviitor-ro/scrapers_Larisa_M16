from tests.api_utils.utils import TestUtils
import allure

class TitleTestUtils(TestUtils):

    # Check method for job titles special characters
    def check_special_job_titles(self, expected_titles):
        # return if any job title contains special characters
        special_job_titles = [TestUtils().check_special_characters(job_title) for job_title in expected_titles if TestUtils().check_special_characters(job_title) != False]
        
        msg = "Unknown error occured"

        if special_job_titles:
            msg = f"Peviitor is having job titles with special characters: {special_job_titles}"
            # for special_job_title in special_job_titles:
            #     for job_title_index, job_title in enumerate(mainobj.filtered_job_titles):
            #         if special_job_title == job_title:
            #             mainobj.filtered_job_titles[job_title_index] = 'REMOVED_JOB'

        if not expected_titles and not special_job_titles:
            msg = f"Scraper is not grabbing any job titles"
            allure.step(msg)
            raise AssertionError(msg)
        
        # Search if there are special job titles missing from expected_titles
        filtered_special_job_titles = [TestUtils().return_without_special_characters(job_title) for job_title in expected_titles]
        allure.attach(f"Scraper Expected Results: {filtered_special_job_titles}", name="Actual Results")
        
        allure.step(msg)
        assert special_job_titles == [], msg