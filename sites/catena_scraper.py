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
# Company ---> catena
# Link ------> https://www.catena.ro/cariere
#
#
#
from sites.__utils.req_bs4_shorts import GetStaticSoup
from sites.__utils.items_struct import Item
from sites.__utils.peviitor_update import UpdateAPI
from sites.__utils.found_county import get_county

def scraper():
    '''
    ... scrape data from catena scraper.
    '''
    soup = GetStaticSoup("https://www.catena.ro/cariere")
    # default location for this company
    catena_locations = ["Popesti",
                        "Bucuresti" ,
                       "Timisoara","Iasi",
                       "Targu Mures", "Brasov", 
                       "Sibiu", "Valcea", "Campulung", "Reghin", "Mangalia", "Falticeni", "Zarnesti", "Vaslui",
                        "Suceava",
                       ]
    

    job_list = []
    for job in soup.find_all('div', attrs= {'class':'job_block'}):
         
        # get jobs items from response
        job_list.append(Item(
            job_title=job.find('a').text.strip(),
            job_link='https://www.catena.ro' + job.find("a")["href"].strip(),
            company='Catena',
            country='Romania',
            county=[get_county(town) for town in catena_locations],
            city=catena_locations,
            remote='on-site',
        ).to_dict())

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''
    company_name = "Catena"
    logo_link = "https://www.catena.ro/assets/uploads/content_images/noimage-og.png"

    jobs = scraper()

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
