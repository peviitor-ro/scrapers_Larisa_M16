#
#
#  Basic for scraping data from static pages
# ------ IMPORTANT! ------
# if you need return soup object:
# you cand import from sites.__utils -> GetHtmlSoup
# if you need return regex object:
# you cand import from sites.__utils ->
# ---> get_data_with_regex(expression: str, object: str)
#
# Company ---> centric
# Link ------> https://careers.centric.eu/ro/open-positions/
#
#
#
from sites.__utils.req_bs4_shorts import GetStaticSoup
from sites.__utils.items_struct import Item
from sites.__utils.peviitor_update import UpdateAPI
from sites.__utils.found_county import get_county

import re


JOBS_URL = "https://careers.centric.eu/ro/open-positions/"
COMPANY = "Centric"
COUNTRY = "Romania"
LOGO_LINK = "https://careers.centric.eu/static/images/logo.svg"

CITY_TRANSLATIONS = {
    "iași": "Iasi",
    "iasi": "Iasi",
}

COUNTY_OVERRIDES = {
    "Iasi": "Iasi",
}


def normalize_city(city_name):
    city_name = re.sub(r"\s+", " ", city_name).strip(" -–,;:/")
    return CITY_TRANSLATIONS.get(city_name.lower(), city_name)


def get_location_county(city_name):
    return COUNTY_OVERRIDES.get(city_name, get_county(city_name))


def extract_city(job):
    for item in job.select(".vacancy-card__metadata-item"):
        city = normalize_city(item.get_text(" ", strip=True))
        if city:
            return city
    return ""


def scraper():
    '''
    ... scrape data from Centric scraper.
    '''
    soup = GetStaticSoup(JOBS_URL)

    job_list = []
    for job in soup.select("a.vacancy-card"):
        title_tag = job.select_one(".vacancy-card__title")
        title = title_tag.get_text(" ", strip=True) if title_tag else ""
        city = extract_city(job)
        if not job.get("href") or not title or not city:
            continue

        job_list.append(Item(
            job_title=title,
            job_link=job["href"],
            company=COMPANY,
            country=COUNTRY,
            county=get_location_county(city),
            city=city,
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
