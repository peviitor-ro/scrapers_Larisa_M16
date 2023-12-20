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
from __utils import (
    GetStaticSoup,
    get_county,
    get_job_type,
    Item,
    UpdateAPI,
)

 
import cfscrape
from bs4 import BeautifulSoup
from __utils import DEFAULT_HEADERS
from sites.__utils.req_bs4_shorts import HackCloudFlare

data = HackCloudFlare('https://romania.cgsinc.com/vino-in-echipa-cgs/') 
print(data)
 


def scraper(html_content):
     soup = BeautifulSoup(html_content, "lxml")
     

      

     job_list = []
     for job in soup.find_all("div", attrs={"class":'eelementor-shortcode'}):
        location = ""

        # get jobs items from response
        job_list.append(Item(
            job_title='',
            job_link='',
            company='CGSRomania',
            country='Romania',
            county='',
            city='',
        ).to_dict())
     return job_list
     

def main():
    html_content = data.prettify()  # Assuming data is the BeautifulSoup object from HackCloudFlare

    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "CGSRomania"
    logo_link = "logo_link"

    jobs = scraper(html_content)
    print(jobs)

    # uncomment if your scraper done
    #UpdateAPI().update_jobs(company_name, jobs)
    #UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()