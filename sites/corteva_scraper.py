#
#
# Configurare pentru Scraperul Dynamic Render!
# Company ---> corteva
# Link ------> https://careers.corteva.com/job-search-results/?keyword=Romania
#
# ------ IMPORTANT! ------
# if you need return soup object:
# you cand import from __utils -> GetHtmlSoup
# if you need return regex object:
# you cand import from __utils ->
# ---> get_data_with_regex(expression: str, object: str)
#
#
from __utils import (
    GetDynamicSoup,
    get_county,
    get_job_type,
    Item,
    UpdateAPI,
)

def scraper():
    '''
    ... scrape data from corteva scraper.
    '''
    soup = GetDynamicSoup("https://careers.corteva.com/job-search-results/?keyword=Romania")

    job_list = []
    for job in soup.find_all('div', attrs={'class','job-innerwrap g-cols'}):
        location = job.find('div', attrs={'class',"parent location"}).text.split(',')[1]
      
        # get jobs items from response
        job_list.append(Item(
            job_title=job.find('a').text,
            job_link='https://careers.corteva.com/' + job.find('a')['href'],
            company='CORTEVA',
            country='Romania',
            county=location,
            city=location,
            remote='remote',
        ).to_dict())

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "CORTEVA"
    logo_link = "https://cdn-static.findly.com/wp-content/uploads/sites/2491/2023/02/02100420/logo.svg"

    jobs = scraper()
    print(jobs)
  
    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
