#!/usr/bin/python3

import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import os.path, time
from datetime import datetime
import csv


url = 'https://www.uwkc.org/free-meals-during-school-closures/'
response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
soup = BeautifulSoup(response.content, 'lxml')

blocks = soup.find_all('div', {'class': 'accordion'})
results = []
for block in blocks:
    meal_info = block.find_all('p')
    for info in meal_info:
        county = block.find_previous_sibling('h2').text
        district_parent = info.find_parent('div', {'class': 'accordion_item'})
        district = district_parent.find('h3').text
        specs = info.text.split('\n')
        infolength = len(specs)
        
        if infolength < 2:
            continue
        
        if 'ROUTE' in specs[0] or 'Nutrition Delivery' in specs[0]:
            route = specs[0]
            for i in range(1, infolength - 1):
                locations = {
                    'siteName':route,
                    'siteStatus': 'Open',
                    'siteLocation':specs[i],
                    'siteState':'WA',
                    'siteCounty': county,
                    # '_createdOn': datetime.fromtimestamp(os.path.getctime('scraper.py')),
                    '_updatedOn': time.ctime(os.path.getmtime('scraper.py'))
                }
                results.append(locations)
        else:
                
            locations = {
                'siteName':specs[0],
                'siteStatus': 'Open',
                'siteOperation':specs[1],
                'siteState':'WA',
                'siteDistrict': district,
                'siteCounty': county,
                #'_createdOn': time.ctime(os.path.getctime('scraper.py')),
                '_updatedOn': time.ctime(os.path.getmtime('scraper.py'))
            }
            if infolength > 2:
                locations['siteOperation']=specs[2]
                locations['siteAddress']=specs[1]
            results.append(locations)

print(results[65])



with open('washingtonscraper_1.csv', 'w', newline='') as f:
    thewriter = csv.writer(f)

    thewriter.writerow(results)
