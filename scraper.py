#!/usr/bin/python3

import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import os.path, time
import datetime
import csv
import json


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
                    'siteAddress':specs[i],
                    'siteState':'WA',
                    'siteZip': '',
                    'siteCounty': county,
                    'contactPhone': '',
                    'breakfastTime': '',
                    'lunchTime': '',
                    'snackTimeAM': '',
                    'snackTimePM': '',
                    'dinnerSupperTime': '',
                    '_updatedOn': time.ctime(os.path.getmtime('scraper.py')),
                }
                results.append(locations)
        else:

            datetime = specs[1].split('-', 1)
                
            locations = {
                'siteName':specs[0],
                'siteStatus': '',
                'siteOperation':specs[1],
                'siteState':'WA',
                'siteZip': '',
                'siteDistrict': district,
                'siteCounty': county,
                'contactPhone': '',
                'breakfastTime': '',
                'lunchTime': '',
                'snackTimeAM': '',
                'snackTimePM': '',
                'dinnerSupperTime': '',
                '_updatedOn': time.ctime(os.path.getmtime('scraper.py')),
            }
            if infolength > 2:
                locations['siteOperation']=specs[2]
                locations['siteAddress']=specs[1]
            results.append(locations)


print(results[65])

with open('washingtonscraper_1.csv', 'w', newline='') as f:
    thewriter = csv.writer(f)
    thewriter.writerow(results)
