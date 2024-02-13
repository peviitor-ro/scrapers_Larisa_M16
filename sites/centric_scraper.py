#
#
#  Basic for scraping data from static pages
# ------ IMPORTANT! ------
# if you need return soup object:
# you cand import from sites.__utils -> GetHtmlSoup
# if you need return regex object:
# you cand import from sites.__utils ->
# ---> get_data_with_regex(expression: str, object: str)
#
# Company ---> centric
# Link ------> https://careers.centric.eu/ro/open-positions/
#
#
#
from sites.__utils.req_bs4_shorts import GetHtmlSoup, GetStaticSoup
from sites.__utils.peviitor_update import UpdateAPI
#

import re
import json
 
def scraper():
    '''
    ... scrape data from test scraper.
    '''
    soup = GetStaticSoup("https://careers.centric.eu/ro/open-positions/")

    job_list = []
    matches = re.search(r"window\.FILTER_BAR_INITIAL = ({[\s\S]*?});\s*<\/script>", str(soup))
 
    if matches:
        json_content = matches.group(1)
        filter_bar_initial = json.loads(json_content)
         

        for data_rex in filter_bar_initial['results']:
            soup_after_regex = GetHtmlSoup(data_rex)

            # scrape data from regex
            for job in soup_after_regex('div', attrs={'class': 'card default'}):
                link = job.find('a')['href']
                title = job.find('div', attrs={'class': 'card__title'}).text
                location = job['data-location']

                # Append job details to the list
                job_list.append({
                    'job_title':title,
                    'job_link':link,
                    'company': 'Centric',
                    'country': 'Romania',   
                    'county': location,    
                    'city': location,
                    'remote': ('onsites','remote'),   
                })
    return job_list            

def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "Centric"
    logo_link = "https://careers.centric.eu/static/images/logo.svg"

    jobs = scraper()
   
    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
