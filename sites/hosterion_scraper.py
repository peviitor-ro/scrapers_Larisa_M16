#
#
#  Basic for scraping data from static pages
# ------ IMPORTANT! ------
# if you need return soup object:
# you cand import from __utils -> GetHtmlSoup
# if you need return regex object:
# you cand import from __utils ->
# ---> get_data_with_regex(expression: str, object: str)
#
# Company ---> Hosterion
# Link ------> https://hosterion.ro/cariere
#
#
from bs4 import BeautifulSoup
from __utils import (
    GetStaticSoup,
    get_county,
    get_job_type,
    Item,
    UpdateAPI,
)
import requests

from sites.__utils.default_headers import DEFAULT_HEADERS



def scraper():
    '''
    ... scrape data from Hosterion scraper.
    '''
    response = requests.get(url="https://hosterion.ro/cariere",
                            headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')
    
    job_list = []
    for job in soup.find_all('div', attrs={'class':'content-column'}):
        job_title = job.find('a').text.strip()
        job_link = job.find('a')['href']
        
        # get jobs items from response
        job_list.append(Item(
            job_title=job_title,
            job_link=job_link,
            company='Hosterion',
            country='Romania',
            county= 'Cluj',
            city='Cluj-Napoca',
            remote='onsite',
        ).to_dict())

    return job_list

def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "Hosterion"
    logo_link = "data:image/png;base64,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"

    jobs = scraper()

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
