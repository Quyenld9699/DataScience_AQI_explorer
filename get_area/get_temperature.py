import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

import requests as re
import os
import time

# please run on linux environment
exe_path = "../static/chromedriver_linux"

popu = pd.read_csv("../data/population.csv")
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

def get_response(url):
    response = re.get(url)
    return response.text

# def configure_driver():
#     svs = Service(exe_path)
#     options = Options()
#     options.add_argument('--no-sandbox')
#     options.add_argument('--headless')
#     options.add_argument('--disable-dev-shm-usage')
#     options.add_argument("--window-size=1920,1080")
#     #driver = webdriver.Chrome(executable_path=exe_path, options = options)
#     driver = webdriver.Chrome(service=svs, options=options)
#     return configure_driver

def configure_driver():
    svs = Service(exe_path)
    options = Options()
    options.headless = True
    options.add_argument('--no-sandbox')
    # options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(service=svs, options=options)
    return driver

driver = configure_driver()

def get_static(url):
    res = get_response(url)
    temp = [res.split("Mean Temp")[i+1].split("&nbsp")[0].split("</span>")[-1].strip() for i in range(13)]
    temp2 = temp[1:]
    temp2.append(temp[0])
    return temp2

def get_dynamic(driver, country, city):
    url = "https://www.timeanddate.com/weather"
    driver.get(url)
    driver.implicitly_wait(2)

    driver.find_element_by_xpath("/html/body/div[6]/header/div[2]/div/form/input").send_keys(country + " " + city)
    time.sleep(0.3)  # wait to load list option
    driver.find_elements(By.CLASS_NAME, "ash")[0].click()
    time.sleep(1)
    return driver.current_url + "/climate"


def get_temp(driver, country, city):
    url = "https://www.timeanddate.com/weather/" + country.lower() + "/" + city.lower() +"/climate"
    if len(country.split(" ")) >= 2 or len(city.split(" ")) >= 2:
        url = get_dynamic(driver, country, city)
    return get_static(url)


def init_temp():
    temp_data = dict()
    temp_data['city'] = list()
    temp_data['Temp_avg'] = list()
    for m in months: temp_data[m] = list()
    return temp_data

temp_data = init_temp()
null_data = [""]*13

for index in range(popu.shape[0]):
    row = popu.iloc[index]

    try:
        temp = get_temp(driver, row['Country'], row['Name'])
        print(row['Country'], row['Name'], temp)
    except:
        print("EXCEPT at ", index, row['Name'], row['Country'])
        temp = null_data

    temp_data['city'].append(row['Name'])
    for i in range(12):
        temp_data[months[i]].append(temp[i])
    temp_data['Temp_avg'].append(temp[12])

pd.DataFrame(temp_data).to_csv("temperature.csv")

driver.quit()


