from tests.TestJobsValidator.api_utils.peviitor_update import UpdateAPI
import requests
import allure
import json

class Pushprod:
    
    # Jobs that will be pushed to prod
    def __init__(self, company_name):
        self.company_name = company_name
        self.payload = []
    
    def add_job_details(self, filtered_job_titles, filtered_job_cities, filtered_job_links, filtered_job_types, filtered_job_countries):
        for job_title, job_city, job_link, job_type, job_country in zip(filtered_job_titles, filtered_job_cities, filtered_job_links, filtered_job_types, filtered_job_countries):
            if not any("REMOVED_JOB" in item for item in (job_title, job_city, job_link, job_type, job_country)):
                self.payload.append({
                    "job_link": job_link,
                    "job_title": job_title,
                    "company": self.company_name,
                    "country": job_country,
                    "city": job_city,
                    "remote": job_type,
                    "published": True,
                    "company_name": self.company_name
                })
                
    def set_headers(self):
        updateapi = UpdateAPI()
        updateapi.get_token()
        
        self.deploy_headers = {
        'Authorization': f'Bearer {updateapi.access_token}',
        'Content-Type': 'application/json'
        }
    
    def push_to_prod(self):
        if self.payload:
            pushed_msg = requests.request("POST", "https://api.laurentiumarian.ro/jobs/publish/", headers=self.deploy_headers, data=json.dumps(self.payload)).json()
            assert pushed_msg['message'] == 'Job published'
        