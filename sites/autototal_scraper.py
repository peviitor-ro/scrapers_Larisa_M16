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
# Company ---> autototal
# Link ------> https://www.autototal.ro/cariere
#
#
#
from sites.__utils.req_bs4_shorts import GetStaticSoup
from sites.__utils.items_struct import Item
from sites.__utils.peviitor_update import UpdateAPI
from sites.__utils.found_county import get_county

from datetime import date
import re


JOBS_URL = "https://www.autototal.ro/cariere/"
COMPANY = "AUTOTOTAL"
COUNTRY = "Romania"
LOGO_LINK = "https://www.autototal.ro/wp-content/uploads/thegem-logos/logo_f7149358a9d89410af13364be85f4883_1x.png"

AUTOTOTAL_MONTHS = {
    'ian.': 1,
    'ianuarie': 1,
    'febr.': 2,
    'februarie': 2,
    'mart.': 3,
    'martie': 3,
    'apr.': 4,
    'aprilie': 4,
    'mai': 5,
    'iun.': 6,
    'iunie': 6,
    'iul.': 7,
    'iulie': 7,
    'aug.': 8,
    'august.': 8,
    'august': 8,
    'sept.': 9,
    'septembrie': 9,
    'oct.': 10,
    'octombrie': 10,
    'nov.': 11,
    'noiembrie': 11,
    'dec.': 12,
    'decembrie': 12,
}

CITY_TRANSLATIONS = {
    'bucuresti': 'Bucuresti',
    'bucurești': 'Bucuresti',
    'cluj': 'Cluj-Napoca',
    'cluj-napoca': 'Cluj-Napoca',
    'iași': 'Iasi',
    'iasi': 'Iasi',
    'măgurele': 'Magurele',
    'magurele': 'Magurele',
    'mogoșoaia': 'Mogosoaia',
    'mogosoaia': 'Mogosoaia',
    'lugoj': 'Lugoj',
    'oradea': 'Oradea',
    'sibiu': 'Sibiu',
    'alba iulia': 'Alba Iulia',
    'baia mare': 'Baia Mare',
    'deva': 'Deva',
    'prahova': 'Prahova',
    'bistrita': 'Bistrita',
    'vaslui': 'Vaslui',
}

COUNTY_OVERRIDES = {
    'Iasi': 'Iasi',
    'Magurele': 'Ilfov',
    'Mogosoaia': 'Ilfov',
    'Bucuresti': 'Bucuresti',
    'Cluj-Napoca': 'Cluj',
    'Lugoj': 'Timis',
}


def is_active_job(summary_text):
    match = re.search(r'Expiră\s+(\d{1,2})\s+([A-Za-zăâîșț\.]+)\s+(\d{4})', summary_text, re.IGNORECASE)
    if not match:
        return True

    day_value = int(match.group(1))
    month_value = AUTOTOTAL_MONTHS.get(match.group(2).lower())
    year_value = int(match.group(3))
    if not month_value:
        return True

    return date(year_value, month_value, day_value) >= date.today()


def normalize_city(city_name):
    city_name = re.sub(r'\s*\([^)]*\)', '', city_name)
    city_name = re.sub(r'\s+', ' ', city_name).strip(' -–,;:/')
    return CITY_TRANSLATIONS.get(city_name.lower(), city_name)


def get_location_county(city_name):
    return COUNTY_OVERRIDES.get(city_name, get_county(city_name))


def extract_locations_from_text(text):
    if not text:
        return []

    text = re.sub(r'Oraș de lucru\s*:\s*', '', text, flags=re.IGNORECASE)
    text = re.sub(r'Oras de lucru\s*:\s*', '', text, flags=re.IGNORECASE)
    text = re.split(r'Nivel carier[ăa]\s*:', text, maxsplit=1, flags=re.IGNORECASE)[0]
    text = re.split(r'Expiră\s+\d', text, maxsplit=1, flags=re.IGNORECASE)[0]
    text = text.replace(' si ', ', ')
    text = text.replace('/', ',')

    locations = []
    for raw_location in text.split(','):
        raw_location = raw_location.strip()
        if not raw_location:
            continue

        raw_location = re.split(r'\s+[–-]\s+', raw_location, maxsplit=1)[0].strip()
        city_name = normalize_city(raw_location)
        if city_name and get_location_county(city_name) and city_name not in locations:
            locations.append(city_name)

    return locations


def extract_title_locations(job_title):
    match = re.search(r'[–-]\s*([A-Za-zĂÂÎȘȚăâîșț\-/ ]+)$', job_title)
    if not match:
        return []

    return extract_locations_from_text(match.group(1))


def extract_detail_locations(job_link):
    soup = GetStaticSoup(job_link)

    for paragraph in soup.find_all('p'):
        paragraph_text = paragraph.get_text(' ', strip=True)
        if 'Oraș de lucru:' in paragraph_text or 'Oras de lucru:' in paragraph_text:
            return extract_locations_from_text(paragraph_text)

    return []


def get_job_locations(job, job_link, job_title):
    summary_tag = job.find('div', attrs={'class': 'summary text-body-tiny'})
    summary_text = summary_tag.get_text(' ', strip=True) if summary_tag else ''

    locations = []
    for source_locations in [
        extract_locations_from_text(summary_text),
        extract_detail_locations(job_link),
        extract_title_locations(job_title),
    ]:
        for city_name in source_locations:
            if city_name not in locations:
                locations.append(city_name)

    return locations

def scraper():
    '''
    ... scrape data from Autototal scraper.
    '''
    soup = GetStaticSoup(JOBS_URL)

    job_list = []
    for job in soup.find_all('div', attrs={'class': 'gem-compact-tiny-right'}):

        job_link_tag = job.find('a', href=True)
        summary_tag = job.find('div', attrs={'class': 'summary text-body-tiny'})
        if not job_link_tag or not summary_tag:
            continue

        job_title = job_link_tag.get_text(strip=True)
        job_link = job_link_tag['href']
        summary_text = summary_tag.get_text(' ', strip=True)

        if not is_active_job(summary_text):
            continue

        locations = get_job_locations(job, job_link, job_title)
        if not locations:
            continue

        job_list.append(Item(
            job_title=job_title,
            job_link=job_link,
            company=COMPANY,
            country=COUNTRY,
            county=[get_location_county(city_name) for city_name in locations],
            city=locations,
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
