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
# Company ---> toptech
# Link ------> https://www.toptech.ro/cariere.html
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

import requests_html
import requests


def scraper():
    '''
    ... scrape data from toptech scraper.
    '''
    soup = GetStaticSoup("https://www.toptech.ro/cariere.html")
    def get_static_soup(url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup

    job_list = []

    for job in soup.find_all('div', class_='inside-single'):
        title = job.find('p')['strong']
        for job in soup.find_all('div', class_='inside-single'):
         title_element = job.find('p')['strong']

        # Check if the title element is found
        if title_element:
            title = title_element.text.strip()
        else:
            title = 'N/A'


        # get jobs items from response
        job_list.append(Item(
            job_title=title,
            job_link='',
            company='Toptech',
            country='',
            county='',
            city='',
            remote='',
        ).to_dict())

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "toptech"
    logo_link = "logo_link"

    jobs = scraper()
    print(jobs)

    # uncomment if your scraper done
    #UpdateAPI().update_jobs(company_name, jobs)
    #UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
