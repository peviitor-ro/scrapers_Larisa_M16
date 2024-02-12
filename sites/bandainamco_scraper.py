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
# Company ---> bandainamco
# Link ------> https://www.bandainamcoent.ro/ro/careers/
#
#
#
from sites.__utils.req_bs4_shorts import GetStaticSoup
from sites.__utils.items_struct import Item
from sites.__utils.peviitor_update import UpdateAPI
from sites.__utils.found_county import get_county

def scraper():
    '''
    ... scrape data from bandainamco scraper.
    '''
    soup = GetStaticSoup("https://www.bandainamcoent.ro/ro/careers/")

    job_list = []
    for job in soup.find_all('p', attrs={'class':'career_job_links has-text-align-center has-black-color has-text-color'}):
        
        # get jobs items from response
        job_list.append(Item(
            job_title=job.find('a').text.strip(),
            job_link= 'https://www.bandainamcoent.ro' + job.find("a")["href"].strip(),
            company='Bandainamco',
            country='România',
            county=get_county('Bucuresti'),
            city='Bucuresti',
            remote='on-site',
        ).to_dict())

    return job_list

def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "Bandainamco"
    logo_link = "https://www.bandainamcoent.ro/wp-content/themes/namco/img/logo_small.jpg"

    jobs = scraper()
     
    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
