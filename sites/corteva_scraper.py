#
#
# Configurare pentru Scraperul Dynamic Render!
# Company ---> corteva
# Link ------> https://careers.corteva.com/job-search-results/?keyword=Romania
#
# ------ IMPORTANT! ------
# if you need return soup object:
# you cand import from __utils -> GetHtmlSoup
# if you need return regex object:
# you cand import from __utils ->
# ---> get_data_with_regex(expression: str, object: str)
#
#
from __utils import (
    GetDynamicSoup,
    get_county,
    get_job_type,
    Item,
    UpdateAPI,
)


'''
    Daca deja te-ai deprins cu aceasta formula de cod,
    atunci poti sterge acest comentariu din fisierul
    __create_scraper.py, din functia - create_static_scraper_config -.

    Deci:
    ########################################################################

    1) --->  clasa GetDynamicSoup returneaza un obiect HTML in urma unui
    request pe un site dinamic, car se incarca cu javascript.

    De obicei unele site-uri nu pot fi scrapuite cu get request sau cu post request.
    Motive sunt diferite. Dar, folosind GetDynamicSoup, putem sa returnam un html
    care sta in spatele unui cod de JS.

    get_dynamic_soup = GetDynamicSoup(link) -> si primim html intr-un obiect BeautifulSoup.

    Putem sa-i dam si headere:
    GetDynamicSoup(link, custom_headers=headers)

    --------------IMPORTANT----------------
    La nivel de proiect, ca o variabila globala, este definit Session()!
    ... acest session inseamna ca orice clasa va putea folosi
    ... aceeasi sesiune, practic se va evita multiple requests;

    ########################################################################

    2) ---> get_county(nume_localitat) -> returneaza numele judetului;
    poti pune chiar si judetul, de exemplu, nu va fi o eroare.

    ########################################################################

    3) --->get_job_type(job_type: str) -> returneaza job_type-ul: remote,
    hybrid, on-site

    ########################################################################

    4) ---> Item -> este un struct pentru datele pe care le vom stoca in lista
    si, apoi, le vom trimite catre API.
    exemplu: list_jobs.append(Item(job_title="titlu_str",
                                    job_link="link",
                                    company="nume_companie",
                                    country="Romania",
                                    county="Judetul",
                                    city="Orasul",
                                    remote="remote, onsite sau hibryd"))

    ########################################################################

    5) ---> clasa UpdateAPI are doua metode:
    update_jobs(lista_dict_joburi) si update_logo(nume_companie, link_logo)

    UpdateAPI().update_jobs(company_name: str, data_jobs: list)
    UpdateAPI().update_logo(id_company: str, logo_link: str)

    ########################################################################
    '''

def scraper():
    '''
    ... scrape data from corteva scraper.
    '''
    soup = GetDynamicSoup("https://careers.corteva.com/job-search-results/?keyword=Romania")

    job_list = []
    for job in soup.find_all('div', attrs={'class','job-innerwrap g-cols'}):
        location = job.find('div', attrs={'class',"parent location"}).text.split(',')[1]
      
        # get jobs items from response
        job_list.append(Item(
            job_title=job.find('a').text,
            job_link='https://careers.corteva.com/' + job.find('a')['href'],
            company='CORTEVA',
            country='Romania',
            county=location,
            city=location,
            remote='remote',
        ).to_dict())

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "CORTEVA"
    logo_link = "https://cdn-static.findly.com/wp-content/uploads/sites/2491/2023/02/02100420/logo.svg"

    jobs = scraper()
  
    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
