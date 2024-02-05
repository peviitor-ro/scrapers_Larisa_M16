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
# Company ---> Genos
# Link ------> https://www.genosdanmark.eu/vacancies
#
#
from __utils import (
    GetStaticSoup,
    get_county,
    get_job_type,
    Item,
    UpdateAPI,
)

def scraper():
    '''
    ... scrape data from Genos scraper.
    '''
    soup = GetStaticSoup("https://www.genosdanmark.eu/vacancies")
     
    job_list = []
    for job in soup.find_all('div', attrs={'class':'product-item'}):
    
        # get jobs items from response
        job_list.append(Item(
            job_title=job.find("h4", attrs={'class', 'product-item__title'}).text.strip(),
            job_link='https://www.genosdanmark.eu'+ job.find('a')['href'] ,
            company='Genos',
            country='Romania',
            county='Bucuresti',
            city='Bucuresti',
            remote='remote',
        ).to_dict())

    return job_list
 
def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''
    company_name = "Genos"
    logo_link = "https://www.genosdanmark.eu/uploads/images/logo-dark_27_12.png"

    jobs = scraper()
    
    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
