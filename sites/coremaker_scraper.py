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
# Company ---> coremaker
# Link ------> https://coremaker.io/careers/
#
#
from __utils import (
    GetStaticSoup,
    get_county,
    get_job_type,
    Item,
    UpdateAPI,
)

def scraper():
    '''
    ... scrape data from coremaker scraper.
    '''
    soup = GetStaticSoup("https://coremaker.io/careers/")

    job_list = []
    for job in soup.find_all("div", attrs={"class":"MuiGrid-root MuiGrid-item MuiGrid-grid-xs-12 MuiGrid-grid-sm-6 MuiGrid-grid-md-4"}):
        location = job.find("span").text.split(",")[-1].strip()

        # get jobs items from response
        job_list.append(Item(
            job_title=job.find('h5',attrs={'class': 'MuiTypography-root jss42 MuiTypography-h5'}).text.strip(),
            job_link="https://coremaker.io" + job.a['href'].strip(),
            company='Coremaker',
            country='Romania',
            county=get_county('Bucuresti'),
            city='Bucuresti',
            remote=get_job_type(location),
        ).to_dict())

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "Coremaker"
    logo_link = "https://media.licdn.com/dms/image/D4E0BAQFTsqltRbQyCA/company-logo_200_200/0/1687867397006/coremaker_logo?e=2147483647&v=beta&t=Bx3t8KSGVS4eJEME2dI8MdcNBX7vDXtDqIqs0xw1Pos"

    jobs = scraper()
     
    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
