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
# Company ---> autototal
# Link ------> https://www.autototal.ro/cariere
#
#
from __utils import (
    GetStaticSoup,
    get_county,
    get_job_type,
    Item,
    UpdateAPI,
)

from datetime import date
import uuid
 
'''
    Daca te-ai deprins cu aceasta formula de cod,
    atunci poti sterge acest comentariu din fisierul
    __create_scraper.py, din functia -> create_static_scraper_config <-

    Deci:
    ########################################################################
    1) --->  clasa GetStaticSoup returneaza un obiect BeautifulSoup,
    direct in instanta, fara a apela alte metode.

    soup = GetStaticSoup(link) -> si gata, ai acces la obiectul soup
    si deja poti face -> for job in soup.find_all(...)

    + poti sa-i adaugi si custom_headers
    soup = GetStaticSoup(link, custom_headers)
    ... by default, custom_headers = None, dar in __utils ai un fisier
    default_headers.py unde poti sa-ti setezi headerele tale default.

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
    exemplu: job_list.append(Item(job_title="titlu_str",
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
location_mapping = {
    'Expiră 9 Nov. 2023': 'Sibiu',
    'Expiră 23 Dec. 2023': '',
    'Expiră 20 Dec. 2023': 'Bacau',
    'Expiră 28 Dec. 2023': 'Deva',
    'Expiră 21 Dec. 2023': 'Targu Neamt',
    'Expiră 21 Dec. 2023':'Alba Iulia / Campeni',
    'Expiră 21 Dec. 2023':'Campeni ',
    'Expiră 20 Dec. 2023':"Iasi",
    'Expiră 14 Dec. 2023':"Neamt",
    "Expir\u0103 10 Dec. 2023":'Onesti - Bacau',
    "Expir\u0103 2 Dec. 2023":'Piatra Neamt',
    "Expir\u0103 7 Dec. 2023":'Targoviste',
    "Expir\u0103 6 Dec. 2023":'Bucuresti',
    

}


def scraper():
    '''
    ... scrape data from autototal scraper.
    '''
    soup = GetStaticSoup("https://www.autototal.ro/cariere")

    today_date = date.today().day
    current_month = date.today().month
    autototal_months = {'ian.': 1, 'febr.': 2, 'mart.': 3,
                        'apr.': 4, 'mai': 5, 'iun.': 6,
                        'iul.': 7, 'aug.': 8, 'sept.': 9,
                        'oct.': 10, 'nov.': 11, 'dec.': 12,
                        'august.': 8}
    


    job_list = []
    for job in soup.find_all("div", attrs={'class':'gem-compact-tiny-right'}):
        location = job.find("div", attrs={'class':'summary text-body-tiny'}).text.split(",")[-1].strip()
        if location in location_mapping:
            location = location_mapping[location]

        location_words = location.split()
        summary = job.find('div', class_='post-text').find('div', class_='summary').text.lower().split()
        
        summary_sort = []
        for ij in [2023, 2024, 2025]:
            if str(ij) in summary:
                summary_sort = summary[summary.index('expiră'):summary.index(str(ij)) +1 ]
                break

        # here check if conditions
        if int(summary_sort[1]) > today_date and autototal_months[summary_sort[2]] == current_month or \
                autototal_months[summary_sort[2]] > current_month:
 
         job_list.append(Item(
            job_title=job.find('a').text.strip(),
            job_link=job.find('a')['href'],
            company='AutoTotal',
            country='Romania',
            county=location,
            city=location,
            remote="on-sites",
        ).to_dict())
        
                 
    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "AutoTotal"
    logo_link = "https://www.autototal.ro/wp-content/uploads/thegem-logos/logo_f7149358a9d89410af13364be85f4883_3x.png"

    jobs = scraper()
     
      
    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
