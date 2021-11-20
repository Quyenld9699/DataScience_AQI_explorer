import math
import csv
import time
import requests

from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

from selenium.common.exceptions import TimeoutException, NoSuchElementException

exe_path = '/home/quyenld/Python/DataScience_AQI_explorer/chromedriver_linux64_95/chromedriver'
exe_path2 = "/home/ds_project/DataScience_AQI_explorer/chromedriver_linux64_96/chromedriver"


def get_api_data(list_city, csv_file):
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(executable_path=exe_path2, options=options)
    driver.set_page_load_timeout(30)
    url = "https://breezometer.com/air-quality-map/air-quality"
    driver.get(url)
    driver.maximize_window()
    driver.implicitly_wait(30)

    try:
        driver.find_element(By.XPATH, './/*[contains(concat(" ",normalize-space(@class)," ")," aq-index-selection ")]/div').click()
        xPath = './/*[contains(concat(" ",normalize-space(@class)," ")," dropdown ")]//*[contains(concat(" ",normalize-space(@class)," ")," body ")]/div[(count(preceding-sibling::*)+1) = 2]'
        driver.find_element(By.XPATH, xPath).click()

        for city_name in list_city:
            xPath = './/*[contains(concat(" ",normalize-space(@class)," ")," ss-content ")]//*[contains(concat(" ",normalize-space(@class)," ")," mt-4 ")]//*[contains(concat(" ",normalize-space(@class)," ")," search-dropdown ")]/div'
            driver.find_element(By.XPATH, xPath).click()
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
            xPath = './/*[contains(concat(" ",normalize-space(@class)," ")," ss-content ")]//*[contains(concat(" ",normalize-space(@class)," ")," current-aqi ")]//*[contains(concat(" ",normalize-space(@class)," ")," aqi ")]'
            list_pollutant["AQI"] = driver.find_element(By.XPATH, xPath).text

            xPath = './/*[contains(concat(" ",normalize-space(@class)," ")," ss-content ")]//*[contains(concat(" ",normalize-space(@class)," ")," dominant-pollutant ")]/p'
            list_pollutant["dominant_pollutant"] = driver.find_element(By.XPATH, xPath).text

            driver.execute_script("document.getElementsByClassName('ss-content')[0].scrollTo(0,2000);")

            time.sleep(2)

            results = driver.find_elements(By.XPATH, './/*[contains(concat(" ",normalize-space(@class)," ")," pollutant-wrapper ")]')

            for result in results:
                pollutant = result.find_element(By.XPATH, './/div[contains(concat(" ",normalize-space(@class)," ")," name ")]').text.strip()
                val = result.find_element(By.XPATH, './/div[contains(concat(" ",normalize-space(@class)," ")," concentration-value ")]').text.strip()
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

    except NoSuchElementException:
        print("Lỗi không tìm thấy phần tử")
    except TimeoutException:
        print("Lỗi Timeout")
    finally:
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
