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
# Company ---> centric
# Link ------> https://careers.centric.eu/ro/open-positions/
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
    ... scrape data from centric scraper.
    '''
    soup = GetStaticSoup("https://careers.centric.eu/ro/open-positions/")

    job_list = []
    for job in soup.find_all('div', attrs={'class':'card-grid__wrapper'}):
        job_ = job.find('div', attrs={'class':'card  default'})
       
         

        # get jobs items from response
        job_list.append(Item(
            job_title=job_,
            job_link=job.find("a", attrs={"class":'card__anchor'})['href'],
            company='centric',
            country='',
            county='',
            city='',
            remote='',
        ).to_dict())

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "centric"
    logo_link = "logo_link"

    jobs = scraper()
    print(jobs)

    # uncomment if your scraper done
    # UpdateAPI().update_jobs(company_name, jobs)
    # UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
