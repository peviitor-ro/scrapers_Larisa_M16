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
import re


JOBS_URL = "https://hosterion.ro/cariere"
SITEMAP_URL = "https://hosterion.ro/sitemap.xml"
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
    job_links = set()

    for job_link in soup.find_all('a', href=True):
        href = job_link['href'].strip()
        if href.startswith('https://hosterion.ro/cariere/'):
            job_links.add(href)

    for href in re.findall(r'"(/cariere/[^"#?]+)"', str(soup)):
        job_links.add(f'https://hosterion.ro{href}')

    sitemap_response = requests.get(url=SITEMAP_URL, headers=DEFAULT_HEADERS)
    for loc in re.findall(r'<loc>\s*([^<]+?)\s*</loc>', sitemap_response.text):
        if re.match(r'https://hosterion\.ro/cariere/[^/]+/?$', loc):
            job_links.add(loc.strip())

    for job_link in sorted(job_links):
        if job_link.rstrip('/') == JOBS_URL:
            continue

        job_response = requests.get(url=job_link, headers=DEFAULT_HEADERS)
        job_soup = BeautifulSoup(job_response.text, 'lxml')
        job_content = job_soup.find('div', attrs={'class': 'content-column'})
        if not job_content:
            continue

        if 'postul nu mai este disponibil' in job_content.get_text(' ', strip=True).lower():
            continue

        title_tag = job_content.find('h1')
        job_title = title_tag.get_text(strip=True) if title_tag else ''
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
