import math
import csv
import time
import requests
import pandas as pd
from bs4 import BeautifulSoup


def writeFieldNameToFile(file_path=None):
    field_name = []
    field_name.append({'city': 'city', 'gdp': 'gdp', 'year': 'year'})
    df = pd.DataFrame(field_name)
    df.to_csv(file_path, mode="a", header=False, index=False)


def crawl_data(file_path=None):
    writeFieldNameToFile(file_path=file_path)
    url_page = 'https://en.wikipedia.org/wiki/List_of_cities_by_GDP'
    response = requests.get(url_page)
    soup = BeautifulSoup(response.content, "html.parser")

    listS = soup.find('tbody')  # tìm thẻ div có class là gnt_ar_b
    raw_data = listS.find_all('tr')
    items_list = []

    l = len(raw_data)
    # print(raw_data[5])
    # cols = raw_data[5].find_all('td')
    # cols = [x.text.strip() for x in cols]
    # print(cols)
    for i in range(1,l):
        d = {}
        cols = raw_data[i].find_all('td')
        cols = [x.text.strip() for x in cols]
        print(cols)
        d['city'] = cols[1].replace('\"','')
        # print(d['city'])
        start_bracket = cols[4].find('[')
        end_bracket = start_bracket
        if start_bracket == -1:
            end_bracket = len(cols[4])
        string = cols[4][0:end_bracket] 
        # print(string)
        start = string.find('(')
        end = string.find(')')
        if start == -1:
            start = len(string)
            
        d['gdp'] = string.replace(',',"")[0:start].replace(' ',"")
        d['year'] = string[start+1:end].replace(' ',"")
        items_list.append(d)
    df = pd.DataFrame(items_list)
    df.to_csv(file_path, mode="a", header=False, index=False)
    # # print(items_list)

if __name__ == '__main__':
    crawl_data(file_path='./city_gdp.csv')
