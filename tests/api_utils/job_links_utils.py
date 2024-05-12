from unidecode import unidecode
from tests.push_to_prod import Pushprod
from sites.__utils.peviitor_update import UpdateAPI
from tests.api_utils.utils import TestUtils
import requests
import allure
import re

class LinksTestUtils(TestUtils):

    # Check method for job links
    def check_job_links(self, expected_links, actual_links):
        missing_links = TestUtils().get_missing_items(expected_links, actual_links)

        if missing_links:
            msg = f"Peviitor is having extra job links: {missing_links}"
        else:
            missing_links = TestUtils().get_missing_items(actual_links, expected_links)
            msg = f"Peviitor is missing job links: {missing_links}"
        
        if not expected_links and not actual_links:
            msg = f"Scraper is not grabbing any job links"
            allure.step(msg)
            raise AssertionError(msg)

        allure.step(msg)
        assert expected_links == actual_links, msg
    
    # get http codes for links
    @staticmethod
    def get_http_code(job_links):
        # Set headers for useragent
        headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_8_8; like Mac OS X) AppleWebKit/535.14 (KHTML, like Gecko) Chrome/49.0.3028.253 Mobile Safari/603.0',
        }
        
        # Get status code for every link in list
        return [requests.get(link, headers=headers).status_code for link in job_links]

    # Check method for job links
    def check_code_job_links(self, mainobj, status_codes_expected_result, status_codes_actual_result):
        http_codes = TestUtils().get_missing_items(status_codes_expected_result, status_codes_actual_result)
        msg = ""

        if not http_codes:
            msg = f"Some job links from scraper do not return 200 http status code: {http_codes}"
            allure.step(msg)
            for job_link_http_index, http_code in enumerate(status_codes_actual_result):
                if http_code != 200:
                    mainobj.filtered_job_links[job_link_http_index] = 'REMOVED_JOB'
        
        if not status_codes_expected_result and not status_codes_actual_result:
            msg = f"Scraper is not grabbing any job links"
            allure.step(msg)
            raise AssertionError(msg)

        if not msg:
            msg = f"An unexpected error occured {status_codes_expected_result} {status_codes_actual_result}"
        assert status_codes_expected_result == status_codes_actual_result, msg