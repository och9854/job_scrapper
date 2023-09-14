import time
from requests import get
from bs4 import BeautifulSoup
from extractors.wwr import extract_wwr_jobs
from extractors.indeed import extract_indeed_jobs
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


keyword = input("What do you want to search for? ")
indeed = extract_indeed_jobs(keyword)
wwr = extract_wwr_jobs(keyword)
jobs = indeed + wwr


# create file and save
file = open(f"{keyword}.csv", "w")

file.write("Position, Company, Location, URL \n")

for job in indeed:
    file.write(
        f"{job['position']}, {job['company']}, {job['location']}, {job['link']} \n")
