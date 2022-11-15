import re
import requests
from bs4 import BeautifulSoup
from helium import *

'''
with open('PracticeWebsite/tf_home.html', 'r') as html_file:
    content = html_file.read()
    
    soup = BeautifulSoup(content, 'lxml')
    reviews = soup.find_all('blockquote', class_='review')

    pattern = re.compile(u'\u2014') # unicode for &mdash;

    for children in reviews:
        user_names = children.find_all('p', text=pattern)

        for user in user_names:
            name = user.text[2:]

            print(name)
'''


url = 'https://catalog.nr.edu/preview_program.php?catoid=30&poid=1282'
browser = start_chrome(url, headless=True)

soup = BeautifulSoup(browser.page_source, 'html.parser')

class_reqs = soup.find_all('li', class_='acalog-course')

for req in class_reqs:
    requirement = req.text

    print(requirement)



