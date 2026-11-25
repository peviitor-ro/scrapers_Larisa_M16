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
# Company ---> Fieldcore
# Link ------> https://www.fieldcore.com/careers/jobs/?p=search&r=&l=Remote+-+Romania+%28LR18%29&c=&q=&nl=1
#
#
#
from urllib.parse import urljoin

from sites.__utils.req_bs4_shorts import GetStaticSoup
from sites.__utils.items_struct import Item
from sites.__utils.peviitor_update import UpdateAPI


JOBS_URL = "https://jobs.jobvite.com/fieldcore/search?nl=1"
RO_JOBS_URL = "https://jobs.jobvite.com/fieldcore/search?nl=1&nl=1&r=&l=Remote%20-%20Romania%20(LR18)&c=&q=&fr=true"
COMPANY = "Fieldcore"
LOGO_LINK = "https://www.fieldcore.com/wp-content/uploads/2022/09/logo-new.png"


def get_jobs(url):
    soup = GetStaticSoup(url)

    job_list = []
    for job in soup.find_all('td', attrs={'class': 'jv-job-list-name'}):
        link = job.find('a', href=True)
        title = job.find('div', class_='title')
        location = job.find('div', class_='jv-job-list-location')
        if not link or not title or not location:
            continue

        location_parts = [part.strip().rstrip(',') for part in
                          location.get_text('\n', strip=True).splitlines() if part.strip()]
        country = location_parts[-1] if location_parts else 'Romania'
        remote = 'Remote' if any('remote' in part.lower() for part in location_parts) else 'on-site'

        job_list.append(Item(
            job_title=title.get_text(' ', strip=True),
            job_link=urljoin(JOBS_URL, link['href']),
            company=COMPANY,
            country=country,
            county='',
            city='',
            remote=remote,
        ).to_dict())

    return job_list


def scraper():
    '''
    ... scrape data from Fieldcore scraper.
    '''
    return get_jobs(RO_JOBS_URL) or get_jobs(JOBS_URL)


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
