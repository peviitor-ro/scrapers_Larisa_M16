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
# Link ------> https://jobs.elektrobit.com/job-offers.html?order%5Bdir%5D=asc&order%5Bfield%5D=stellenbezeichnung&filter[countr][]=Romania+-+Brasov&filter[countr][]=Romania+-+Oradea&filter[countr][]=Romania+-+Timisoara&filter[volltext]=
#
#
from scrapers.__utils import (
    GetStaticSoup,
    get_county,
    get_job_type,
    Item,
    UpdateAPI,
)

locations_ = [
    'Timisoara',
    "Brasov"
]
def scraper():
    '''
    ... scrape data from elektrobit scraper.
    '''
    soup = GetStaticSoup("https://jobs.elektrobit.com/job-offers.html?order%5Bdir%5D=asc&order%5Bfield%5D=stellenbezeichnung&filter[countr][]=Romania+-+Brasov&filter[countr][]=Romania+-+Oradea&filter[countr][]=Romania+-+Timisoara&filter[volltext]=")

    job_list = []
    for job in soup.find_all('td', attrs={'class':'real_table_col1'}):
       
        # get jobs items from response
        job_list.append(Item(
            job_title=job.find('a').text,
            job_link=job.find('a')['href'],
            company='Elektrobit',
            country='Romania',
            county= [get_county(town) for town in locations_],
            city=locations_,
            remote='on site',
        ).to_dict())

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "Elektrobit"
    logo_link = "https://jobs.elektrobit.com/bilder/elektrobitautomotive/symbole/logo1.png"

    jobs = scraper()

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
