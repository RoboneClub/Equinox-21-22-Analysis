import numpy as np
from api import ClimateAnalysisIndicatorsTool, OpenWeatherMap
import pandas as pd
import matplotlib.pyplot as plt


data = pd.read_csv('data.csv')
data_ndvi = pd.read_csv('xla.csv')
points_of_study = [3978, 4207, 4341, 4848, 5315, 5409]

date = data['Date'].values

lat_dd = list(data.iloc[points_of_study]['Latitude'].values)
long_dd = list(data.iloc[points_of_study]['Longitude'].values)
img_ids = list(data.iloc[points_of_study]['ImgID'].values)

cait = ClimateAnalysisIndicatorsTool()
owm = OpenWeatherMap()



# 4.1 Downloading the Weather data for the last 5 years for each point using the API
gas_emission_data = cait.get_gas_emission_data(lat_dd, long_dd, 2017)

# 4.2 - Extracting measurements
co2_emissions = np.array(cait.get_co2(gas_emission_data))
ch4_emissions = np.array(cait.get_ch4(gas_emission_data))

locations = []
for lat, long in zip(lat_dd, long_dd):
    locations.append(cait.get_location(lat, long))


# Set the date for the requests.
dates = owm.get_dates(date[0])

# Set the areas for each point.
polys = owm.get_polys()

# 2.2 - Downloading the NDVI data for the last 5 years for each point using the API
ndvi_data = owm.get_ndvi_data(polys, dates)

# 2.3 - Extracting Mean NDVI
# Extract Mean NDVI for each reading in the data.
mean_ndvi = np.array(owm.get_mean_ndvi(ndvi_data))

# Import the 2022 Mean NDVI collected on board the ISS for the chosen images.
mean_ndvi_2022 = np.array(data_ndvi.iloc[img_ids]["NDVI"])

# Adding new data to mean NDVI dataset
mean_ndvi = np.concatenate((mean_ndvi, mean_ndvi_2022[:, None]), axis=1)

# 6.1.2.1 - NDVI - CO2 Emissions - All Locations
print("CO2")
for i, location in enumerate(locations):
    print("----------")
    print(location)
    print(f"NDVI: {mean_ndvi[i][0]}, Emission: {co2_emissions[i]}")



# 6.1.2.2 - NDVI - CH4 Emissions - All Locations
print("CH4")
for i, location in enumerate(locations):
    print("----------")
    print(location)
    print(f"NDVI: {mean_ndvi[i][0]}, Emission: {ch4_emissions[i]}")

