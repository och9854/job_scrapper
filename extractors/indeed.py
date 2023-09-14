import time
from requests import get
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
# from extractors.wwr import extract_wwr_jobs

# use selenium
# dont need to worry about three lines below
options = Options()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")


def extract_indeed_jobs(keyword):  # search jobs in one page
    pages = get_page_count(keyword)
    print(f"Found {pages} pages")
    results = []
    for page in range(pages):
        # broswer = webdriver.Chrome(options=options)
        browser = webdriver.Chrome(
            '/Users/ohchanghyun/Desktop/nomad_coder/web_scrapper/chromedriver', options=options)

        url = f"https://kr.indeed.com/jobs?q={keyword}&start={page*10}"
        print(f"Requesting {url}")
        browser.get(url=url)

        # use soup
        soup = BeautifulSoup(browser.page_source, "html.parser")
        job_list = soup.find("ul", class_="css-zu9cdh eu4oa1w0")
        # make soup find only depth-one 'li' s
        jobs = job_list.find_all("li", recursive=False)
        for job in jobs:
            zone = job.find("div", class_='mosaic-zone nonJobContent-desktop')
            if zone is None:
                anchor = job.select_one("h2 a")
                title = anchor['aria-label']
                link = anchor['href']
                company = job.find("span", class_="companyName")
                location = job.find("div", class_="companyLocation")
                job_data = {
                    'link': f"https://kr.indeed.com{link}",
                    'company': company.string,
                    'location': location.string,
                    'position': title
                }
                print(job_data)
                for _ in job_data:
                    if job_data[_] != None:
                        job_data[_] = job_data[_].replace(",", " ")
                    else:
                        job_data[_] = ""
                results.append(job_data)

    return results
# traverse pages


def get_page_count(keyword):
    # broswer = webdriver.Chrome(options=options)
    browser = webdriver.Chrome(
        '/Users/ohchanghyun/Desktop/nomad_coder/web_scrapper/chromedriver', options=options)
    url = f"https://kr.indeed.com/jobs?q={keyword}&limit=50"

    browser.get(url=url)
    soup = BeautifulSoup(browser.page_source, "html.parser")

    # search pagination
    pagination = soup.find('nav', class_='css-jbuxu0 ecydgvn0')
    if pagination == None:  # if it doesnt exist
        return 1
    pages = pagination.find_all(
        'div', class_='css-tvvxwd ecydgvn1', recursive=False)

    count = len(pages)
    if count >= 5:
        return 5
    else:
        return count


# jobs = extract_indeed_jobs('python')
