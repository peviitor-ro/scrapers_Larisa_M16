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
# Company ---> elektrobit
# Link ------> https://jobs.elektrobit.com/api/jobs
#
#
#
from sites.__utils.req_bs4_shorts import GetRequestJson
from sites.__utils.items_struct import Item
from sites.__utils.peviitor_update import UpdateAPI
from sites.__utils.found_county import get_county


COMPANY = "Elektrobit"
LOGO_LINK = "https://jobs.elektrobit.com/bilder/elektrobitautomotive/symbole/logo1.png"
API_URL = "https://jobs.elektrobit.com/api/jobs"
PAGE_SIZE = 100


def get_jobs():
    '''
    ... fetch every job from the elektrobit api, page by page,
    so no Romania job can be missed because of the api filters.
    '''
    jobs = []
    offset = 0
    while True:
        json_data = GetRequestJson(f"{API_URL}?limit={PAGE_SIZE}&offset={offset}") or {}
        page_jobs = json_data.get('jobs', [])
        jobs.extend(page_jobs)

        total = json_data.get('totalCount')
        offset += PAGE_SIZE
        if not page_jobs or not isinstance(total, int) or len(jobs) >= total:
            break

    return jobs


def scraper():
    '''
    ... scrape data from elektrobit scraper.
    '''
    job_list = []
    for job in get_jobs():
        data = job['data']

        # get Romania cities from primary and additional locations
        cities = []
        if data.get('country') == 'Romania' and data.get('city'):
            cities.append(data['city'])
        for location in data.get('additional_locations') or []:
            if location.get('country') == 'Romania' and location.get('city'):
                cities.append(location['city'])
        if not cities:
            continue
        cities = list(dict.fromkeys(cities))

        job_list.append(Item(
            job_title=data['title'],
            job_link=data['apply_url'],
            company=COMPANY,
            country='Romania',
            county=[get_county(town) for town in cities],
            city=cities,
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
