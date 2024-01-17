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
# Company ---> cgsromania
# Link ------> https://romania.cgsinc.com/vino-in-echipa-cgs/
#
#
from sites.__utils import (
    GetStaticSoup,
    get_county,
    get_job_type,
    Item,
    UpdateAPI,
    HackCloudFlare,
)
 
import cfscrape
from bs4 import BeautifulSoup
from sites.__utils import DEFAULT_HEADERS
from sites.__utils.req_bs4_shorts import HackCloudFlare

data = HackCloudFlare('https://romania.cgsinc.com/vino-in-echipa-cgs/') 
 
def has_hungarian_letters(text):
    # Check if the text contains Hungarian letters
    hungarian_letters = ['ő', 'ü', 'é', 'á']
    return any(letter in text.lower() for letter in hungarian_letters)
def remove_hungarian_letters(text):
    # Remove Hungarian letters from the text
    for letter in has_hungarian_letters:
        text = text.replace(letter, 'ő', 'ü', 'é', 'á')
    return text

sensors_letters = ['ő', 'ü', 'é', 'á']
def scraper():
     data= HackCloudFlare("https://romania.cgsinc.com/vino-in-echipa-cgs/")
     
     
     job_list = []
     for job in data.select('article[class*="elementor-post"]'):
        link = job.find('a')['href']
        title_loc = job.find('div', attrs={'class': 'job-item'}).text.strip('-')
        if len(title_loc) > 1:
                    if  any(s_l in title_loc[0].lower() for s_l in sensors_letters):
                         continue

        else:
            title = title_loc[0].strip()
            if title.startswith('Client'):
              title = title.replace('Client', 'Client Relații Clienți')
            if title.endswith('(Remote)'):
                title = title.replace('(Remote)', '')
            if title.endswith('Ügyfélszolgálati állásajánlat '):
                title = title.replace('Ügyfélszolgálati állásajánlat ', 'Oferta de munca serviciu clienti')
            job_list.append(title)
 
        for title in job_list:
             print(title)
            
        _ = job.find('p', attrs={'class','fw-r text-white p'}).text


        job_list.append(Item(
            job_title=title_loc,
            job_link=job.find('a')['href'],
            company='CGSRomania',
            country='România',
            county='',
            city='',
            remote=''
        ).to_dict())
     return job_list
     

def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "CGSRomania"
    logo_link = "https://romania.cgsinc.com/wp-content/uploads/2021/05/logo_CGS.svg"

    jobs = scraper()
    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()