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
# Company ---> monefy
# Link ------> https://monefy.ro/careers/
#
#
from sites.__utils import (
    GetStaticSoup,
    get_county,
    get_job_type,
    Item,
    UpdateAPI,
)


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
    In interiorul clasei GetStaticSoup este definit Session() ->
    deci requesturile se fac in aceeasi sesiune!

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

def get_location(response: GetStaticSoup) -> str:
    locations = [
        location.split(":")[1]
        for element in response.find_all("div", {"class": "et_pb_text_inner"})
        for location in element.text.split()
        if "location" in location.lower()
    ]

    if locations:
        if locations[0] == 'Bucharest':
            return 'Bucuresti'

    return 'Bucuresti'


def scraper():
    '''
    ... scrape data from monefy scraper.
    '''
    soup = GetStaticSoup("https://monefy.ro/careers/")

    job_list = []
    for job in soup.find_all('h3', attrs={'class': 'entry-title'}):
        response = GetStaticSoup(job.a['href'])

        # get jobs items from response
        job_list.append(Item(
            job_title=job.find('a').text,
            job_link=job.a['href'],
            company='monefy',
            country='România',
            county=get_county(get_location(response)),
            city=get_location(response),
            remote='Remote',
        ).to_dict())

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "monefy"
    logo_link = "https://monefy.ro/wp-content/uploads/2021/02/Logo.png"

    jobs = scraper()
    
    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
