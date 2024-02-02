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
# Company ---> monefy
# Link ------> https://monefy.ro/careers/
#
#
from  __utils import (
    GetStaticSoup,
    get_county,
    get_job_type,
    Item,
    UpdateAPI,
)

def get_location(response: GetStaticSoup) -> str:
    locations = [
        location.split(":")[1]
        for element in response.find_all("div", {"class": "et_pb_text_inner"})
        for location in element.text.split()
        if "location" in location.lower()
    ]

    if locations:
        if locations[0] == 'Bucharest':
            return 'Bucuresti'

    return 'Bucuresti'


def scraper():
    '''
    ... scrape data from monefy scraper.
    '''
    soup = GetStaticSoup("https://monefy.ro/careers/")

    job_list = []
    for job in soup.find_all('h3', attrs={'class': 'entry-title'}):
        response = GetStaticSoup(job.a['href'])

        # get jobs items from response
        job_list.append(Item(
            job_title=job.find('a').text,
            job_link=job.a['href'],
            company='Monefy',
            country='Romania',
            county=get_county(get_location(response)),
            city=get_location(response),
            remote='Remote',
        ).to_dict())

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "Monefy"
    logo_link = "https://monefy.ro/wp-content/uploads/2021/02/Logo.png"

    jobs = scraper()
    
    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
