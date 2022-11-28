
import csv
import requests
from bs4 import BeautifulSoup
from pathlib import Path


def get_proxies():
    url = 'https://github.com/mertguvencli/http-proxy-list/blob/main/proxy-list/data.txt'
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser').find_all('td', {'class': 'blob-code blob-code-inner js-file-line'})

    proxies_list = [{'https':proxy.text} for proxy in soup]
    return proxies_list

possible_proxies = get_proxies()



def proxy_sorter():
    all_items = len(possible_proxies)
    current_item = 0

    print(f'total proxies to scan: {all_items}')
    for proxy in possible_proxies:
        current_item += 1
        try:
            r = requests.get('https://www.shopify.com/', proxies=proxy, timeout=3)
            print(proxy, r.status_code, 'success', f'{current_item}/{all_items}')

            if (r.status_code) == 200:

                with open(Path(__file__).with_name('proxies.csv'), 'a', newline='') as f:
                    writer = csv.DictWriter(f, proxy.keys())
                    writer.writerows(proxy)

            else:
                print(proxy, 'invalid http code')

        except:
            print(proxy, 'failed', f'{current_item}/{all_items}')

# proxy_sorter()



def proxy_rectifier():

    with open(Path(__file__).with_name('proxies.csv'), 'r') as f:
        reader = csv.reader(f)

        for row in reader:
            proxy_item = {row[0]: row[1]}

            for proxy in proxy_item:
                try:
                    r = requests.get('https://www.google.com/', proxies=proxy_item, timeout=10)
                    print(proxy, r.status_code, end=' ')

                    if r.status_code != 200:
                        print(proxy_item, 'unsuccessful')
                    else:
                        print(proxy_item, 'successful')

                except:
                    print(proxy_item, 'invalid')

proxy_rectifier()


