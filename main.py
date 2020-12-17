from collections import Counter,defaultdict
from bs4 import BeautifulSoup
import requests

def year_archive_scraping(year):
    global organization_index
    global org_dataset
    source = requests.get("https://summerofcode.withgoogle.com/archive/{}/organizations/".format(year)).text
    soup_orgs = BeautifulSoup(source,'lxml')
    org_list = []
    org_details = {}
    for org_card in soup_orgs.section.ul.find_all('li'):
        #EXTRACTING ORG_NAME AND LINK FROM MAIN LIST
        organization_name = org_card.h4.text.lower()
        organization_link = org_card.a["href"]
        #PARSING DETAILS FROM EXTRACTED LINK
        organization_html = BeautifulSoup(requests.get("https://summerofcode.withgoogle.com"+organization_link).text,'lxml')
        details = {}
        details["category"],details["tech"],details["topics"],details["contact"] = organization(organization_html)
        details["proj_count"],details["proj"] = organization_proj(organization_html,year)
        org_details[organization_name]=details
        details = {}
        org_dataset.add(organization_name)
    organization_index[year]=org_details

def organization(soup_org):
    website_segment = soup_org.section.div
    technologies = [tech.text for tech in website_segment.ul.find_all('li')]
    category = website_segment.find('li',class_="organization__tag organization__tag--category").text.strip()
    topics = [topic.text for topic in website_segment.find_all('li',class_="organization__tag organization__tag--topic")]
    contacts = [contact["href"] for contact in website_segment.div.find_all('md-button',class_="md-primary org__meta-button")]
    return category,technologies,topics,contacts
    
def organization_proj(soup_org,year):
    projects = soup_org.find('section',id="projects").find_all('li')
    project_count = len(projects)
    project_list = []
    for project in projects:
        name = project.h5.text.strip()
        project_name = project["aria-label"]
        project_desc = project.find('div',class_="archive-project-card__content md-padding font-black-54").text.strip()
        project_list.append([name,project_name,project_desc].replace("\n"," "))
    return project_count,project_list

org_dataset = set()
organization_index = {}
choice = input("Enter archive year(s) (2016|2017|2018|2019|2020|alltime) :")
if choice.isdigit():
    print("scraping {} archives.....".format(int(choice)))
    year_archive_scraping(int(choice))

else:
    for year in range(2016,2021):
        print("scraping {} archives.....".format(year))
        year_archive_scraping(year)



for year,details in organization_index.items():
    print(year)
    l=[]
    for org_name,org_det in details.items():
        l.append([org_det["proj_count"],org_name,org_det["category"],org_det["tech"]])
    for i in sorted(l,reverse=True):
        print(i)
    print("___________________________________________________________________________________")
    print("___________________________________________________________________________________")
    print("___________________________________________________________________________________")
    print("___________________________________________________________________________________")
