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
#

from sites.__utils.items_struct import Item
from sites.__utils.peviitor_update import UpdateAPI
import requests

from bs4 import BeautifulSoup
from __utils.default_headers import DEFAULT_HEADERS

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
    logo_link = "https://ctdefense.com/wp-content/uploads/2019/03/hoster.png"
    jobs = scraper()

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
