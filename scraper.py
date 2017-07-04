from os import environ
import csv

from bs4 import BeautifulSoup as bs
import requests
# hack to override sqlite database filename
# see: https://help.morph.io/t/using-python-3-with-morph-scraperwiki-fork/148
environ['SCRAPERWIKI_DATABASE_NAME'] = 'sqlite:///data.sqlite'
import scraperwiki


r = requests.get('http://geonames.nga.mil/namesgaz/')
soup = bs(r.text, 'html.parser')
selects = soup.find(id='divFeatureDesignations').find_all('select')

options = soup.find(id='DesignationCode').find('select', id='lbFeatureClass').find_all('option')
location_categories = [{
    'code': option['value'].replace('\'', ''),
    'name': option.text.split(' (')[0],
} for option in options]

scraperwiki.sqlite.save(['code'], location_categories, 'location_categories')

locations = []
for location_category in location_categories:
    options = soup.find(text=location_category['name']).find_parent('div').find('select').find_all('option')
    locations += [{
        'category': location_category['code'],
        'code': option.text.split(',')[0],
        'name': option.text.split(',')[1],
    } for option in options]

scraperwiki.sqlite.save(['code'], locations, 'locations')
