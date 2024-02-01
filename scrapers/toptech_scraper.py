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
# Company ---> toptech
# Link ------> https://www.toptech.ro/cariere.html
#
#
from bs4 import BeautifulSoup
from __utils import (
    GetStaticSoup,
    get_county,
    get_job_type,
    Item,
    UpdateAPI,
)

import requests_html
import requests


def scraper():
    '''
    ... scrape data from toptech scraper.
    '''
    soup = GetStaticSoup("https://www.toptech.ro/cariere.html")
     
    def get_static_soup(url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup

    job_list = []

    for job in soup.find_all('p'):
        strong_tag = job.find('strong')
        
        if strong_tag:
            job_title = strong_tag.text.strip()
            # Exclud non job title
            if not job_title or  'Suntem o echipa unita, formata din oameni valorosi' in job_title or 'Te invitam sa vezi joburile disponibile' in job_title or 'Posturi disponibile' in job_title :
              continue
            
            # daca linkul de job se află în eticheta de ancorare din același paragraf
            job_link_tag = job.find('a', href=True)
            job_link = job_link_tag['href'] if job_link_tag else ''
        
            #  județul, orașul și informațiile de la distanță sunt în paragrafele următoare
            next_paragraphs = job.find_all_next('p')
            county, city, remote ='Timisoara, Cluj Napoca, Alba Iulia', 'Timisoara, Cluj Napoca, Alba Iulia', 'remote'

            for paragraph in next_paragraphs:
                if 'TEHNICIAN' in paragraph.text:   
                    break   
                elif 'County' in paragraph.text:
                    county = paragraph.text.replace('County:', '').strip()
                elif 'City' in paragraph.text:
                    city = paragraph.text.replace('City:', '').strip()
                elif 'Remote' in paragraph.text:
                    remote = paragraph.text.replace('Remote:', '').strip()

         
            job_list.append({
                'job_title': job_title,
                'job_link': 'https://www.toptech.ro/cariere.html',
                'company': 'Toptech',
                'country':'Romania',
                'county': county,
                'city': city,
                'remote': remote,
            })

    return job_list
def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "Toptech"
    logo_link = "https://www.toptech.ro/img/toptech-og-logo-2023.png"

    jobs = scraper()
    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
