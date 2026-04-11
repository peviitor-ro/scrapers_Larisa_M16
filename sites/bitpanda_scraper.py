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
# Company ---> bitpanda
# Link ------> https://job-boards.eu.greenhouse.io/bitpanda?offices%5B%5D=4000797101
#
#
#
from sites.__utils.req_bs4_shorts import GetStaticSoup
from sites.__utils.items_struct import Item
from sites.__utils.peviitor_update import UpdateAPI
from sites.__utils.found_county import get_county

import json
import re


JOBS_URL = "https://job-boards.eu.greenhouse.io/bitpanda?offices%5B%5D=4000797101"
COMPANY = "Bitpanda"
COUNTRY = "Romania"
LOGO_LINK = "https://s101-recruiting.cdn.greenhouse.io/external_greenhouse_job_boards/logos/400/029/610/resized/logo_linkedin-1-01.png?1636451495"

CITY_TRANSLATIONS = {
    "bucurești": "Bucuresti",
    "bucharest": "Bucuresti",
}


def normalize_city(city_name):
    city_name = re.sub(r"\s+", " ", city_name).strip(" -–,;:/")
    return CITY_TRANSLATIONS.get(city_name.lower(), city_name)


def extract_job_posts(soup):
    for script_tag in soup.find_all("script"):
        script_text = script_tag.string or script_tag.get_text()
        if not script_text or "window.__remixContext" not in script_text:
            continue

        match = re.search(r"window\.__remixContext\s*=\s*(\{.*\});", script_text, re.DOTALL)
        if not match:
            continue

        remix_context = json.loads(match.group(1))
        return remix_context["state"]["loaderData"]["routes/$url_token"]["jobPosts"]["data"]

    return []


def scraper():
    '''
    ... scrape data from bitpanda scraper.
    '''
    soup = GetStaticSoup(JOBS_URL)

    job_list = []
    for job in extract_job_posts(soup):
        location_parts = [part.strip() for part in job.get("location", "").split(",")]
        if not any(part.lower() == "romania" for part in location_parts):
            continue

        city = normalize_city(location_parts[0])
        if not city:
            continue

        job_list.append(Item(
            job_title=job.get("title", "").strip(),
            job_link=job.get("absolute_url", "").strip(),
            company=COMPANY,
            country=COUNTRY,
            county=get_county(city),
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
