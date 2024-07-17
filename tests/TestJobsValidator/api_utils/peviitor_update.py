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


    def __init__(self):
        self.email = os.environ.get('API_KEY')

        self.logo_header = {
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        }
        
    def get_token(self):

        payload = json.dumps({
        "email": self.email
        })
        
        post_header = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        }

        self.access_token = requests.request("POST", "https://api.peviitor.ro/v5/get_token/", headers=post_header, data=payload).json()['access']
        