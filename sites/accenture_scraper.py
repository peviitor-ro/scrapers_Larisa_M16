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
# Company ---> Accenture
# Link ------> https://www.accenture.com/ro-en/jobpostings-sitemap.xml
#
#
import sys
import os
directory = os.path.abspath(".\\")
sys.path.append(directory)

from sites.__utils import (
    GetStaticSoup,
    get_county,
    get_job_type,
    Item,
    UpdateAPI,
)

# single, because it used once
from __utils import GetXMLObject
import time
from random import randint

def scraper():
    '''
    ... scrape data from Accenture scraper.
    '''
    soup = GetXMLObject("https://www.accenture.com/ro-en/jobpostings-sitemap.xml")
    job_list = []
    count = 0
    for url_element in soup.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}url'):
        loc_element = url_element.find('{http://www.sitemaps.org/schemas/sitemap/0.9}loc')

        if loc_element is not None and loc_element.text:
            try:
                extract_data = GetStaticSoup(loc_element.text.strip())
            except:
                continue

            # find single and multiply locations...
            location_final = list()
            city_to_translate = ['bucharest']
            #
            location = extract_data.find('div', attrs={'class': 'cmp-job-listing-hero__labels-container'}).find('span', attrs={'class': 'cmp-text__label-small'})
            if location.text.lower() in ['multiple locations', 'multiple location']:
                data_loc_strip = extract_data.find('div', attrs={'class': 'cmp-job-listing-details__location-description'}).text.strip().split(',')
                
                new_lst_cities = list()
                cluj_c = ['cluj napoca']
                
                for dd_city in data_loc_strip:
                    if dd_city.lower().strip() in city_to_translate:
                        dd_city = 'Bucuresti'
                    elif dd_city.lower().strip() in cluj_c:
                        dd_city = 'Cluj-Napoca'
                    new_lst_cities.append(dd_city)
                location_final.extend([x.strip() for x in new_lst_cities])
            else:
                if location:
                    if location.text.lower() in city_to_translate:
                        new_loc = "Bucuresti"
                        location_final.append(new_loc)
                else:
                    location_final.append(location.text.strip())

            # ---> Title
            title_site = extract_data.find('h1')
            if title_site:
                title_final = title_site.text.strip()
            else: 
                continue

            job_list.append(Item(
                job_title=title_final,
                job_link=loc_element.text.strip(),
                company='Accenture',
                country='Romania',
                county=[get_county(town) for town in location_final],
                city=location_final, 
                remote='remote',
            ).to_dict())
            time.sleep(randint(1,3))

            count += 1
            if count >= 10:
                break
    return job_list
         


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "Accenture"
    logo_link = "/content/dam/accenture/final/images/icons/symbol/Acc_Logo_Black_Purple_RGB.png"

    jobs = scraper()
  
    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
