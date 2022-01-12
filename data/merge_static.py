import pandas as pd
import numpy as np


dynamic = pd.read_csv("./aqi_all.csv")
area = pd.read_csv("./area.csv")
rank = pd.read_csv("./country_gdp.csv")
gdp = pd.read_csv("./formated_gdp.csv")
popu = pd.read_csv("./population.csv")
temp = pd.read_csv("./temperature.csv")
vehi = pd.read_csv("./vehicle-density.csv")

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
merged["GDP_Per_Capita"] = [""]*merged.shape[0]

print("MERGING")
     # merge area to merged
print("MERGING AREA")
for i in range(area.shape[0]):
    row = area.iloc[i]
    merged["Area"] = np.where(merged['City'].str.lower() == row['city'].lower(), row["area"], merged["Area"])
    
    # merge GDP to merged
print("MERGING GDP")
for i in range(gdp.shape[0]):
    row = gdp.iloc[i]
    merged["GDP"] = np.where(merged['City'].str.lower() == row['city'].lower(), row["gdp"], merged["GDP"])

print("MERGING VEHICLE DENSITY")
for i in range(vehi.shape[0]):
    row = vehi.iloc[i]
    merged["Traffic_Index"] = np.where(merged['Country'].str.lower() == row['country'].lower(), row["traffic index"], merged["Traffic_Index"])
    merged["CO2_Emission_Index"] = np.where(merged['Country'].str.lower() == row['country'].lower(), row["co2 emission index"], merged["CO2_Emission_Index"])

    # merge temp to merged
print("MERGING TEMPERATURE")

for i in range(temp.shape[0]):
    row = temp.iloc[i]
    for m in months:
        merged["Temp_" + m] = np.where(merged['City'].str.lower() == row['city'].lower(), row[m], merged["Temp_" + m])
    merged["Temp_Avg"] = np.where(merged['City'].str.lower() == row['city'].lower(), row["Temp_avg"], merged["Temp_Avg"])

print("MERGING GDP RANK")
for i in range(rank.shape[0]):
    row = rank.iloc[i]
    merged["GDP_Per_Capita"] = np.where(merged['Country'].str.lower() == row['country'].lower(), row["gdpPerCapita"], merged["GDP_Per_Capita"])


# MERGE DYNAMIC DATA
print("MERGING AQI DATA (ONLY AVERAGE)")
indices = ['AQI', 'O3', 'SO2', 'PM2.5', 'PM10', 'CO', 'NO2', 'NO', 'NOX', 'C6H6', 'NMHC']
for ind in indices:
    merged[ind + '_Avg'] = [""]*merged.shape[0]
for i in range(merged.shape[0]):
    row = merged.iloc[i]
    for ind in indices:
        mean = dynamic[dynamic['city'].str.lower() == row['City'].lower()][ind].mean()
        merged[ind + '_Avg'] = np.where(merged['City'].str.lower() == row['City'].lower(), mean, merged[ind + '_Avg'])
#    if i > 2: break

print("MERGING GDP PER CAPITA")
merged["GDP_Per_Capita"] = [""]*merged.shape[0]
for i in range(rank.shape[0]):
    row = rank.iloc[i]
    merged["GDP_Per_Capita"] = np.where(merged['Country'].str.lower() == row['country'].lower(), row["gdpPerCapita"], merged["GDP_Per_Capita"])


# MERGE DOMINANT POLLUTANT
print("MERGING DOMINANT POLLUTANT")
merged['dominant_pollutant'] = [""]*merged.shape[0]
for i in range(merged.shape[0]):
    row = merged.iloc[i]
    domin = dynamic[dynamic['city'] == row['City']]['dominant_pollutant']
    if len(domin) != 0:
        try:
            merged["dominant_pollutant"] = np.where(merged['City'].str.lower() == row['City'].lower(), domin.mode(), merged["dominant_pollutant"])
        except Exception as e: 
            print(e)


# MIN AQI AND MAX AQI
merged['AQI_Max'] = [""]*merged.shape[0]
merged['AQI_Min'] = [""]*merged.shape[0]
# rows  = dynamic[dynamic['city'].str.lower() == "Tokyo".lower()]['AQI']#.max()
for i in range(merged.shape[0]):
    row = merged.iloc[i]
    rows = dynamic[dynamic['city'].str.lower() == row['City'].lower()]['AQI']#.max()
    if len(rows) != 0:    
#         print(max(rows), min(rows))
        merged["AQI_Max"] = np.where(merged['City'].str.lower() == row['City'].lower(), max(rows), merged["AQI_Max"])
        merged["AQI_Min"] = np.where(merged['City'].str.lower() == row['City'].lower(), min(rows), merged["AQI_Min"])
#     if i > 2: break


pd.DataFrame(merged).to_csv("Merged_All.csv")

print("MERGE FINISHED")

