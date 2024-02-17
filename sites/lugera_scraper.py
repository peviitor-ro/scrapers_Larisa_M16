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


def scraper():
    '''
    ... scrape data from Lugera scraper.
    '''
    job_list = []
    page = 1

    while page <= 6:
        url = f"https://www.lugera.ro/jobex/public/ro?txt=+&country=Romania&cities%5B%5D=&page={page}"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        for job in soup.find_all("div", attrs={'class': 'job col-xs-12 m-grid m-grid-responsive-sm'}):
            job_t = job.find('a', class_='job-title-link').text
            location = job.find('div', attrs={'class': 'job-location m-grid-col m-grid-col-middle m-grid-col-left m-grid-col-md-2 m-grid-col-sm-12'}).text.strip().split('\n')[0]
            if location == 'Fully remote':
                location = ""
            if location == 'Fully remote':
                location = ""
            if location == 'Cluj-Napoca':
                location = "Cluj"
            if location == 'Ploiesti':
                location = "Prahova"
            if location == 'Timisoara':
                location = "Timis"
            if location == 'Caracal':
                location = "Olt"

            city = job.find('div', attrs={'class': 'job-location m-grid-col m-grid-col-middle m-grid-col-left m-grid-col-md-2 m-grid-col-sm-12'}).text.strip().split('\n')[0]
            if city == 'Fully remote':
                city = ""
            remote_status = job.find('div', attrs={'class': 'job-location m-grid-col m-grid-col-middle m-grid-col-left m-grid-col-md-2 m-grid-col-sm-12'}).text.strip().split('\n')[0]
            remote_status = 'Hybrid' if 'Hybrid' in remote_status else 'Fully remote' if 'Fully remote' in remote_status else 'remote' if 'remote' in remote_status else 'onsite'
            
            job_list.append(Item(
                job_title=job_t,
                job_link="https://www.lugera.ro" + job.find('a', class_='job-title-link')['href'],
                company='Lugera',
                country='Romania',
                county=location,
                city=city,
                remote=remote_status,
            ).to_dict())
        
        page += 1

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