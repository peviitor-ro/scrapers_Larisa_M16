from tests.TestJobsValidator.module_names import module_names
from tests.TestJobsValidator.api_utils.job_details_utils import JobDetails
import importlib
import pytest


class SetupTests:
    jobdetails = JobDetails()
    
    def import_all_modules(self):
        return module_names
    
    def get_jobs_careers(self, scraper_class):
        """
        Fixture for scraping process from the career section.
        """
        self.scraper_data = self.jobdetails.scrape_peviitor(scraper_class)
        return self.scraper_data

class TestScrapers:
    setup_tests = None  # Class attribute to hold SetupTests instance
    
    @pytest.fixture(scope="class", params=SetupTests().import_all_modules())
    def scraper_class(self, request):
        return request.param

    @pytest.fixture(scope="class")
    def setup(self, scraper_class):
        TestScrapers.setup_tests = SetupTests()
        peviitor_jobs_data = TestScrapers.setup_tests.get_jobs_careers(scraper_class)
        yield peviitor_jobs_data
        TestScrapers.setup_tests.jobdetails.send_to_prod(scraper_class)

    # @pytest.mark.smoke
    # def test_scrapers_special_title(self, setup):
    #     """
    #     Test job titles contain special characters
    #     """
    #     peviitor_jobs_data = setup
    #     job_titles = peviitor_jobs_data[0]
    #     TestScrapers.setup_tests.jobdetails.check_special_job_titles(job_titles)
        
    @pytest.mark.smoke
    def test_job_link_content(self, setup):
        """
        Test job links for the job title presence in the html response output
        """
        
        peviitor_jobs_data = setup
        job_links = peviitor_jobs_data[2]
        job_titles = peviitor_jobs_data[0]
        TestScrapers.setup_tests.jobdetails.check_job_link_content(job_links, job_titles)
    
    # @pytest.mark.smoke
    # def test_job_types(self, setup):
    #     """
    #     Test job types match ['hybrid', 'remote', 'on-site']
    #     """
    #     peviitor_jobs_data = setup
    #     job_types = peviitor_jobs_data[3]
    #     TestScrapers.setup_tests.jobdetails.check_job_format_types(job_types)

    @pytest.mark.smoke
    def test_job_countries(self, setup):
        """
        Test job countries match Romania
        """
        peviitor_jobs_data = setup
        job_countries = peviitor_jobs_data[4]
        TestScrapers.setup_tests.jobdetails.check_job_countries(job_countries)
    
    # @pytest.mark.smoke
    # def test_job_cities(self, setup):
    #     """
    #     Test job titles contain special characters
    #     """
    #     peviitor_jobs_data = setup
    #     job_titles = peviitor_jobs_data[0]
    #     job_cities = peviitor_jobs_data[1]
    #     TestScrapers.setup_tests.jobdetails.check_job_cities(job_cities, job_titles)