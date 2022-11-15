
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

url = 'https://catalog.nr.edu/preview_program.php?catoid=30&poid=1282'
browser = start_chrome(url, headless=True)

soup = BeautifulSoup(browser.page_source, 'html.parser')

class_reqs = soup.find_all('li', class_='acalog-course')


# for req in class_reqs:
#     data = {}
#     data['required_class'] = req

# write_json(data)

