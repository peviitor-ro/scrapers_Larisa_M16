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
# Company ---> agilefreaks
# Link ------>  https://careers.agilefreaks.com/jobs
#
#

from sites.__utils.req_bs4_shorts import GetStaticSoup
from sites.__utils.items_struct import Item
from sites.__utils.peviitor_update import UpdateAPI
from sites.__utils.found_county import get_county


JOBS_URL = "https://careers.agilefreaks.com/jobs"
COMPANY = "AgileFreaks"
COUNTRY = "Romania"
LOGO_LINK = "https://images.teamtailor-cdn.com/images/s3/teamtailor-production/logotype-v3/image_uploads/3866dbb1-2690-4a4a-8c59-951548beda43/original.png"


def normalize_remote_type(remote_value):
    remote_value = remote_value.lower()
    if "remote" in remote_value:
        return "remote"
    if "hybrid" in remote_value:
        return "hybrid"
    return "on-site"


def parse_job_meta(job):
    meta_values = [
        span.get_text(" ", strip=True)
        for span in job.select("div.mt-1.text-md span")
    ]
    meta_values = [value for value in meta_values if value and value != "·"]

    city = next((value for value in meta_values if get_county(value)), "")
    remote_value = next(
        (value for value in meta_values if "remote" in value.lower() or "hybrid" in value.lower()),
        "on-site",
    )

    return city, normalize_remote_type(remote_value)

def scraper():
    '''
    ... scrape data from agilefreaks scraper.
    '''
    soup = GetStaticSoup(JOBS_URL)

    job_list = []

    for job in soup.select("ul#jobs_list_container > li"):
        title_tag = job.find("a", href=True)
        if not title_tag:
            continue

        city, remote_type = parse_job_meta(job)
        if not city:
            continue

        job_list.append(Item(
            job_title=title_tag.get_text(strip=True),
            job_link=title_tag["href"],
            company=COMPANY,
            country=COUNTRY,
            county=get_county(city),
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
