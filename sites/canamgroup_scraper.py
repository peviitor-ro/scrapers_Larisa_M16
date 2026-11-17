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
# Company ---> canamgroup
# Link ------>  https://www.canam.com/en/job-opportunities/?country%5B%5D=romania&search=
#
#
#
from sites.__utils.req_bs4_shorts import GetStaticSoup
from sites.__utils.items_struct import Item
from sites.__utils.peviitor_update import UpdateAPI
from sites.__utils.found_county import get_county
from sites.__utils.get_job_type import get_job_type


JOBS_URL = "https://www.canam.com/en/job-opportunities/?country%5B%5D=romania&search="
COMPANY = "CanamGroup"
COUNTRY = "Romania"
CITY = "Brasov"
LOGO_LINK = "https://www.canam.com/wp-content/themes/canam/dist/img/logo-canam.png"


def scraper():
    '''
    ... scrape data from canamgroup scraper.
    '''
    soup = GetStaticSoup(JOBS_URL)

    job_list = []
    for job in soup.find_all('a', class_='c-card-job'):
        title_tag = job.select_one('.c-card-job__title span')
        location_tag = job.select_one('.c-btn--tag')
        if not title_tag or not location_tag:
            continue

        job_title = title_tag.get_text(strip=True)
        location = location_tag.get_text(strip=True)

        job_list.append(Item(
            job_title=job_title,
            job_link=job.get('href'),
            company=COMPANY,
            country=COUNTRY,
            county=get_county(location),
            city=CITY,
            remote=get_job_type(location),
        ).to_dict())

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    jobs = scraper()

    UpdateAPI().update_jobs(COMPANY, jobs)
    UpdateAPI().update_logo(COMPANY, LOGO_LINK)


if __name__ == '__main__':
    main()
