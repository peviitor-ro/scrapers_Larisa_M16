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
# Company ---> C4Media
# Link ------> https://c4media.com/career
#
#
#
from sites.__utils.req_bs4_shorts import GetStaticSoup
from sites.__utils.items_struct import Item
from sites.__utils.peviitor_update import UpdateAPI

def scraper():
    '''
    ... scrape data from C4Media scraper.
    '''
    soup = GetStaticSoup("https://c4media.com/career")

    job_list = []
    for job in soup.find_all('div', attrs={'class': 'text-left'}):
        link = job.find('a')

        if link and 'https' not in str(link):
            # get jobs items from response
            job_list.append(Item(
                job_title=link.text,
                job_link='https://c4media.com' + link.get('href'),
                company='C4Media',
                country='Romania',
                county='Bucuresti',
                city='Bucuresti',
                remote='remote',
            ).to_dict())

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "C4Media"
    logo_link = "https://c4media.com/_nuxt/img/c4media-logo.b690907.svg"

    jobs = scraper()
    
    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
