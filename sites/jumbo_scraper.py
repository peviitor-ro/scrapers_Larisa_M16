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
# Company ---> jumbo
# Link ------> https://corporate.e-jumbo.gr/ro/job-opportunities/theseis-ergasias/
#
#
#
from sites.__utils.req_bs4_shorts import GetStaticSoup
from sites.__utils.items_struct import Item
from sites.__utils.peviitor_update import UpdateAPI
from sites.__utils.found_county import get_county

def scraper():
    '''
    ... scrape data from jumbo scraper.
    '''
    soup = GetStaticSoup("https://corporate.e-jumbo.gr/ro/job-opportunities/theseis-ergasias/")

    # default location for this company
    jumbo_locations = ["Bucuresti",
                       "Timisoara", "Oradea",
                       "Arad", "Ploiesti", "Pitesti",
                       "Constanta", "Suceava", "Bacau", "Braila",
                       "Brasov", "Craiova",
                       ]

    job_list = []
    for job in soup.find_all('article', attrs={'class': 'x-control x-box x-article-box careers-article'}):

        # get jobs items from response
        job_list.append(Item(
            job_title=job.find('h2', attrs={'class': 'title'}).text.strip(),
            job_link='https://corporate.e-jumbo.gr' + job.find('a', attrs={'class': 'view-more'})['href'],
            company='Jumbo',
            country='Romania',
            county=[get_county(town) for town in jumbo_locations],
            city=jumbo_locations,
            remote='on-site'
        ).to_dict())

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "jumbo"
    logo_link = "https://corporate.e-jumbo.gr/uploads/images/logo.png"

    jobs = scraper()

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
