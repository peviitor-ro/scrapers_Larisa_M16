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
# Company ---> Accenture
# Link ------> https://www.accenture.com/api/accenture/elastic/findjobs
#
#
#
from sites.__utils.items_struct import Item
from sites.__utils.peviitor_update import UpdateAPI
from sites.__utils.found_county import get_county

import re

import requests


API_URL = "https://www.accenture.com/api/accenture/elastic/findjobs"
REFERER_URL = "https://www.accenture.com/ro-en/careers/jobsearch?jk=&sb=1&vw=0&is_rj=0&pg=1"
COMPANY = "Accenture"
COUNTRY = "Romania"
LOGO_LINK = "/content/dam/accenture/final/images/icons/symbol/Acc_Logo_Black_Purple_RGB.png"
PAGE_SIZE = 12

CITY_TRANSLATIONS = {
    "bucharest": "Bucuresti",
    "cluj-napoca": "Cluj-Napoca",
    "cluj napoca": "Cluj-Napoca",
    "targu-mures": "Targu Mures",
    "targu mures": "Targu Mures",
    "timisoara": "Timisoara",
}

REMOTE_TRANSLATIONS = {
    "hybrid": "hybrid",
    "remote": "remote",
    "on-site": "on-site",
    "onsite": "on-site",
    "on site": "on-site",
    "on\u002dsite": "on-site",
}

REQUEST_HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json, text/plain, */*",
    "Origin": "https://www.accenture.com",
    "Referer": REFERER_URL,
    "X-Requested-With": "XMLHttpRequest",
}


def normalize_city(city_name):
    city_name = re.sub(r"\s+", " ", city_name).strip(" -–,;:/")
    return CITY_TRANSLATIONS.get(city_name.lower(), city_name)


def normalize_remote(remote_value):
    remote_value = (remote_value or "").strip().lower()
    return REMOTE_TRANSLATIONS.get(remote_value, "on-site")


def extract_locations(location_text):
    if not location_text:
        return []

    if isinstance(location_text, list):
        raw_locations = location_text
    else:
        raw_locations = re.split(r",|/|\|", location_text)

    locations = []

    for raw_location in raw_locations:
        city_name = normalize_city(raw_location)
        if city_name and get_county(city_name) and city_name not in locations:
            locations.append(city_name)

    return locations


def fetch_jobs_page(start_index):
    payload = {
        "startIndex": str(start_index),
        "maxResultSize": str(PAGE_SIZE),
        "jobKeyword": "",
        "jobCountry": COUNTRY,
        "jobLanguage": "en",
        "countrySite": "ro-en",
        "sortBy": "1",
        "searchType": "vectorSearch",
        "enableQueryBoost": "true",
        "minScore": "0.6",
        "getFeedbackJudgmentEnabled": "true",
        "useCleanEmbedding": "true",
        "score": "true",
        "totalHits": "true",
        "debugQuery": "false",
        "jobFilters": "[]",
    }

    response = requests.post(API_URL, headers=REQUEST_HEADERS, files=payload, timeout=30)
    response.raise_for_status()
    return response.json()


def build_item(job_data):
    title = (job_data.get("title") or "").strip()
    job_link = (job_data.get("jobDetailUrl") or "").strip().replace("{0}", "ro-en")
    locations = extract_locations(job_data.get("location", ""))
    if not title or not job_link or not locations:
        return None

    return Item(
        job_title=title,
        job_link=job_link,
        company=COMPANY,
        country=COUNTRY,
        county=[get_county(city_name) for city_name in locations],
        city=locations,
        remote=normalize_remote(job_data.get("remoteType", "")),
    ).to_dict()


def scraper():
    '''
    ... scrape data from Accenture scraper.
    '''
    job_list = []
    start_index = 0
    total_hits = None

    while total_hits is None or start_index < total_hits:
        payload = fetch_jobs_page(start_index)
        total_hits = payload.get("totalHits", {}).get("total", 0)

        for job_data in payload.get("data", []):
            job_item = build_item(job_data)
            if job_item:
                job_list.append(job_item)

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
