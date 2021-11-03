import math
import csv
import time
import requests
import math
import csv
import time
import requests

from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC, wait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.command import Command
# urlpage = "https://www.usatoday.com/story/news/world/2019/07/11/the-50-most-densely-populated-cities-in-the-world/39664259/"
# response = requests.get(urlpage)
# soup = BeautifulSoup(response.content, "html.parser")

# listS = soup.find('div', class_="gnt_ar_b")  # tìm thẻ div có class là gnt_ar_b
# raw_data = listS.find_all('strong')  # tìm bên trong div.gnt_ar_b tất cả thẻ strong

# list_density = {
#     "city": "",
#     "density": ""
# }
# for item in raw_data:
#     print(item)


s = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=s)
driver.set_page_load_timeout(20)
url = "https://breezometer.com/air-quality-map/air-quality"
driver.get(url)

driver.implicitly_wait(10)
# time.sleep(2)

driver.find_element(By.CSS_SELECTOR, ".aq-index-selection > div").click()
driver.find_element(By.CSS_SELECTOR, ".dropdown .body>div:nth-child(2)").click()

driver.find_element(By.CSS_SELECTOR, ".ss-content .mt-4 .search-dropdown >div").click()


# driver.find_element(By.CSS_SELECTOR, ".search-input").clear()
driver.find_element(By.CLASS_NAME, "search-input").send_keys("Hà Nội")
# searhbar = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "search-input")))
# searhbar.send_keys("Hà Nội")
# searhbar._execute(Command.CLEAR_ELEMENT)
# searhbar.sendKeys("Hà Nội")
# element = WebDriverWait(driver, 2).until(
#     EC.presence_of_element_located((By.ID, "vs1__option-1"))
# )

# action = ActionChains(driver)
# action.click(on_element=element)
# action.perform()
time.sleep(1)  # dừng 1 giây để đợi data load tìm kiếm trên web

list_pollutant = {
    "city": "Nam Định",
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
# list_pollutant["dominant_pollutant"] = driver.find_element_by_css_selector(".ss-content .card .dominant-pollutant>p").text

driver.execute_script("document.getElementsByClassName('ss-content')[0].scrollTo(0,2000);")

time.sleep(2)

results = driver.find_elements_by_css_selector(".pollutant-wrapper")

for result in results:
    pollutant = result.find_element_by_css_selector("div.name").text.strip()
    val = result.find_element_by_css_selector("div.concentration-value").text.strip()
    list_pollutant[pollutant] = val

time.sleep(2)

print(list_pollutant)
print("Success")
