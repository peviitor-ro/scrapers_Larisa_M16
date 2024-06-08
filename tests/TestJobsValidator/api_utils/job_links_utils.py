from tests.TestJobsValidator.api_utils.utils import TestUtils
from bs4 import BeautifulSoup
import subprocess
import time
import allure

class LinksTestUtils(TestUtils):

    @staticmethod
    def get_html_content(url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_8_8; like Mac OS X) AppleWebKit/535.14 (KHTML, like Gecko) Chrome/49.0.3028.253 Mobile Safari/603.0',
        }
        
        try:
            # Construct the curl command
            command = [
                'curl', '-s', '-A', headers['User-Agent'], url
            ]
            # Execute the curl command and capture the output
            result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=False)
            # Check if there was an error
            if result.returncode != 0:
                raise Exception(result.stderr.decode('utf-8'))
            # Decode the output using utf-8
            return result.stdout.decode('utf-8')
        except Exception as e:
            # Handle exceptions (e.g., network errors, invalid responses)
            print(f"An error occurred: {e}")
            return None
    
    # Check content of the page for the job title
    def check_job_link_content(self, mainobj, links, job_titles):
        missing_job_links = []
        missing_job_titles = []
        for link, job_title in zip(links, job_titles):
            job_content = LinksTestUtils().get_html_content(link)
            
            # Section where the content is not loaded after the request
            if job_content is None:
                missing_job_links.append(link)
                missing_job_titles.append(job_title)
                print("Job Page content has not been loaded")
                for job_link_index, job_link in enumerate(mainobj.filtered_job_links):
                    if job_link == link:
                        mainobj.filtered_job_links[job_link_index] = 'REMOVED_JOB'
                continue
            
            # Section that run in case the job page content is loaded
            soup = BeautifulSoup(job_content, 'html.parser')
            job_content = soup.get_text()
            if job_title not in job_content:
                missing_job_links.append(link)
                missing_job_titles.append(job_title)
                for job_link_index, job_link in enumerate(mainobj.filtered_job_links):
                    if job_link == link:
                        mainobj.filtered_job_links[job_link_index] = 'REMOVED_JOB'
        
        assert missing_job_links == [], f"The following job links {missing_job_links} do not contain the expected job title: {missing_job_titles}"
