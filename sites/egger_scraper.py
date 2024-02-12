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
# Company ---> Egger
# Link ------> https://careers.egger.com/go/Jobs-in-Romania/8984955/
#
#
#
from sites.__utils.req_bs4_shorts import GetStaticSoup
from sites.__utils.items_struct import Item
from sites.__utils.peviitor_update import UpdateAPI

from urllib.parse import unquote

def scraper():
    '''
    ... scrape data from Egger scraper.
    '''
    soup = GetStaticSoup("https://careers.egger.com/go/Jobs-in-Romania/8984955/")

    job_list = []
    for job in soup.find_all('tr', attrs={'class':'data-row'}):
 
        # get jobs items from response
        job_list.append(Item(
            job_title=unquote(job.find('a')['href'].strip().split('/')[2].replace('-', ' ')),
            job_link='https://careers.egger.com' + job.find('a')['href'].strip(),
            company='Egger',
            country='Romania',
            county='Radauti',
            city='Radauti',
            remote='onsite',
        ).to_dict())

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "Egger"
    logo_link = "https://rmkcdn.successfactors.com/24f99312/dac140b7-bf0d-474e-b2c7-7.jpg"

    jobs = scraper()
 
    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
