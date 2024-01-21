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
from scrapers.__utils import (
    GetStaticSoup,
    get_county,
    get_job_type,
    Item,
    UpdateAPI,
)

def scraper():
    '''
    ... scrape data from bunge scraper.
    '''
    soup = GetStaticSoup(" https://jobs.bunge.com/search/?createNewAlert=false&q=&locationsearch=Romania&optionsFacetsDD_country=")

    job_list = []
    for job in soup.find_all("tr", attrs={"class":"data-row"}):
        
        location_ = job.find_next('td', attrs={'class': 'colLocation hidden-phone'}).find('span',attrs={'class':"jobLocation"}).text.strip().split(',')[0]
        if location_ == 'Bucharest':
            location_ = "Bucuresti"
         
        # get jobs items from response
        job_list.append(Item(
            job_title=job.find("a", attrs={"class":"jobTitle-link"}).text.strip(),
            job_link="https://jobs.bunge.com" + job.find("a",attrs={"class":"jobTitle-link"})['href'].strip(),
            company='Bunge',
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

    company_name = "Bunge"
    logo_link = "https://rmkcdn.successfactors.com/c8d09bed/298fb332-da77-4747-9f6b-9.svg"

    jobs = scraper()
    

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
