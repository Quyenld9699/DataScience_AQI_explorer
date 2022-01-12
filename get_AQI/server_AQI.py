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

# exe_path = '/home/quyenld/Python/DataScience_AQI_explorer/chromedriver_linux64_95/chromedriver'
exe_path2 = "../static/chromedriver_mac"

AQI_data = dict()
AQI_data["city"] = list()
AQI_data["AQI"] = list()
AQI_data["dominant_pollutant"] = list()
AQI_data["O3"] = list()
AQI_data["SO2"] = list()
AQI_data["PM2.5"] = list()
AQI_data["PM10"] = list()
AQI_data["CO"] = list()
AQI_data["NO2"] = list()
AQI_data["NO"] = list()
AQI_data["NOX"] = list()
AQI_data["C6H6"] = list()
AQI_data["NMHC"] = list()

error_list = dict()
error_list['URL'] = list()

# def configure_driver():
#     svs = Service(exe_path2)
#     options = Options()
#     options.add_argument('--no-sandbox')
#     options.add_argument('--headless')
#     options.add_argument('--disable-dev-shm-usage')
#     options.add_argument("--window-size=1920,1080")
#     driver = webdriver.Chrome(service=svs, options=options)
#     return driver


def configure_driver():
    # svs = Service(exe_path2)
    options = Options()
    options.add_argument('--no-sandbox')
    # options.add_argument('--headless')
    # options.add_argument('--disable-dev-shm-usage')
    options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(executable_path=exe_path2, options=options)
    return driver



#def get_api_data(list_city, csv_aqi_file, csv_log_file):
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
            print("1")
            driver.find_elements(By.CLASS_NAME, "search-input")[2].clear() # error here
            print("2")
            driver.find_elements(By.CLASS_NAME, "search-input")[2].send_keys(city_name)
            time.sleep(5)  # wait to load list option
            print("3")

            driver.find_elements(By.CLASS_NAME, "option__title")[1].click()
            print("4")
            time.sleep(5)

            driver.find_element(By.CSS_SELECTOR, ".aq-index-selection > div").click()
            print("5")
            driver.find_element(By.CSS_SELECTOR, ".dropdown .body>div:nth-child(2)").click()
            print("6")
            time.sleep(5)

            list_pollutant = {
                "city": city_name,
                "AQI": "0",
                "dominant_pollutant": "",
                "O3": "0",
                "SO2": "0",
                "PM2.5": "0",
                "PM10": "0",
                "CO": "0",
                "NO2": "0",
                "NO": "0",
                "NOX": "0",
                "C6H6": "0",
                "NMHC": "0"
            }
            list_pollutant["AQI"] = driver.find_element_by_css_selector(".ss-content .current-aqi .aqi").text
            list_pollutant["dominant_pollutant"] = driver.find_element_by_css_selector(".ss-content .dominant-pollutant>p").text

            driver.execute_script("document.getElementsByClassName('ss-content')[0].scrollTo(0,2000);")

            time.sleep(3)

            results = driver.find_elements_by_css_selector(".pollutant-wrapper")

            for result in results:
                pollutant = result.find_element_by_css_selector("div.name").text.strip()
                val = result.find_element_by_css_selector("div.concentration-value").text.strip()
                list_pollutant[pollutant] = val

            time.sleep(1)

            for k in list_pollutant.keys():
                AQI_data[key].append(list_pollutant[key])
            print(list_pollutant)

            # AQI_data["city"].append(list_pollutant["city"])
            # AQI_data["AQI"].append(list_pollutant["AQI"])
            # AQI_data["dominant_pollutant"].append(list_pollutant["dominant_pollutant"])
            # AQI_data["O4"].append(list_pollutant["O3"])
            # AQI_data["SO2"].append(list_pollutant["SO2"])
            # AQI_data["PM2.5"].append(list_pollutant["PM2.5"])
            # AQI_data["PM10"].append(list_pollutant["PM10"])
            # AQI_data["CO"].append(list_pollutant["CO"])
            # AQI_data["NO2"].append(list_pollutant["NO2"])
            # AQI_data["NO"].append(list_pollutant["NO"])
            # AQI_data["NOX"].append(list_pollutant["NOX"])
            # AQI_data["C6H6"].append(list_pollutant["C6H6"])
            # AQI_data["NMHC"].append(list_pollutant["NMHC"])

           #  csv_aqi_file.writerow([list_pollutant["city"],
           #                         list_pollutant["AQI"],
           #                         list_pollutant["dominant_pollutant"],
           #                         list_pollutant["O3"],
           #                         list_pollutant["SO2"],
           #                         list_pollutant["PM2.5"],
           #                         list_pollutant["PM10"],
           #                         list_pollutant["CO"],
           #                         list_pollutant["NO2"],
           #                         list_pollutant["NO"],
           #                         list_pollutant["NOX"],
           #                         list_pollutant["C6H6"],
           #                         list_pollutant["NMHC"]])
            # print(list_pollutant)
            print("Success, time: ", time.time() - start)

            driver.execute_script("document.getElementsByClassName('ss-content')[0].scrollTo(0,40);")

        except:
            print("Không tìm thấy data", city_name)
            error_list['URL'].append(city_name)
            # csv_log_file.writerow([city_name])

    driver.quit()


def get_prefix():
    t = time.localtime()
    return time.strftime("%Hh-%Mm-%h-%d-%Y", t)


def open_files(prefix):
    aqi_file = "./CSV_file_data/" + prefix + ".csv"
    log_file = "./log_data/" + prefix + ".csv"
    aqi_data = csv.writer(open(aqi_file, "w", encoding='utf-8'))
    log_data = csv.writer(open(log_file, "w", encoding='utf-8'))
    column = ["city", "AQI", "dominant pollutant", "O3", "SO2", "PM2.5", "PM10", "CO", "NO2", "NO", "NOX", "C6H6", "NMHC"]
    not_found = ["city not found data"]
    aqi_data.writerow(column)
    log_data.writerow(not_found)
    return aqi_data, log_data

def save_data(prefix):
    aqi_file = "./CSV_file_data/" + prefix + ".csv"
    log_file = "./log_data/" + prefix + ".csv"
    pd.DataFrame(AQI_data).to_csv(aqi_file)
    pd.DataFrame(error_list).to_csv(log_file)


def main():
    cities_csv = pd.read_csv("./../static/cities.csv")
    cities = cities_csv['Name']
    cities = cities[0:10]
    current_time = get_prefix()

    num_thread = 2
    length = int(len(cities)/num_thread)
    threads = list()
    for i in range(num_thread):
        data = cities[i*length:(i+1)*length]
        t = threading.Thread(target=get_api_data, args=(data, 0))
        threads.append(t)

    begin = time.time()
    for th in threads: th.start()
    for th in threads: th.join()

    print("THREAD FINISHED", num_thread, time.time() - begin, current_time)
    save_data(current_time)

    #for num_thread in [2]:
     #   current_time = get_prefix()
      #  file_aqi_data, file_log_data = open_files(current_time)
        # num_thread = 2
        # 4 thread: 166 seconds
        # 2 thread: 139 seconds
        # 2 process: 137
       # length = int(len(cities)/num_thread)
        #threads = list()
        #for i in range(num_thread):
         #   data = cities[i*length:(i+1)*length]
            # t = threading.Thread(target=get_api_data, args=(data,file_aqi_data, file_log_data))
          #  t = multiprocessing.Process(target=get_api_data, args=(data, file_aqi_data, file_log_data))
           # threads.append(t)

       # begin = time.time()
        #for th in threads: th.start()
        #for th in threads: th.join()

       # print("PROCESS FINISHED", num_thread, time.time() - begin, current_time)

    # cities = ["Hà Nội", "Nam Định", "Bắc Giang", "New York", "England"]
    # get_api_data(cities[12:50], file_aqi_data, file_log_data)

    return


main()
