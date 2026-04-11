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
from sites.__utils.req_bs4_shorts import GetHtmlSoup, GetStaticSoup
from sites.__utils.items_struct import Item
from sites.__utils.peviitor_update import UpdateAPI
from sites.__utils.found_county import get_county

import json
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


def extract_results(soup):
    matches = re.search(r"window\.FILTER_BAR_INITIAL\s*=\s*(\{[\s\S]*?\});\s*</script>", str(soup))
    if not matches:
        return []

    payload = json.loads(matches.group(1))
    return payload.get("results", [])


def scraper():
    '''
    ... scrape data from Centric scraper.
    '''
    soup = GetStaticSoup(JOBS_URL)

    job_list = []
    for raw_job in extract_results(soup):
        soup_after_regex = GetHtmlSoup(raw_job)

        for job in soup_after_regex("div", attrs={"class": "card default"}):
            link_tag = job.find("a", href=True)
            title = (job.get("data-name") or "").strip()
            city = normalize_city(job.get("data-location", ""))
            if not link_tag or not title or not city:
                continue

            job_list.append(Item(
                job_title=title,
                job_link=link_tag["href"],
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
