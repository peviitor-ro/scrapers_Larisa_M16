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
# Company ---> agilefreaks
# Link ------>  https://careers.agilefreaks.com/jobs
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
    ... scrape data from agilefreaks scraper.
    '''
    soup = GetStaticSoup(" https://careers.agilefreaks.com/jobs")

    job_list = []
    jobtype = ""
    
    for job in soup.find_all("li",attrs={"class":"w-full"}):
        location = job.find("div", attrs={"class":"mt-1 text-md"}).find_all("span")
        if len(location) > 1:
            split_loc = [x.lower() for x in location[-1].text.split()]
             
            if "remote" in split_loc:
                jobtype = 'remote'
            elif 'hybrid' in split_loc:
                jobtype = 'hybrid'
        else: 
            jobtype = location[0].text


        # get jobs items from response
        job_list.append(Item(
            job_title=job.find("span", attrs={"class":"text-block-base-link sm:min-w-[25%] sm:truncate company-link-style"}).text,
            job_link=job.find('a', attrs={'class': 'flex flex-col py-6 text-center sm:px-6 hover:bg-gradient-block-base-bg focus-visible-company focus-visible:rounded'})['href'],
            company='AgileFreaks',
            country='România',
            county=get_county(location[0].text),
            city= location[0].text,
            remote=get_job_type(jobtype),
        ).to_dict())

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "AgileFreaks"
    logo_link = "https://images.teamtailor-cdn.com/images/s3/teamtailor-production/logotype-v3/image_uploads/3866dbb1-2690-4a4a-8c59-951548beda43/original.png"

    jobs = scraper()
    

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
