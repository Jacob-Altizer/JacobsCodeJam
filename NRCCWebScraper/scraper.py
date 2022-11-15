
import re
import requests
from bs4 import BeautifulSoup
from helium import *
import json


def write_json(new_data, filename='data.json'):
    with open(filename, 'r+') as file:
        file_data = json.load(file)
        file_data["Full-Stack Web Developer"].append(new_data)
        file.seek(0)
        json.dump(file_data, file, indent = 4)

# Full stack url https://catalog.nr.edu/preview_program.php?catoid=30&poid=1282
# NRCC programs list https://catalog.nr.edu/content.php?catoid=30&navoid=2019

# opens a headless browser and goes to desired url / headless cuz javascript and such
url = 'https://catalog.nr.edu/content.php?catoid=30&navoid=2019'
browser = start_chrome(url, headless=True)

# scans html provided by browser var
soup = BeautifulSoup(browser.page_source, 'html.parser')

# finds the Associate of Applied Science ul and returns every anchor tag
AAS_programs_list = soup.select(selector='td.block_content ul:nth-of-type(2) a')

program_name = []
poid = []

for program in AAS_programs_list:

    program_name.append(program.text)

    split_href = re.split('&|=', program.get('href'))
    poid.append(split_href[-3])

    # print(program.text, program.get('href')) # returns text from inside anchor tag, href from anchor tag

AAS_programs = {program_name:poid for (program_name, poid) in zip(program_name, poid)}
print(AAS_programs)


# class_reqs = soup.find_all('li', class_='acalog-course')


# for req in class_reqs:
#     data = {}
#     data['required_class'] = req

# write_json(data)

