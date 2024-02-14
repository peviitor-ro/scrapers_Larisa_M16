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
# Company ---> canamgroup
# Link ------>  https://www.canam.com/en/job-opportunities/?country%5B%5D=romania&search=
#
#
#
from sites.__utils.req_bs4_shorts import GetStaticSoup
from sites.__utils.items_struct import Item
from sites.__utils.peviitor_update import UpdateAPI
from sites.__utils.found_county import get_county
from sites.__utils.get_job_type import get_job_type

def scraper():
    '''
    ... scrape data from canamgroup scraper.
    '''
    soup = GetStaticSoup(" https://www.canam.com/en/job-opportunities/?country%5B%5D=romania&search=")

    job_list = []
    for job in soup.find_all('a', attrs={'class': "c-card-job"}):
        job_ = job.find("div", attrs= {"class":'c-card-job__title u-heading-600'}).find("span").text
        location = job.find("div", attrs={'class': "c-btn c-btn--ghost c-btn--tag u-pointer-events-none"}).text.strip()
   
        # get jobs items from response
        job_list.append(Item(
            job_title=job_,
            job_link=job.get('href'),
            company='CanamGroup',
            country='Romania',
            county=get_county(location),
            city="Brasov",
            remote=get_job_type(location),
        ).to_dict())

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "CanamGroup"
    logo_link = "https://www.canam.com/wp-content/themes/canam/dist/img/logo-canam.png"

    jobs = scraper()
    
    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
