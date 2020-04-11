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
                skip = ['Yellow Camp (1', '1:30 – 11:45 AM)']
                if specs[i] in skip:
                    continue
                specs[i] = specs[i].strip(')')
                specs[i] = specs[i].split('(')
                locations = {
                    'siteName':route,
                    'siteStatus': '',
                    'siteAddress':specs[i][0],
                    'siteState':'WA',
                    'siteZip': '',
                    'siteCounty': county,
                    'contactPhone': '',
                    'startDate': '',
                    'endDate': '',
                    'daysofOperation': '',
                    'siteTime': specs[i][1],
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
                'siteState':'WA',
                'siteZip': '',
                'siteDistrict': district,
                'siteCounty': county,
                'contactPhone': '',
                'startDate': '',
                'endDate': '',
                'daysofOperation': '',
                'siteTime':specs[1],
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

#Manually fixing mutliple specific entries due to inconsistent formatting between entries

# print([element for element in results if element['siteName'] == 'The Boys and Girls Club will be delivering meals to the following locations:'])

for entry in results:
    if entry['siteName'] == 'The Boys and Girls Club will be delivering meals to the following locations:':
        results.remove(entry)
    if entry['siteName'] == 'Mansfield School':
        entry['contactPhone'] = '509-683-1012'
        entry['siteTime'] = 'Contact for times'
        entry['siteAddress'] = ''
        entry['breakfastTime'] = 'Serving, Contact for time'
        entry['lunchTime'] = 'Serving, Contact for time'
    if entry['siteName'] == 'Orchard Middle School':
        entry['siteTime'] = ''
        entry['siteAddress'] = '1024 Orchard Ave, Wenatchee'
    if entry['siteName'] == 'Keller School':
        entry['contactPhone'] = '509-634-4325'
        entry['siteTime'] = 'Delivery, Contact to be added to list.'
        entry['startDate'] = '03/23/2020'
        entry['siteAddress'] = ''
    if entry['siteName'] == 'Mansfield School':
        entry['contactPhone'] = '509-684-6873'
        entry['siteTime'] = 'Delivery, Contact to be added to list.'
        entry['siteAddress'] = ''
    if entry['siteName'] == 'North River':
        results.remove(entry)
    if entry['siteName'] == 'Black Diamond Elementary ***Starting Wednesday, 3/18':
        entry['startDate'] = '03/18/2020'
        entry['siteName'] = 'Black Diamond Elementary'
    if entry['siteName'] == 'Enumclaw High School ***Starting Wednesday, 3/18':
        entry['startDate'] = '03/18/2020'
        entry['siteName'] = 'Enumclaw High School'
    if entry['siteName'] == 'Enumclaw King County Library ***Starting Wednesday, 3/18':
        entry['startDate'] = '03/18/2020'
        entry['siteName'] = 'Enumclaw King County Library'
    if entry['siteName'] == 'Mercer Island School District students':
        entry['siteAddress'] = 'Mercer Island High School and Islander Middle School'
        entry['lunchTime'] = 'Serving pre-order meals, visit district page for more info'
        entry['siteTime'] = 'Visit district page for more info'
        entry['siteAddress'] = 'Pickup at 33 locations, visit district page'
    if entry['siteName'] == 'Northshore School District students':
        entry['contactPhone'] = 'Northshore School District students'
        entry['siteTime'] = 'Serving pre-rder meals, visit district page for more info'
    if entry['siteName'] == 'Riverview School District students':
        entry['siteTime'] = 'Serving pre-rder meals, visit district page for more info'
        entry['siteAddress'] = 'Cherry Valley Elementary and Carnation Elementary'
    if entry['siteName'] == 'Snoqualmie Valley School District students':
        entry['siteTime'] = 'Serving pre-rder meals for Snoqualmie Valley School District students, details to come'
        entry['siteAddress'] = 'Details to come'
        entry['startDate'] = '03/18/2020'
    if entry['siteName'] == 'Vashon Island School District students':
        entry['siteTime'] = 'Serving pre-rder meals for Vashon Island students students, details to come'
        entry['siteAddress'] = 'Details to come'
        entry['startDate'] = '03/16/2020'
    if entry['siteName'] == 'McMicken Hts Park ***Starting Tuesday, 3/17':
        entry['siteName'] = 'McMicken Hts Park'
        entry['startDate'] = '03/17/2020'
    if entry['siteName'] == 'Pine Ridge Apts ***Starting Tuesday, 3/17':
        entry['startDate'] = '03/17/2020'
        entry['siteName'] = 'Pine Ridge Apts'
    if entry['siteName'] == 'Windsor Heights Apt ***Starting Tuesday, 3/17':
        entry['startDate'] = '03/17/2020'
        entry['siteName'] = 'Windsor Heights Apt'
    if entry['siteName'] == 'Northwest School Sites':
        entry['siteAddress'] = 'Ballard High School, 1418 NW 65th St Seattle, WA 98117'
    if entry['siteName'] == 'Tukwila School District AM Bus Stops':
        results.remove(entry)
    if entry['siteName'] == 'Morton Jr/Sr High School':
        entry['siteTime'] = 'Contact district'
        entry['siteAddress'] = '152 Westlake Ave, Morton'
        entry['contactPhone'] = '360-496-5300'
    if entry['siteName'] == 'Morton Elementary School':
        entry['siteTime'] = 'Contact District'
        entry['siteAddress'] = '400 W Main Ave, Morton'
        entry['contactPhone'] =	'360-496-5300'
    if entry['siteName'] == 'Breezeway picnic tables (near big gym)':
        entry['daysofOperation'] = 'M, T, W, Th, F'
    if entry['siteName'] == 'Doty General Store':
        entry['daysofOperation'] = 'M, T, W, Th, F'
    if entry['siteName'] == 'Almira Lion’s Club Park':
        entry['contactPhone'] = '509-639-2414 - call for delivery requests + more information'
    if entry['siteName'] == 'Fife School District Bus Stops':
        results.remove(entry)
    if entry['siteName'] == 'Faith Lutheran Church':
        entry['daysofOperation'] = 'M, T, W, Th, F'
        entry['siteTime'] = '9:00AM-10:00AM'
        entry['siteAddress'] = '1424 172nd St NE, Marysville'
    if entry['siteName'] == 'Reclamation Church':
        entry['daysofOperation'] = 'M, T, W, Th, F'
        entry['siteTime'] = '9:00AM-10:00AM'
        entry['siteAddress'] = '907 Lakewood Rd, Arlington'
    if entry['siteName'] == 'Jake’s House':
        entry['daysofOperation'] = 'M, T, W, Th, F'
        entry['siteTime'] = '9:00AM-10:00AM'
        entry['siteAddress'] = '18824 Smokey Point Blvd Suite 105, Arlington'
    if entry['siteName'] == 'Smokey Point Community Church':
        entry['daysofOperation'] = 'M, T, W, Th, F'
        entry['siteTime'] = '9:00AM-10:00AM'
        entry['siteAddress'] = '17721 Smokey Point Blvd, Arlington'
    if entry['siteName'] == 'Reverse the Baker Bus':
        entry['daysofOperation'] = 'T, F'
        entry['siteTime'] = '10:00AM-12:00PM'
        entry['siteAddress'] = 'Morning routine elementary bus routes'
        

results.append(
    {
                'siteName':'ROUTE 3:',
                'siteStatus': '',
                'siteOperation': '',
                'siteState':'WA',
                'siteZip': '',
                'siteDistrict': '',
                'siteCounty': 'Adams County',
                'contactPhone': '',
                'siteTime': '11:30 - 11:45 AM',
                'breakfastTime': '',
                'lunchTime': '',
                'snackTimeAM': '',
                'snackTimePM': '',
                'dinnerSupperTime': '',
                '_updatedOn': time.ctime(os.path.getmtime('scraper.py')),
    }
)


def create_csv(results):
    fieldnames = []

    for fields in results[0].keys():
        fieldnames.append(fields)

    with open('washington_1.csv', 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(results)


create_csv(results)
