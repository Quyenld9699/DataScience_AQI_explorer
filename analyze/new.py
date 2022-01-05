import pandas as pd
import numpy as np
# Read AQ
def average_AQI(file=''):
    df = pd.read_csv(file)
    # df = df[['city','AQI']]
    df_result = df.groupby('city').mean()
    return df_result

df_aqi = average_AQI('../ProcessedAQI/Final/aqi.csv')
import pandasql as ps
def population_area(population_path='',area_path=''):
    df_population = pd.read_csv(population_path)
    df_population = df_population[['Name','Population','Country']].drop_duplicates()
    df_area = pd.read_csv(area_path)
    df_area = df_area[['city','area']].drop_duplicates()
    # print(len(df_area))
    # print(len(df_population['Name'].unique()))
    for index,row in df_area.iterrows():
        row['area'] = row['area'].replace('.','')
        # print(row['area'])
    sql1 = "SELECT df_area.city,df_population.population,df_population.Country,df_area.area, df_population.population*1.0/df_area.area as density FROM df_area,df_population  WHERE df_area.city == df_population.Name"
    df_result = ps.sqldf(sql1,locals())
    return df_result

df_density = population_area('../data/population.csv','../data/area.csv')
df_density = df_density.drop_duplicates()
print(len(df_density['city'].unique()))
sql = 'SELECT df_aqi.city,AQI,Population,Country,area,density FROM df_aqi,df_density WHERE df_aqi.city = df_density.city'
df2 = ps.sqldf(sql,locals())
df2 = df2.drop_duplicates(subset='city', keep="first")

df_gdp= pd.read_csv('../get_gdp/city_gdp.csv')
# df_gdp = df_temperature[['city','country','oct','nov','dec']]
df_gdp = df_gdp.dropna()
df_gdp = df_gdp.drop([408,409])
from unidecode import unidecode
def remove_non_ascii(text):
    return unidecode(unidecode(text))
import re
def format_ascii_string(input=''):
    output = re.sub(r'[^\x00-\x7f]',' ', input)
    return output


df_gdp['city'] = df_gdp['city'].map(lambda x: remove_non_ascii(x))
# Convert Datatype of Temperature to Float
df_gdp['gdp'] = df_gdp['gdp'].map(lambda x: float(x))

sql2 = 'SELECT df2.city,AQI,Population,Country,area,density,df_gdp.gdp FROM df2,df_gdp WHERE df2.city = df_gdp.city'
df3 = ps.sqldf(sql2,locals())
from sklearn.preprocessing import StandardScaler,MinMaxScaler
df1 = df3.copy()
# df2[['AQI','density']] = StandardScaler().fit_transform(df2[['AQI', 'density']])
df1[['AQI','density','gdp']] = MinMaxScaler().fit_transform(df1[['AQI', 'Population','gdp']])
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from mpl_toolkits.mplot3d import Axes3D


# plt.show()
from sklearn.cluster import KMeans

X = df1[['AQI','Population','gdp']]
X = X.to_numpy(dtype=float)
X
kmean = KMeans(6,random_state=100).fit(X)

# c=kmean.labels_.astype(float)
fig = plt.figure()
fig = plt.figure(figsize = (12, 8), dpi=80)
ax = fig.add_subplot(111, projection='3d')
pnt3d = ax.scatter3D(df3['AQI'],df3 ['Population'], df3['gdp'],c=kmean.labels_.astype(float))
cbar=plt.colorbar(pnt3d)
cbar.set_label("Grinding Volume (cm3)")
fig.set_facecolor('white')
ax.set_facecolor('white')
# plt.xticks(np.arange(2018, 2021, 1))
# plt.yticks(np.arange(1,3,1))
ax.set_xlabel('AQI')
ax.set_ylabel('Population')
ax.set_zlabel('gdp')
plt.show()