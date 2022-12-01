
import re
from bs4 import BeautifulSoup
import helium as he
import os
from pathlib import Path
import sqlite3
import time


# Full stack url https://catalog.nr.edu/preview_program.php?catoid=30&poid=1282
# NRCC programs list https://catalog.nr.edu/content.php?catoid=30&navoid=2019

# proxies = 107.152.42.141:8080, 47.89.185.178:8888

NRCC_Catalog = 'https://catalog.nr.edu/content.php?catoid=30&navoid=2019'

# opens a headless browser and goes to desired url / headless cuz javascript and such
def headless_browser(url):

    browser = he.start_firefox(url, headless=False)
    
    return browser



def write_database(data_list):

    '''
    Define list of data to be input in scraping function 'table_name, data, contents, data_format' in that order\n
    Example:

        table_name = 'programs_index'
        data = list(zip(program_name, poid))
        contents = 'program_name TEXT, poid INTEGER'
        data_format = '?,?'

    table_name: name of the desired table to create/write to
    data: list of tuples to be written
    contents: desired column name(s) and their data type as tuple "(data_name1 TEXT, data_name2 INTEGER, etc...)"
    data_format: column format to be created for table "(?,?,?,etc...)"
    '''

    table_name, data, contents, data_format = data_list[0], data_list[1], data_list[2], data_list[3]

    conn = sqlite3.connect(Path(__file__).with_name('data.db'))
    c = conn.cursor()
    
    c.execute(f"""CREATE TABLE IF NOT EXISTS '{table_name}' ({contents})""")

    c.executemany(f"""INSERT OR REPLACE INTO '{table_name}' VALUES ({data_format})""", data)

    conn.commit()

    conn.close()



def read_database():

    conn = sqlite3.connect(Path(__file__).with_name('data.db'))
    c = conn.cursor()

    c.execute("""SELECT poid FROM programs_index WHERE program_name='Information_Technology-Full_Stack_Developer_Specialization_AAS' """)

    print(c.fetchall())

    conn.commit()

    conn.close()

#read_database()



def program_addresses():

    program_name = []
    poid = []

    # scans html provided by browser var
    soup = BeautifulSoup(headless_browser(NRCC_Catalog).page_source, 'html.parser')

    # finds each ul in NRCC Catalog
    programs_list = soup.select(selector='td.block_content ul a')

    for program in programs_list:

        program_name.append(program.text.replace(' ', '_').replace('-', '_'))
        
        # pulls poid value in list anchor tag hrefs
        split_href = re.split('&|=', program.get('href'))
        poid.append(int(split_href[-3]))

    ## desired formatting for program_addresses function

    table_name = 'programs_index' # name of table for this function
    data = list(zip(program_name, poid)) # zips program_name & poid lists into AAS_programs list of tuples
    contents = 'program_name TEXT, poid INTEGER' # column names and their value type
    data_format = '?,?' # place holder column format

    return table_name, data, contents, data_format



def program_classes():
    template_url = f'https://catalog.nr.edu/preview_program.php?catoid=30&poid=' # 1282
    classes = []

    conn = sqlite3.connect(Path(__file__).with_name('data.db'))
    c = conn.cursor()

    c.execute(f"""SELECT * FROM programs_index""")

    for info in c.fetchall():
        print(info)
        address = str(info[1])

        soup = BeautifulSoup(headless_browser(template_url + address).page_source, 'html.parser')
        all_reqs = soup.select(selector='li.acalog-course span a')

        for requirement in all_reqs:
            req_item = requirement.text.strip()
            classes.append((req_item, address))

        he.kill_browser()

        time.sleep(10)

    conn.close()

    table_name = 'class_requirements' # name of table for this function
    data = classes
    contents = 'class_name TEXT, poid INTEGER' # column names and their value type
    data_format = '?,?' # place holder column format

    return table_name, data, contents, data_format


#write_database(program_addresses())
write_database(program_classes())


