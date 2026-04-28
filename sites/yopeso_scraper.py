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
# Company ---> yopeso
# Link ------> https://www.yopeso.com/careers-and-culture
#
#

import re
import requests
from bs4 import BeautifulSoup
from sites.__utils.items_struct import Item
from sites.__utils.peviitor_update import UpdateAPI
from sites.__utils.found_county import get_county
from sites.__utils.get_job_type import get_job_type


def get_job_details(job_link):
    '''
    ... get job locations and job type from job page
    '''
    try:
        r = requests.get(job_link, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
        soup = BeautifulSoup(r.text, 'lxml')
        
        # Get locations - format "City | Country"
        location_elems = soup.find_all('h4', class_='location-title')
        locations = []
        for loc in location_elems:
            text = loc.get_text(strip=True)
            # Parse "City | Country" format
            match = re.match(r'(.+?)\s*\|\s*([A-Z]{2})', text)
            if match:
                city = match.group(1).strip()
                country_code = match.group(2).strip()
                locations.append((city, country_code))
        
        return locations
    except:
        return []


def scraper():
    '''
    ... scrape data from yopeso scraper.
    '''
    response = requests.get('https://www.yopeso.com/careers-and-culture', headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(response.text, 'lxml')

    job_list = []
    
    # Find all job items
    job_items = soup.find_all('div', class_='w-dyn-item')
    
    for item in job_items:
        # Get job link
        link_elem = item.find('a', href=True)
        if not link_elem:
            continue
        
        job_link = 'https://www.yopeso.com' + link_elem['href']
        
        # Get job title
        title_elem = item.find('div', class_='open-psoitions-job-title')
        if not title_elem:
            continue
        
        job_title = title_elem.get_text(strip=True)
        
        # Get locations from job page
        locations = get_job_details(job_link)
        
        # Filter for Romania locations only
        for city, country_code in locations:
            if country_code == 'RO':
                # Determine job type based on title or default to on-site
                job_type_ = 'on-site'
                if 'remote' in job_title.lower():
                    job_type_ = 'remote'
                elif 'hybrid' in job_title.lower():
                    job_type_ = 'hybrid'
                
                job_list.append(Item(
                    job_title=job_title,
                    job_link=job_link,
                    company='Yopeso',
                    country='Romania',
                    county=get_county(city),
                    city=city.replace('Cluj Napoca', 'Cluj-Napoca'),
                    remote=get_job_type(job_type_),
                ).to_dict())
    
    return job_list




def main():
    '''
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "Yopeso"
    logo_link = "https://www.yopeso.com/wp-content/uploads/2022/05/logo-Yopeso-150x78.png"

    jobs = scraper()
    
    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
