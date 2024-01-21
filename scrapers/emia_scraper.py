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
# Company ---> emia
# Link ------> https://emia.com/jobs/
#
#
from scrapers.__utils import (
    GetStaticSoup,
    get_county,
    get_job_type,
    Item,
    UpdateAPI,
)

def scraper():
    '''
    ... scrape data from emia scraper.
    '''
    soup = GetStaticSoup("https://emia.com/jobs/")
     
    job_list = []
    for job in soup.find_all('div', attrs={'class': 'col-lg-4 col-md-6 pt--30'}):
            
        # get jobs items from response
        job_list.append(Item(
            job_title=job.find('h5', attrs={'class':'h5'}).text,
            job_link=job.find('a', attrs={'class':'card-job top-only'})['href'],
            company='Emia',
            country='Romania',
            county="Bucuresti",
            city='Bucuresti',
            remote='on-site',
        ).to_dict())

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "Emia"
    logo_link = "https://emia.com/image/emia-logo.png"

    jobs = scraper()

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
