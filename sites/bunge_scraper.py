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
# Company ---> bunge
# Link ------>  https://jobs.bunge.com/search/?createNewAlert=false&q=&locationsearch=Romania&optionsFacetsDD_country=
#
#
#
import time
import urllib3
import requests
from sites.__utils.req_bs4_shorts import GetHtmlSoup, session
from sites.__utils.default_headers import DEFAULT_HEADERS
from sites.__utils.items_struct import Item
from sites.__utils.peviitor_update import UpdateAPI
from sites.__utils.found_county import get_county

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

COMPANY = "Bunge"
SEARCH_URL = "https://jobs.bunge.com/search/?createNewAlert=false&q=&locationsearch=Romania&optionsFacetsDD_country="
LOGO_LINK = "https://rmkcdn.successfactors.com/c8d09bed/298fb332-da77-4747-9f6b-9.svg"


def get_jobs_soup():
    '''
    ... The careers site sporadically answers with a 504 page; retry before
        accepting an empty result.
    '''
    soup = GetHtmlSoup("")
    for _ in range(5):
        try:
            response = session.get(
                SEARCH_URL,
                headers=DEFAULT_HEADERS.copy(),
                verify=False,
                timeout=15,
            )
            if response.status_code == 200:
                soup = GetHtmlSoup(response.content)
                if soup.find_all("tr", attrs={"class": "data-row"}):
                    return soup
        except requests.RequestException:
            pass
        time.sleep(1)

    return soup


def scraper():
    '''
    ... scrape data from bunge scraper.
    '''
    soup = get_jobs_soup()

    job_list = []
    for job in soup.find_all("tr", attrs={"class": "data-row"}):
        
        location_ = job.find_next('td', attrs={'class': 'colLocation hidden-phone'}).find('span',attrs={'class':"jobLocation"}).text.strip().split(',')[0]
        if location_ == 'Bucharest':
            location_ = "Bucuresti"
         
        # get jobs items from response
        job_list.append(Item(
            job_title=job.find("a", attrs={"class":"jobTitle-link"}).text.strip(),
            job_link="https://jobs.bunge.com" + job.find("a",attrs={"class":"jobTitle-link"})['href'].strip(),
            company=COMPANY,
            country='Romania',
            county=get_county(location_),
            city=location_,
            remote='on-site',
        ).to_dict())

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = COMPANY

    jobs = scraper()
    

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, LOGO_LINK)


if __name__ == '__main__':
    main()
