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
from urllib.parse import urljoin


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
    chips = [chip.get_text(" ", strip=True) for chip in response.select(".tagchip")]
    location_text = next(
        (chip for chip in chips if re.search(r"romania|remote|on-site|hybrid", chip, re.IGNORECASE)),
        "",
    )
    location_lower = location_text.lower()
    if "remote" in location_lower:
        return "Bucuresti", "remote"

    remote_type = "hybrid" if "hybrid" in location_lower else "on-site"
    location_text = re.sub(r"\([^)]*\)", "", location_text)
    city = normalize_city(location_text.split(",")[0])
    return city or "Bucuresti", remote_type


def scraper():
    '''
    ... scrape data from monefy scraper.
    '''
    soup = GetStaticSoup(JOBS_URL)

    job_list = []
    for job in soup.select('a.job-card[href]'):
        title_tag = job.find('h3')
        if not title_tag:
            continue

        job_link = urljoin(JOBS_URL, job['href'])
        response = GetStaticSoup(job_link)
        city, remote_type = extract_location_and_remote(response)

        job_list.append(Item(
            job_title=title_tag.get_text(strip=True),
            job_link=job_link,
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
