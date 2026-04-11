#
#
# Configurare pentru Scraperul Dynamic Render!
# Company ---> corteva
# Link ------> https://apply.corteva.com/careers?keyword=Romania&domain=corteva.com&start=0&location=Romania&pid=893393579943&sort_by=distance&filter_include_remote=1
#
# ------ IMPORTANT! ------
# if you need return soup object:
# you cand import from __utils -> GetHtmlSoup
# if you need return regex object:
# you cand import from __utils ->
# ---> get_data_with_regex(expression: str, object: str)
#
#
#
from sites.__utils.items_struct import Item
from sites.__utils.peviitor_update import UpdateAPI
from sites.__utils.found_county import get_county

import requests
from bs4 import BeautifulSoup


JOBS_URL = "https://apply.corteva.com/careers?keyword=Romania&domain=corteva.com&start=0&location=Romania&pid=893393579943&sort_by=distance&filter_include_remote=1"
SEARCH_API_URL = "https://apply.corteva.com/api/pcsx/search"
COMPANY = "CORTEVA"
COUNTRY = "Romania"
LOGO_LINK = "https://assets.corteva.com/is/image/Corteva/CortevaLegal_HorColor_RGB_no_tagline"
DOMAIN = "corteva.com"
PAGE_SIZE = 10

CITY_TRANSLATIONS = {
    "bucarest": "Bucuresti",
    "bucharest": "Bucuresti",
}

COUNTY_OVERRIDES = {
    "Bucuresti": "Bucuresti",
}


def normalize_city(city_name):
    city_name = city_name.strip()
    return CITY_TRANSLATIONS.get(city_name.lower(), city_name)


def get_location_county(city_name):
    return COUNTY_OVERRIDES.get(city_name, get_county(city_name))


def get_remote_type(job_data):
    remote_value = (job_data.get("workLocationOption") or "").strip().lower()
    if remote_value == "remote":
        return "remote"
    if remote_value == "hybrid":
        return "hybrid"
    return "on-site"


def create_session():
    session = requests.Session()
    response = session.get(JOBS_URL, headers={"User-Agent": "Mozilla/5.0"}, timeout=30)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "lxml")
    csrf_token = soup.find("meta", attrs={"name": "_csrf"})
    if csrf_token:
        session.headers.update({"x-csrf-token": csrf_token["content"]})

    session.headers.update({
        "User-Agent": "Mozilla/5.0",
        "x-requested-with": "XMLHttpRequest",
    })
    return session


def fetch_jobs_page(session, start_index):
    response = session.get(
        SEARCH_API_URL,
        params={
            "domain": DOMAIN,
            "query": "Romania",
            "location": "Romania",
            "start": start_index,
            "sort_by": "distance",
            "filter_include_remote": 1,
        },
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def build_item(job_data):
    standardized_locations = job_data.get("standardizedLocations") or []
    if standardized_locations and isinstance(standardized_locations[0], str):
        city_source = standardized_locations[0].split(",")[0]
    else:
        city_source = job_data.get("locations", [""])[0].split(",")[0]

    city = normalize_city(city_source)
    if not city:
        return None

    return Item(
        job_title=job_data.get("name", "").strip(),
        job_link=(job_data.get("positionUrl", "").strip() and f"https://apply.corteva.com{job_data.get('positionUrl', '').strip()}") or f"https://apply.corteva.com/careers/job/{job_data.get('id')}",
        company=COMPANY,
        country=COUNTRY,
        county=get_location_county(city),
        city=city,
        remote=get_remote_type(job_data),
    ).to_dict()


def scraper():
    '''
    ... scrape data from corteva scraper.
    '''
    session = create_session()

    job_list = []
    start_index = 0

    while True:
        payload = fetch_jobs_page(session, start_index)
        positions = payload.get("data", {}).get("positions", [])
        if not positions:
            break

        for job_data in positions:
            job_item = build_item(job_data)
            if job_item:
                job_list.append(job_item)

        if len(positions) < PAGE_SIZE:
            break

        start_index += PAGE_SIZE

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
