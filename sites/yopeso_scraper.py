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
# Company ---> yopeso
# Link ------> https://careers.yopeso.com/
#
#
import sys
import os
directory = os.path.abspath(".\\")
sys.path.append(directory)

from __utils import (
    GetStaticSoup,
    get_county,
    get_job_type,
    Item,
    UpdateAPI,
)

def scraper():
    '''
    ... scrape data from yopeso scraper.
    '''
    soup = GetStaticSoup("https://careers.yopeso.com/")

    job_list = []
    for job in soup.find_all("div", attrs={"class":"sc-6exb5d-3 gnPPfQ"}):

        location = job.find("span", attrs={"class":"custom-css-style-job-location-city"}).text

        country_ = job.find("span", attrs={"class":"custom-css-style-job-location-country"}).text 

        job_type_ = job.find("span", attrs={"class":"sc-1s8re0d-0 feitSf"})
        if job_type_:
            new_job_type = job_type_.text
        else:
            new_job_type = "on-site"

        if country_.lower() == "romania":


            # get jobs items from response
            job_list.append(Item(
                job_title=job.find("a", attrs={"class":"sc-6exb5d-1 fmfYYf"}).text,
                job_link='https://careers.yopeso.com' + job.find("a", attrs={"class":"sc-6exb5d-1 fmfYYf"})["href"],
                company='Yopeso',
                country=country_.replace("Romania", "Romania"),
                county=get_county(location),
                city=location,
                remote=get_job_type(new_job_type),
            ).to_dict())

    return job_list



def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "Yopeso"
    logo_link = "https://www.yopeso.com/wp-content/uploads/2022/05/logo-Yopeso-150x78.png"

    jobs = scraper()
    
    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
