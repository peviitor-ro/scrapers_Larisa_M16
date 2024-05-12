from unidecode import unidecode
from tests.push_to_prod import Pushprod
from sites.__utils.peviitor_update import UpdateAPI
import requests
import allure
import re

class CountTestUtils:

    # Check number of jobs using the job links count
    def check_job_count(self, expected_links_count, actual_links_count):

        if expected_links_count < actual_links_count:
            msg = f"Peviitor is having extra jobs not available on company website"
        else:
            msg = f"Company website contains more jobs than on peviitor"
        
        if not expected_links_count and not actual_links_count:
            msg = f"Scraper is not grabbing any job links"
            allure.step(msg)
            raise AssertionError(msg)

        allure.step(msg)
        assert expected_links_count == actual_links_count, msg