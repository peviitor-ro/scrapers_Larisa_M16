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
# Company ---> bitpanda
# Link ------> https://boards.eu.greenhouse.io/bitpanda
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
    ... scrape data from bitpanda scraper.
    '''
    soup = GetStaticSoup("https://boards.eu.greenhouse.io/bitpanda")

    job_list = []
    for job in soup.find_all("div",attrs={"class":"opening"}):
        location =  job.find('span', attrs={"class":'location'}).text.split(',')
        if "romania" in [x.lower().strip() for x in location]:

            # get jobs items from response
            job_list.append(Item(
                job_title=job.find('a').text,
                job_link='https://boards.eu.greenhouse.io' + job.find('a')['href'],
                company='Bitpanda',
                country='Romania',
                county=get_county(location[0]),
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

    company_name = "Bitpanda"
    logo_link = "https://s101-recruiting.cdn.greenhouse.io/external_greenhouse_job_boards/logos/400/029/610/resized/logo_linkedin-1-01.png?1636451495"

    jobs = scraper()
   

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
