# Use this file to Format the name of the city in the GDP table

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re

df_gdp= pd.read_csv('../get_gdp/city_gdp.csv')
# df_gdp = df_temperature[['city','country','oct','nov','dec']]
print(df_gdp)
print(df_gdp.dtypes)
# df_gdp = df_gdp.dropna()
df_gdp = df_gdp.drop([408,409])


from unidecode import unidecode
def remove_non_ascii(text):
    return unidecode(unidecode(text))


def format_ascii_string(input=''):
    output = re.sub(r'[^\x00-\x7f]',' ', input)
    return output

def select_first_string(input=''):
    location = input.find(',')
    if location!=-1:
        out_string = input[0:location]
    else:
        out_string = input
    return out_string

df_gdp['city'] = df_gdp['city'].map(lambda x: remove_non_ascii(x))
df_gdp['city'] = df_gdp['city'].map(lambda x: select_first_string(x))
# Convert Datatype of Temperature to Float
df_gdp['gdp'] = df_gdp['gdp'].map(lambda x: float(x))


df_gdp.to_csv('./formated_gdp.csv')