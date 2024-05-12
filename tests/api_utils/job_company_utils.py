from unidecode import unidecode
from tests.push_to_prod import Pushprod
from sites.__utils.peviitor_update import UpdateAPI
import requests
import allure
import re

class CompanyTestUtils:

    # Check company job name in the response
    def check_job_company(self, expected_company_name: list, actual_company_name: list):
        
        # Lowercase all items in list to ensure proper comparison
        expected_company_name, actual_company_name = [name.lower() for name in expected_company_name], [name.lower() for name in actual_company_name]
        
        # If no actual company name is in the API
        if not actual_company_name:
            msg = f"No results display the company name within the API Response"
            allure.step(msg)
            raise AssertionError(msg)
        
        # If the actual company name in the api does not correspond to expected company name raise error
        for actual_name, expected_name in zip(actual_company_name, expected_company_name):
            if actual_name != expected_name:
                msg = f"Company name does not match for one of the job results from the API Response"
                allure.step(msg)
                raise AssertionError(msg)
        
        assert expected_company_name == actual_company_name, "An unknown error occured in the API job company name test case"