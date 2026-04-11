#
#
#  Basic for scraping data from static pages
#
# ------ IMPORTANT! ------
# if you need return soup object:
# you cand import from __utils -> GetHtmlSoup
# if you need return regex object:
# you cand import from __utils ->
# ---> get_data_with_regex(expression: str, object: str)
#
# Company ---> jumbo
# Link ------> https://corporate.e-jumbo.gr/ro/job-opportunities/theseis-ergasias/
#
#
#
from sites.__utils.items_struct import Item
from sites.__utils.peviitor_update import UpdateAPI
from sites.__utils.found_county import get_county

from bs4 import BeautifulSoup
import cloudscraper


JOBS_URL = "https://corporate.e-jumbo.gr/ro/job-opportunities/theseis-ergasias/"
BASE_URL = "https://corporate.e-jumbo.gr"
COMPANY = "Jumbo"
COUNTRY = "Romania"
LOGO_LINK = "https://corporate.e-jumbo.gr/uploads/images/logo.png"

CITY_KEYWORDS = {
    "timisoara": "Timisoara",
    "constanta": "Constanta",
    "militari": "Bucuresti",
    "oradea": "Oradea",
    "sibiu": "Sibiu",
    "pallady": "Bucuresti",
    "arad": "Arad",
    "berceni": "Bucuresti",
    "ghiroda": "Timisoara",
    "giroc": "Timisoara",
}

COUNTY_OVERRIDES = {
    "Bucuresti": "Bucuresti",
    "Timisoara": "Timis",
    "Constanta": "Constanta",
    "Oradea": "Bihor",
    "Sibiu": "Sibiu",
    "Arad": "Arad",
}


def get_location_county(city_name):
    return COUNTY_OVERRIDES.get(city_name, get_county(city_name))


def create_scraper():
    return cloudscraper.create_scraper(browser={'browser': 'chrome', 'platform': 'darwin', 'mobile': False})


def extract_city(job_title):
    title_lower = job_title.lower()
    for keyword, city_name in CITY_KEYWORDS.items():
        if keyword in title_lower:
            return city_name

    return ""


def scraper():
    '''
    ... scrape data from jumbo scraper.
    '''
    scraper_client = create_scraper()
    soup = BeautifulSoup(scraper_client.get(JOBS_URL, timeout=30).text, 'lxml')

    job_list = []
    for job in soup.select('a.job-box'):
        country_tag = job.select_one('div.country')
        name_tag = job.select_one('div.name')
        if not country_tag or not name_tag:
            continue

        if country_tag.get_text(strip=True).lower() != 'romania':
            continue

        job_title = name_tag.get_text(strip=True)
        city = extract_city(job_title)
        if not city:
            continue

        job_list.append(Item(
            job_title=job_title,
            job_link=BASE_URL + job['href'],
            company=COMPANY,
            country=COUNTRY,
            county=get_location_county(city),
            city=city,
            remote='on-site'
        ).to_dict())

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "jumbo"
    logo_link = LOGO_LINK

    jobs = scraper()

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
