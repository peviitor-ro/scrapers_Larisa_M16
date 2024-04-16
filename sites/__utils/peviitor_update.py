#
#
#
#  Send data to Peviitor API!
#  ... OOP version
#
#
import requests
#
import os  # I do not have API KEY
#
import json
#
import time


class UpdateAPI:
    '''
    - Method for clean data,
    - Method for update data,
    - Method for update logo.
    '''

    def __init__(self):
        self.email = os.environ.get('EMAIL')
        self.logo_url = 'https://api.peviitor.ro/v1/logo/add/'

        self.logo_header = {
            'Content-Type': 'application/json',
        }
        
    def get_token(self):

        payload = json.dumps({
        "email": self.email
        })
        
        post_header = {
        'Content-Type': 'application/json'
        }

        self.access_token = requests.request("POST", "https://api.laurentiumarian.ro/get_token", headers=post_header, data=payload).json()['access']

    def add_jobs(self, company_name, data_jobs):

        post_header = {
        'Authorization': f'Bearer {self.access_token}',
        'Content-Type': 'application/json'
        }

        requests.request("POST", "https://api.laurentiumarian.ro/jobs/add/", headers=post_header, data=json.dumps(data_jobs))
        
        # don't delete this lines if you want to see the graph on scraper's page
        file = company_name.lower() + '.py'
        data = {'data': len(data_jobs)}
        dataset_url = f'https://dev.laurentiumarian.ro/dataset/JobsScrapers/{file}/'
        requests.post(dataset_url, json=data)
        ########################################################
    

    def update_jobs(self, company_name: str, data_jobs: list):
        '''
        ... update and clean data on peviitor

        '''
        self.get_token()
        time.sleep(0.2)
        self.add_jobs(company_name, data_jobs)

    def update_logo(self, id_company: str, logo_link: str):
        '''
        ... update logo on peviitor.ro
        '''

        data = json.dumps([{"id": id_company, "logo": logo_link}])
        response = requests.post(self.logo_url, headers=self.logo_header, data=data)

        #  print(f'Logo update ---> succesfuly {response}')
