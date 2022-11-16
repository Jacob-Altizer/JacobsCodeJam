
import re
import requests
from bs4 import BeautifulSoup
from helium import *
import os
from pathlib import Path
import sqlite3

# Full stack url https://catalog.nr.edu/preview_program.php?catoid=30&poid=1282
# NRCC programs list https://catalog.nr.edu/content.php?catoid=30&navoid=2019

NRCC_Catalog = 'https://catalog.nr.edu/content.php?catoid=30&navoid=2019'


connection = sqlite3.connect(Path(__file__).with_name('data.db'))
cursor = connection.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS aas_program_index
                        (program_name text, poid integer)''')


cursor.execute('''INSERT INTO aas_program_index VALUES
                        ('Information_Technology-Full_Stack_Developer_Specialization_AAS', '1282')''')

connection.commit()

for row in cursor.execute('''SELECT * FROM aas_program_index'''):
    print(row)

# opens a headless browser and goes to desired url / headless cuz javascript and such
def headless_browser(url):

    browser = start_chrome(url, headless=True)

    return browser



def program_address():

    program_name = []
    poid = []

    # scans html provided by browser var
    soup = BeautifulSoup(headless_browser(NRCC_Catalog).page_source, 'html.parser')

    # finds the Associate of Applied Science ul and returns every anchor tag
    AAS_programs_list = soup.select(selector='td.block_content ul:nth-of-type(2) a')

    for program in AAS_programs_list:

        # pulls text inside list anchor tags / replaces space chars with _
        program_name.append(program.text.replace(' ', '_'))

        # pulls poid value in list anchor tag hrefs
        split_href = re.split('&|=', program.get('href'))
        poid.append(int(split_href[-3]))

    # zips program_name & poid lists into AAS_programs dictionary
    AAS_programs = {program_name:poid for (program_name, poid) in zip(program_name, poid)}

    return AAS_programs

# print(program_address())
