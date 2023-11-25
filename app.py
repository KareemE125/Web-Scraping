import requests
from bs4 import BeautifulSoup
import csv

page = requests.get('https://wuzzuf.net/search/jobs/?a=hpb%7Cspbg&q=python%20web%20scraping')


def main(page):
    src = page.content
    soup = BeautifulSoup(src, 'lxml')
    
    jobs = soup.find_all('div', {"class": "css-pkv5jc"})
    jobTitles = []
    jobCompanies = []
    jobLocations = []
    jobSkills = []
    jobLinks = []

    jobSearchResults = []


    for job in jobs:
        upperSections = job.find_all('div', {"class": "css-laomuu"})
        for section in upperSections:
            titleAndLinks = section.find('h2')
            jobTitles.append(titleAndLinks.text.strip())
            jobLinks.append(titleAndLinks.find('a').attrs['href'])
            jobCompanies.append(section.find('div', {"class": "css-d7j1kk"}).find('a').text.replace('-', '').strip())
            jobLocations.append(section.find('div', {"class": "css-d7j1kk"}).find('span',{'class':'css-5wys0k'}).text.replace('-', '').strip())

        lowerSections = job.find_all('div', {"class": "css-y4udm8"})
        for section in lowerSections:
            skillSet = section.text.strip().replace('· ', ', ')
            jobSkills.append(skillSet)
            


    with open('jobs.csv', 'w', encoding='utf-8', newline='') as csvfile:
       wr = csv.writer(csvfile)
       wr.writerow(['Job Title', 'Company', 'Location', 'Skills', 'Link'])
       wr.writerows(zip(jobTitles, jobCompanies, jobLocations, jobSkills, jobLinks))
            

    
    
main(page)

    
    