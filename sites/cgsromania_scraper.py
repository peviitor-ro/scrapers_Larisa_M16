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
# Company ---> cgsromania
# Link ------> https://romania.cgsinc.com/vino-in-echipa-cgs/
#
#
#
from sites.__utils.items_struct import Item
from sites.__utils.peviitor_update import UpdateAPI
from sites.__utils.found_county import get_county

from bs4 import BeautifulSoup
import cloudscraper
import re


JOBS_URL = "https://romania.cgsinc.com/vino-in-echipa-cgs/"
COMPANY = "CGSRomania"
COUNTRY = "Romania"
LOGO_LINK = "https://romania.cgsinc.com/wp-content/uploads/2021/05/logo_CGS.svg"

CITY_TRANSLATIONS = {
    "bucharest": "Bucuresti",
    "bucuresti": "Bucuresti",
    "brasov": "Brasov",
    "targu- jiu": "Targu Jiu",
    "targu-jiu": "Targu Jiu",
    "targu jiu": "Targu Jiu",
}

COUNTY_OVERRIDES = {
    "Bucuresti": "Bucuresti",
    "Brasov": "Brasov",
    "Targu Jiu": "Gorj",
}


def normalize_city(city_name):
    city_name = re.sub(r"\s+", " ", city_name).strip(" -–,;:/")
    return CITY_TRANSLATIONS.get(city_name.lower(), city_name)


def get_location_county(city_name):
    return COUNTY_OVERRIDES.get(city_name, get_county(city_name))


def extract_locations(location_text):
    location_text = location_text.replace("Hybrid", "")
    location_text = re.sub(r"\s+", " ", location_text)

    locations = []
    for raw_location in re.split(r"/", location_text):
        city_name = normalize_city(raw_location)
        if city_name and get_location_county(city_name) and city_name not in locations:
            locations.append(city_name)

    return locations


def get_remote_type(title, location):
    combined_text = f"{title} {location}".lower()
    if "remote" in combined_text:
        return "remote"
    if "hybrid" in combined_text:
        return "hybrid"
    if "la sediu" in combined_text:
        return "on-site"
    return "on-site"


def scraper():
    '''
    ... scrape data from CGS Romania scraper.
    '''
    scraper_client = cloudscraper.create_scraper(browser={'browser': 'chrome', 'platform': 'darwin', 'mobile': False})
    soup = BeautifulSoup(scraper_client.get(JOBS_URL, timeout=30).text, 'lxml')

    job_list = []
    for job in soup.find_all("article"):
        link_tag = job.find("a", href=True)
        if "/joburi/" not in link_tag["href"]:
            continue

        card_lines = [line.strip() for line in job.get_text("\n", strip=True).split("\n") if line.strip()]
        if len(card_lines) < 2:
            continue

        title = card_lines[0]
        location_text = card_lines[1]
        locations = extract_locations(location_text)
        if not title or not locations:
            continue

        job_list.append(Item(
            job_title=title,
            job_link=link_tag["href"],
            company=COMPANY,
            country=COUNTRY,
            county=[get_location_county(city_name) for city_name in locations],
            city=locations,
            remote=get_remote_type(title, location_text),
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
