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
# Company ---> monefy
# Link ------> https://monefy.ro/careers/
#
#
#
from sites.__utils.req_bs4_shorts import GetStaticSoup
from sites.__utils.items_struct import Item
from sites.__utils.peviitor_update import UpdateAPI
from sites.__utils.found_county import get_county

import re


JOBS_URL = "https://monefy.ro/careers/"
COMPANY = "Monefy"
COUNTRY = "Romania"
LOGO_LINK = "https://monefy.ro/wp-content/uploads/2021/02/Logo.png"

CITY_TRANSLATIONS = {
    "bucharest": "Bucuresti",
    "brașov": "Brasov",
    "brasov": "Brasov",
}

COUNTY_OVERRIDES = {
    "Bucuresti": "Bucuresti",
    "Brasov": "Brasov",
}


def normalize_city(city_name):
    city_name = re.sub(r"\s+", " ", city_name).strip(" -–,;:/")
    return CITY_TRANSLATIONS.get(city_name.lower(), city_name)


def get_location_county(city_name):
    return COUNTY_OVERRIDES.get(city_name, get_county(city_name))


def extract_location_and_remote(response):
    page_text = response.get_text(" | ", strip=True)
    match = re.search(r"Location\s*\|?\s*:?\s*\|?\s*([^|]+)", page_text, re.IGNORECASE)
    if not match:
        return "Bucuresti", "on-site"

    location_text = match.group(1).strip()
    location_lower = location_text.lower()
    if "remote" in location_lower:
        return "Bucuresti", "remote"

    remote_type = "on-site"
    if "on-site" in location_lower:
        remote_type = "on-site"
        location_text = location_text.replace("On-site", "").replace("on-site", "")

    if "," in location_text:
        location_parts = [part.strip() for part in location_text.split(",") if part.strip()]
        location_text = next((part for part in location_parts if "site" not in part.lower()), location_parts[0])

    city = normalize_city(location_text)
    return city or "Bucuresti", remote_type


def scraper():
    '''
    ... scrape data from monefy scraper.
    '''
    soup = GetStaticSoup(JOBS_URL)

    job_list = []
    for job in soup.select('div.et_pb_ajax_pagination_container article.et_pb_post'):
        link_tag = job.find('a', href=True)
        if not link_tag:
            continue

        response = GetStaticSoup(link_tag['href'])
        city, remote_type = extract_location_and_remote(response)

        job_list.append(Item(
            job_title=link_tag.get_text(strip=True),
            job_link=link_tag['href'],
            company=COMPANY,
            country=COUNTRY,
            county=get_location_county(city),
            city=city,
            remote=remote_type,
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
