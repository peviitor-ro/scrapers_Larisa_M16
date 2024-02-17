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
# Company ---> Fieldcore
# Link ------> https://www.fieldcore.com/careers/jobs/?p=search&r=&l=Remote+-+Romania+%28LR18%29&c=&q=&nl=1
#
#
#
from sites.__utils.req_bs4_shorts import GetXMLObject, GetStaticSoup
from sites.__utils.items_struct import Item
from sites.__utils.peviitor_update import UpdateAPI
from sites.__utils.found_county import get_county
from sites.__utils.get_job_type import get_job_type



def scraper():
    '''
    ... scrape data from Fieldcore scraper.
    '''
    soup = GetStaticSoup("https://jobs.jobvite.com/fieldcore/search?nl=1&nl=1&r=&l=Remote%20-%20Romania%20(LR18)&c=&q=&fr=true")

    job_list = []
    for job in soup.find_all('td', attrs={'class':'jv-job-list-name'}):
        job_location = [element.strip() for element in
                        job.find_next('div', class_='jv-job-list-location').text.strip().split('\n')]
                
        # get jobs items from response
        job_list.append(Item(
            job_title=job.find('div', class_='title').text.strip(),
            job_link='https://jobs.jobvite.com/'+ job.find('a')['href'],
            company='Fieldcore',
            country='Romania',
            county='',
            city='',
            remote='Remote',
        ).to_dict())

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "Fieldcore"
    logo_link = "https://www.fieldcore.com/wp-content/uploads/2022/09/logo-new.png"

    jobs = scraper()
      
    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
