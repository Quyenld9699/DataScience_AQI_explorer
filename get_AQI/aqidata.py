import math
import csv
import time
import requests
import threading
import multiprocessing

from bs4 import BeautifulSoup
import pandas as pd

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException, NoSuchElementException

exe_path = '/home/quyenld/Python/DataScience_AQI_explorer/chromedriver_linux64_95/chromedriver'
exe_path2 = "../static/chromedriver"

server_name = "1"

AQI_data = dict()
keys = ["city","AQI", "dominant_pollutant", "O3", "SO2", "PM2.5", "PM10", "CO", "NO2", "NO","NOX", "C6H6", "NMHC"]
for key in keys:
    AQI_data[key] = list()

error_list = dict()
error_list['URL'] = list()

def configure_driver():
    svs = Service(exe_path2)
    options = Options()
    options.headless = True
    # options.add_argument('--no-sandbox')
    # options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(service=svs, options=options)
    return driver
    # svs = Service(exe_path2)
    # options = Options()
    # options.add_argument('--no-sandbox')
    # options.add_argument('--headless')
    # options.add_argument('--disable-dev-shm-usage')
    # options.add_argument("--window-size=1920,1080")
    # driver = webdriver.Chrome(service=svs, options=options)
    # return driver


def get_api_data(list_city, sth):
    # driver = webdriver.Chrome(executable_path=ChromeDriverManager().install())
    driver = configure_driver()
    driver.set_page_load_timeout(20)
    url = "https://breezometer.com/air-quality-map/air-quality"
    driver.get(url)
    driver.implicitly_wait(20)

    for city_name in list_city:
        try:
            start = time.time()
            driver.find_element(By.CSS_SELECTOR, ".ss-content .mt-4 .search-dropdown >div").click()
            driver.find_elements(By.CLASS_NAME, "search-input")[2].clear()
            driver.find_elements(By.CLASS_NAME, "search-input")[2].send_keys(city_name)
            time.sleep(1)  # wait to load list option

            driver.find_elements(By.CLASS_NAME, "option__title")[1].click()
            time.sleep(1.5)

            driver.find_element(By.CSS_SELECTOR, ".aq-index-selection > div").click()
            driver.find_element(By.CSS_SELECTOR, ".dropdown .body>div:nth-child(2)").click()
            time.sleep(1)
            
            list_pollutant = {}
            for key in keys:
                list_pollutant[key] = "0"
            list_pollutant["dominant_pollutant"] = ""
            list_pollutant["city"] = city_name

            list_pollutant["AQI"] = driver.find_element(By.CSS_SELECTOR, ".ss-content .current-aqi .aqi").text
            list_pollutant["dominant_pollutant"] = driver.find_element(By.CSS_SELECTOR, ".ss-content .dominant-pollutant>p").text

            driver.execute_script("document.getElementsByClassName('ss-content')[0].scrollTo(0,2000);")

            time.sleep(1)

            results = driver.find_elements(By.CSS_SELECTOR, ".pollutant-wrapper")

            for result in results:
                pollutant = result.find_element(By.CSS_SELECTOR, "div.name").text.strip()
                val = result.find_element(By.CSS_SELECTOR, "div.concentration-value").text.strip()
                list_pollutant[pollutant] = val

            time.sleep(0.5)

            for key in keys:
                AQI_data[key].append(list_pollutant[key])

            print(list_pollutant)
            print("Success, time: ", time.time() - start)

            driver.execute_script("document.getElementsByClassName('ss-content')[0].scrollTo(0,40);")

        except:
            print("Kh??ng t??m th???y data", city_name)
            error_list['URL'].append(city_name)

    driver.quit()


def get_prefix():
    t = time.time() * 1000
    return str(int(t))


# def open_files(prefix):
#     aqi_file = "./CSV_file_data/" + prefix + ".csv"
#     log_file = "./log_data/" + prefix + ".csv"
#     aqi_data = csv.writer(open(aqi_file, "w", encoding='utf-8'))
#     log_data = csv.writer(open(log_file, "w", encoding='utf-8'))
#     column = ["city", "AQI", "dominant pollutant", "O3", "SO2", "PM2.5", "PM10", "CO", "NO2", "NO", "NOX", "C6H6", "NMHC"]
#     not_found = ["city not found data"]
#     aqi_data.writerow(column)
#     log_data.writerow(not_found)
#     return aqi_data, log_data

def save_data(prefix):
    aqi_file = "./CSV_file_data_" + server_name + "/" + prefix + ".csv"
    log_file = "./log_data_/" + server_name + "/" + prefix + ".csv"
    pd.DataFrame(AQI_data).to_csv(aqi_file)
    pd.DataFrame(error_list).to_csv(log_file)


def main():
    cities_csv = pd.read_csv("./../static/population_" + server_name + ".csv")
    cities = cities_csv['Name']
    current_time = get_prefix()
    begin = time.time()
    get_api_data(cities, 0)

    # num_thread = 4
    # length = int(len(cities)/num_thread)
    # threads = list()
    # print(len(cities))
    # for i in range(num_thread):
    #     if i+1 == num_thread : data = cities[i*length:]
    #     else : data = cities[i*length:(i+1)*length]
    #     print(len(data))
    #     t = threading.Thread(target=get_api_data, args=(data, 0))
    #     threads.append(t)

    # for th in threads: th.start()
    # for th in threads: th.join()

    print("THREAD FINISHED",  time.time() - begin, current_time)
    save_data(current_time)

    return


main()
