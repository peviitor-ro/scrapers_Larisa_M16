from tests.Test_Selenium_Suite.seleniumutils import TestUtils
from sites.corteva_scraper import scraper as cortevaScraper
import pytest
import allure


company_name = 'corteva'
testutils = TestUtils(company_name)

@pytest.fixture(scope="module")
def get_job_details():
    """
    Fixture for scruing process from the career section.
    """
    scraper_data = cortevaScraper()
    scraped_jobs_data = testutils.scrape_jobs(scraper_data)
    
    return scraped_jobs_data

@pytest.fixture(scope="module")
def scrape_ui(driver, expected_wait):
    # open the browser
    testutils.open_browser(driver, expected_wait)
        
    # Grab the data
    job_details = testutils.get_jobs_selenium()
    
    # Return the browser instance and the data
    yield testutils, job_details
    
    # Close the browser at the end
    testutils.close_browser()
    

@pytest.mark.regression
@pytest.mark.API
def test_corteva_job_count_api(get_job_details, scrape_ui):
    allure.dynamic.title(f"Test number of jobs from the Peviitor against the number of jobs on the {company_name} website")

    scraped_jobs_data = get_job_details
    with allure.step("Step 1: Get job links from the scraper"):
        job_links_scraper = len(scraped_jobs_data[3])
    with allure.step("Step 2: Get job links from the Peviitor API"):
        # Grab the data from peviitor ui
        testutils, job_details = scrape_ui[0], scrape_ui[1]
        job_links_peviitor = len(job_details[2])

    with allure.step("Step 3: Compare number of jobs from the Peviitor against the number of jobs on the company website"):
        allure.attach(f"Expected Results: {job_links_scraper}", name="Expected Results")
        allure.attach(f"Actual Results: {job_links_peviitor}", name="Actual Results")
        testutils.check_job_count(job_links_scraper, job_links_peviitor)

@pytest.mark.regression
@pytest.mark.ui
def test_corteva_titles_scraper(get_job_details, scrape_ui):
    allure.dynamic.title(f"Test job titles from the {company_name} website against Peviitor ui")

    scraped_jobs_data = get_job_details
    with allure.step("Step 1: Get job titles from the scraper"):
        job_titles_scraper = scraped_jobs_data[0]
    
    with allure.step("Step 2: Get job titles from the Peviitor ui"):
        
        # Grab the data from peviitor ui
        testutils, job_details = scrape_ui[0], scrape_ui[1]
        job_titles_peviitor = job_details[0]

    with allure.step("Step 3: Compare job titles from scraper response against Peviitor ui Response"):
        allure.attach(f"Expected Results: {job_titles_scraper}", name="Expected Results")
        allure.attach(f"Actual Results: {job_titles_peviitor}", name="Actual Results")
        testutils.check_scraper_job_titles(job_titles_scraper, job_titles_peviitor)

@pytest.mark.regression
@pytest.mark.ui
def test_corteva_titles_ui(get_job_details, scrape_ui):
    allure.dynamic.title(f"Test job titles from the Peviitor ui against {company_name} website")

    scraped_jobs_data = get_job_details
    with allure.step("Step 1: Get job titles from the scraper"):
        job_titles_scraper = scraped_jobs_data[0]
    
    with allure.step("Step 2: Get job titles from the Peviitor ui"):
        
        # Grab the data from peviitor ui
        testutils, job_details = scrape_ui[0], scrape_ui[1]
        job_titles_peviitor = job_details[0]
        job_titles_elements = job_details[4]

    with allure.step("Step 3: Compare job titles from scraper response against Peviitor ui Response"):
        allure.attach(f"Expected Results: {job_titles_peviitor}", name="Expected Results")
        allure.attach(f"Actual Results: {job_titles_scraper}", name="Actual Results")
        testutils.check_peviitor_job_titles(job_titles_peviitor, job_titles_scraper, job_titles_elements)

@pytest.mark.regression
@pytest.mark.ui
def test_corteva_link_scraper(get_job_details, scrape_ui):
    allure.dynamic.title(f"Test job links from the {company_name} website against Peviitor API Response")

    scraped_jobs_data = get_job_details
    with allure.step("Step 1: Get job links from the scraper"):
        job_links_scraper = scraped_jobs_data[3]
    with allure.step("Step 2: Get job links from the Peviitor API"):
        
        # Grab the data from peviitor ui
        testutils, job_details = scrape_ui[0], scrape_ui[1]
        job_links_peviitor = job_details[2]
        

    with allure.step("Step 3: Compare job links from scraper response against Peviitor API Response"):
        allure.attach(f"Expected Results: {job_links_scraper}", name="Expected Results")
        allure.attach(f"Actual Results: {job_links_peviitor}", name="Actual Results")
        testutils.check_scraper_job_links(job_links_scraper, job_links_peviitor)

@pytest.mark.regression
@pytest.mark.ui
def test_corteva_link_ui(get_job_details, scrape_ui):
    allure.dynamic.title(f"Test job links from the Peviitor ui against the {company_name} website")

    scraped_jobs_data = get_job_details
    with allure.step("Step 1: Get job links from the scraper"):
        job_links_scraper = scraped_jobs_data[3]
    with allure.step("Step 2: Get job links from the Peviitor API"):
        # Grab the data from peviitor ui
        
        testutils, job_details = scrape_ui[0], scrape_ui[1]
        job_titles_peviitor = job_details[0]
        job_links_peviitor = job_details[2]
        job_links_elements = job_details[6]

    with allure.step("Step 3: Compare job links from Peviitor ui against the company website"):
        allure.attach(f"Expected Results: {job_links_scraper}", name="Expected Results")
        allure.attach(f"Actual Results: {job_links_peviitor}", name="Actual Results")
        testutils.check_peviitor_job_links(job_links_scraper, job_links_peviitor, job_titles_peviitor, job_links_elements)

@pytest.mark.regression
@pytest.mark.ui
def test_corteva_company_ui(get_job_details, scrape_ui):
    allure.dynamic.title(f"Test job companies from the {company_name} website against Peviitor ui")

    scraped_jobs_data = get_job_details
    with allure.step("Step 1: Get expected job company names"):
        job_companies_scraper = [company_name] * len(scraped_jobs_data[4])
    with allure.step("Step 2: Get actual job companies from the Peviitor ui"):
        # Grab the data from peviitor ui
        
        testutils, job_details = scrape_ui[0], scrape_ui[1]
        job_companies_peviitor = job_details[3]

    with allure.step("Step 3: Compare job companies from scraper response against Peviitor ui"):
        allure.attach(f"Expected Results: {job_companies_scraper}", name="Expected Results")
        allure.attach(f"Actual Results: {job_companies_peviitor}", name="Actual Results")
        testutils.check_ui_job_company(job_companies_scraper, job_companies_peviitor)