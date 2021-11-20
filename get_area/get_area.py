import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service

import requests as re
import os
import time

exe_path = "./../static/chromedriver"
cities_path = "./../static/cities.csv"

def configure_driver():
    svs = Service(exe_path)
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--headless')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(service=svs, options = options)
    return driver

driver = configure_driver()

xpaths = dict()
xpaths['area'] = '//*[@id="rso"]/div[1]/div/div[1]/div[1]/div[1]/div/div[2]/div/div/div/div[1]'
xpaths['area_wiki'] = '//*[@id="kp-wp-tab-overview"]/div/div/div/div/div/div[2]/div/div/div/span[2]'

error_list = dict()
error_list['url'] = list()

def extract_area(response):
    if "km" not in response: return "", ""
    spl = response.split(" ")
    area = spl[0].replace(",", "")
    return area, "km2"

def extract_element(driver, attribute):
    area, unit = "", ""
    try:
        attr = attribute + '_wiki'
        data = driver.find_element_by_xpath(xpaths[attr]).text
        area, unit = extract_area(data)
    except:
        area, unit = "", ""
    if area != "": return area, unit
    try:
        attr = attribute
        data = driver.find_element_by_xpath(xpaths[attr]).text
        area, unit = extract_area(data)
    except:
        area, unit = "", ""
    return area, unit

def crawl(driver, city, attribute):
    if attribute == 'area':
        urls = [
            'https://www.google.com/search?q=' + city.replace(" ", "+")+
            '+city',
            'https://www.google.com/search?q=' + city.replace(" ", "+")+
            '+surface+area',
            'https://www.google.com/search?q=' + city.replace(" ", "+")+
            '+surface',
            'https://www.google.com/search?q=' + city.replace(" ", "+")+
            '+area',
            'https://www.google.com/search?q=' + city.replace(" ", "+")+
            '+city+area',
            'https://www.google.com/search?q=' + city.replace(" ", "+")+
            '%3A+area'
        ]
    else:
        urls = []
    area, unit = "", ""
    for url in urls:
        try:
            driver.get(url)
            time.sleep(5)
            area, unit = extract_element(driver, attribute)
        except:
            area, unit = "", ""
        if area != "": break
    if area != "": print("Area found at: ", area, "url: ", url)
    return area, unit, url

csv_data = pd.read_csv(cities_path)
new_area = dict() 
new_area['city'], new_area['area'] = list(), list()
new_area['unit'], new_area['url'] = list(), list() 

count, length = 0, len(csv_data['Name'])
for index, c in enumerate(csv_data['Name']):
    count += 1
    # if  count > 10: continue 
    area, unit, url = crawl(driver, c, "area")
    if area == "": error_list['url'].append(url)
    print(count, length, c, area, unit, url)
    new_area['city'].append(c)
    new_area['area'].append(area)
    new_area['unit'].append(unit)
    new_area['url'].append(url)

driver.close()
pd.DataFrame(new_area).to_csv('AllArea.csv')
pd.DataFrame(error_list).to_csv('error_list.csv')

