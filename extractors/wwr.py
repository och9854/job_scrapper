from requests import get
from bs4 import BeautifulSoup


def extract_wwr_jobs(keyword) -> list:
    base_url = 'https://weworkremotely.com/remote-jobs/search?term='
    search_term = f'{keyword}'  # any language or serach terms
    response = get(f'{base_url}{search_term}')

    if response.status_code != 200:
        print("Can't request webiste")
    else:
        result = []
        soup = BeautifulSoup(response.text, "html.parser")
        jobs = soup.find_all("section", class_='jobs')

        for job_section in jobs:
            job_posts = job_section.find_all("li")
            job_posts.pop(-1)  # remove last item: 'view-all' li

            for post in job_posts:
                anchor = post.find_all('a')[1]  # get only second one
                link = anchor['href']
                # print(link)
                company, kind, region = anchor.find_all(
                    "span", class_='company')
                title = anchor.find("span", class_='title')
                job_data = {
                    'link': f"https://weworkremotely.com/{link}",
                    'company': company.string,
                    'location': region.string,
                    'position': title.string
                }
                result.append(job_data)

        return result


# print(extract_wwr_jobs('python'))
