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
# Company ---> Lugera
# Link ------> https://www.lugera.ro/jobex/public/ro?txt=+&country=Romania&cities%5B%5D=
#
#
from bs4 import BeautifulSoup
import requests
from sites.__utils.req_bs4_shorts import GetXMLObject, GetStaticSoup
from sites.__utils.items_struct import Item
from sites.__utils.peviitor_update import UpdateAPI
from sites.__utils.found_county import get_county
from sites.__utils.get_job_type import get_job_type


def extract_jobs_num():
    '''
    ... extract jobs num'''

    return int(GetStaticSoup('https://www.lugera.ro/jobex/public/ro?txt=%20&country=Romania&cities%5B0%5D=&page=1').select_one('h1.jobsHomeTitle').text.strip().split('(')[-1].split('-')[0].strip())
def scraper():
    '''
    ... scrape data from Lugera scraper.
    '''

    job_list = []
    for page in range(1, (extract_jobs_num()) // 20 + 2):
        soup = GetStaticSoup(f"https://www.lugera.ro/jobex/public/ro?txt=%20&country=Romania&cities%5B0%5D=&page={str(page)}")

        if len(soup_data := soup.select_one('div.jobs-listing.jobs.jobex-search-results.row').select('div.job.col-xs-12.m-grid.m-grid-responsive-sm')) > 0:

            new_location = None
            job_type = None
            for data_job in soup_data:
                location = data_job.select_one('div.job-location').text.strip().split('\n')[0] 
                link = 'https://www.lugera.ro' + data_job.select_one('a.job-title-link')['href']
                job_t = data_job.select_one('a.job-title-link').text
                
                if 'bucuresti' in location.lower():
                    new_location = 'Bucuresti'
                elif 'fully remote' == location.lower():
                    new_location = ''
                    job_type = 'remote'
                elif 'hybrid' == location.lower():
                    new_location = ''
                    job_type = 'hybrid'
                else:
                    new_location = location
                    job_type = 'on-site'

                
                # get jobs items from response
                job_list.append(Item(
                    job_title=job_t,
                    job_link=link,
                    company='Lugera',
                    country='Romania',
                    county='' if location == None else get_county(new_location),
                    city=new_location,
                    remote=job_type,
                ).to_dict())

    return job_list
            
        
def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "Lugera"
    logo_link = "https://www.lugera.ro/jobex/public/theme/images/logo-lugera-color-small.png"

    jobs = scraper()
    
   
    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()