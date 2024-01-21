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
# Company ---> Azur
# Link ------> https://www.azur.ro/ro/cariere
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
    ... scrape data from Azur scraper.
    '''
    soup = GetStaticSoup("https://www.azur.ro/ro/cariere")

    job_list = []
    for job in soup.find_all("div",attrs={"class":"titlu-sortare22"}):
        
        # get jobs items from response
        job_list.append(Item(
            job_title=job.find('a').text.strip(),
            job_link="https://www.azur.ro" + job.find("a")["href"].strip(),
            company='AZUR',
            country='Romania',
            county=get_county("Timisoara"),
            city='Timisoara',
            remote='on-site',
        ).to_dict())

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "AZUR"
    logo_link = "https://www.azur.ro/images/logo.png"

    jobs = scraper()
    
    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
