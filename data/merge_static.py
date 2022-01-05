import pandas as pd
import numpy as np


temp = pd.read_csv("temperature.csv")
area = pd.read_csv("area.csv")
gdp = pd.read_csv("formated_gdp.csv")
popu = pd.read_csv("population.csv")
vehi = pd.read_csv("vehicle-density.csv")
merged = popu.copy()
merged.rename(columns = {'Name':'City'}, inplace = True)

print("PREPARE COLUMNS")
merged["Area"] = [""]*merged.shape[0]
merged["GDP"] = [""]*merged.shape[0]
merged["Traffic_Index"] = [""]*merged.shape[0]
merged["CO2_Emission_Index"] = [""]*merged.shape[0]

months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
for m in months:
    merged["Temp_" + m] = [""]*merged.shape[0]
merged["Temp_Avg"] = [""]*merged.shape[0]

print("MERGING")
     # merge area to merged
for i in range(area.shape[0]):
    row = area.iloc[i]
    merged["Area"] = np.where(merged['City'].str.lower() == row['city'].lower(), row["area"], merged["Area"])
    
    # merge GDP to merged
for i in range(gdp.shape[0]):
    row = gdp.iloc[i]
    merged["GDP"] = np.where(merged['City'].str.lower() == row['city'].lower(), row["gdp"], merged["GDP"])

for i in range(vehi.shape[0]):
    row = vehi.iloc[i]
    merged["Traffic_Index"] = np.where(merged['Country'].str.lower() == row['country'].lower(), row["traffic index"], merged["Traffic_Index"])
    merged["CO2_Emission_Index"] = np.where(merged['Country'].str.lower() == row['country'].lower(), row["co2 emission index"], merged["CO2_Emission_Index"])

    # merge temp to merged
for i in range(temp.shape[0]):

    row = temp.iloc[i]
    for m in months:
        merged["Temp_" + m] = np.where(merged['City'].str.lower() == row['city'].lower(), row[m], merged["Temp_" + m])
    merged["Temp_Avg"] = np.where(merged['City'].str.lower() == row['city'].lower(), row["Temp_avg"], merged["Temp_Avg"])


pd.DataFrame(merged).to_csv("Merge_static.csv")

print("MERGE FINISHED")

