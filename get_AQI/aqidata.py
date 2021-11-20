import math
import csv
import time
import requests

from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


exe_path = "./../driver/chromedriver"

def get_api_data(list_city, csv_file):
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(exe_path,options=chrome_options)
    driver.set_page_load_timeout(15)
    url = "https://breezometer.com/air-quality-map/air-quality"
    driver.get(url)
    driver.implicitly_wait(15)

    driver.find_element(By.CSS_SELECTOR, ".aq-index-selection > div").click()
    driver.find_element(By.CSS_SELECTOR, ".dropdown .body>div:nth-child(2)").click()

    for city_name in list_city:

        driver.find_element(By.CSS_SELECTOR, ".ss-content .mt-4 .search-dropdown >div").click()
        driver.find_elements(By.CLASS_NAME, "search-input")[2].clear()
        driver.find_elements(By.CLASS_NAME, "search-input")[2].send_keys(city_name)

        time.sleep(2)
        driver.find_elements(By.CLASS_NAME, "option__title")[1].click()

        time.sleep(1)
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

        time.sleep(2)

        results = driver.find_elements_by_css_selector(".pollutant-wrapper")

        for result in results:
            pollutant = result.find_element_by_css_selector("div.name").text.strip()
            val = result.find_element_by_css_selector("div.concentration-value").text.strip()
            list_pollutant[pollutant] = val

        time.sleep(1)
        csv_file.writerow([list_pollutant["city"],
                           list_pollutant["AQI"],
                           list_pollutant["dominant_pollutant"],
                           list_pollutant["O3"],
                           list_pollutant["SO2"],
                           list_pollutant["PM2.5"],
                           list_pollutant["PM10"],
                           list_pollutant["CO"],
                           list_pollutant["NO2"],
                           list_pollutant["NO"],
                           list_pollutant["NOX"],
                           list_pollutant["C6H6"],
                           list_pollutant["NMHC"]])
        print(list_pollutant)
        print("Success")
        driver.execute_script("document.getElementsByClassName('ss-content')[0].scrollTo(0,50);")

    driver.quit()


def main():
    t = time.localtime()
    current_time = time.strftime("%Hh-%Mm-%Ss-%h-%d-%Y", t)
    new_file_name = "./CSV_file_data/" + current_time + ".csv"
    file_data = csv.writer(open(new_file_name, "w", encoding='utf-8'))

    column = ["city", "AQI", "dominant pollutant", "O3", "SO2", "PM2.5", "PM10", "CO", "NO2", "NO", "NOX", "C6H6", "NMHC"]
    file_data.writerow(column)

    get_api_data(["Hà Nội", "Nam Định", "Bắc Giang", "New York"], file_data)

    return


main()
