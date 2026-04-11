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
from sites.__utils.default_headers import DEFAULT_HEADERS


JOBS_URL = "https://hosterion.ro/cariere"
COMPANY = "Hosterion"
COUNTRY = "Romania"
LOGO_LINK = "https://ctdefense.com/wp-content/uploads/2019/03/hoster.png"


def scraper():
    '''
    ... scrape data from Hosterion scraper.
    '''
    response = requests.get(url=JOBS_URL, headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')

    job_list = []
    content_column = soup.find('div', attrs={'class': 'content-column'})
    if not content_column:
        return job_list

    careers_links = []
    for job_link in content_column.find_all('a', href=True):
        href = job_link['href'].strip()
        if not href.startswith('https://hosterion.ro/cariere/'):
            continue

        if href.rstrip('/') == JOBS_URL:
            continue

        careers_links.append(job_link)

    for job in careers_links:
        job_title = job.get_text(strip=True)
        job_link = job['href']
        if not job_title:
            continue

        # get jobs items from response
        job_list.append(Item(
            job_title=job_title,
            job_link=job_link,
            company=COMPANY,
            country=COUNTRY,
            county='Cluj',
            city='Cluj-Napoca',
            remote='on-site',
        ).to_dict())

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = COMPANY
    logo_link = LOGO_LINK
    jobs = scraper()

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
