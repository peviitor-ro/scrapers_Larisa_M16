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
import requests
 
 
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
import datetime
import re
import calendar

current_year = datetime.datetime.now().year

def scraper():
    '''
    ... scrape data from Autototal scraper.
    '''
    soup = GetStaticSoup("https://www.autototal.ro/cariere/")

    # date and month
    today_date = date.today().day
    current_month = date.today().month

    # dict for clean data by date
    autototal_months = {'ian.': 1, 'febr.': 2, 'mart.': 3,
                        'apr.': 4, 'mai': 5, 'iun.': 6,
                        'iul.': 7, 'aug.': 8, 'sept.': 9,
                        'oct.': 10, 'nov.': 11, 'dec.': 12,
                        'august.': 8}

    job_list = []
    for job in soup.find_all('div', attrs={'class': 'gem-compact-tiny-right'}):

        # save title and link -> if check_data == true
        link_job = job.find('a')['href']
        summary = job.find('div', attrs={'class': 'summary text-body-tiny'}).text.lower()

        # extract date
        summary_sort = ''
        for ij in range (2024, 2030):
            if str(ij) in summary:
                summary_sort = summary[summary.index('expiră'):summary.index(str(ij)) +4]
                break

        # split to make list from string
        summary_sort = summary_sort.split()
        try:
            if int(summary_sort[1]) > today_date and autototal_months[summary_sort[2]] == current_month or autototal_months[summary_sort[2]] > current_month:
                request_for_city = GetStaticSoup(link_job)
                city_name = request_for_city.find('div', attrs={'class': 'wpb_wrapper'}).find('p').text.split('\n')[0].split(':')[1].strip().split()
                special_c = ['–','.',':',';' ]

                job_list.append(Item(
                    job_title=job.find('a').text.strip(),
                    job_link=link_job,
                    company='AUTOTOTAL',
                    country='Romania',
                    county=[get_county(city_l) for city_l in city_name if city_l not in special_c],
                    city=[city_l for city_l in city_name if city_l not in special_c],
                    remote='onsite',
                ).to_dict())
        except:
            continue
        
    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "AUTOTOTAL"
    logo_link = "https://www.autototal.ro/wp-content/uploads/thegem-logos/logo_f7149358a9d89410af13364be85f4883_1x.png"

    jobs = scraper()
    print(jobs)
     

    # uncomment if your scraper done
    #UpdateAPI().update_jobs(company_name, jobs)
    #UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()