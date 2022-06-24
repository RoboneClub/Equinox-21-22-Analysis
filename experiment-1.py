import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from api import ClimateAnalysisIndicatorsTool, OpenWeatherMap, WorldWeatherOnline
from imu import IMU
from noise_filtering import NoiseFiltering

# _______________________ 0: Importing the experiment data _______________________
data = pd.read_csv('data.csv')

data_ndvi = pd.read_csv('xla.csv')

record_id = data["RecordID"].values
date = data['Date'].values
time = data["Time"].values

magnX = data["MagX"].values
magnY = data["MagY"].values
magnZ = data["MagZ"].values

# _______________________ 1: Extracting 6 points to preform the research on _______________________

# 1.1 - Setting the indicies for chosen points and years
points_of_study = [3978, 4207, 4341, 4848, 5315, 5409]
years_of_study = [2017, 2018, 2019, 2020, 2021, 2022]

# 1.2 - Extracting the locations of these points from the dataset

cait = ClimateAnalysisIndicatorsTool()

lat_dd = list(data.iloc[points_of_study]['Latitude'].values)
long_dd = list(data.iloc[points_of_study]['Longitude'].values)

locations = []
for lat, long in zip(lat_dd, long_dd):
    locations.append(cait.get_location(lat, long))

# 1.3 - Extracting the image ids of these points from the dataset
img_ids = list(data.iloc[points_of_study]['ImgID'].values)


# _______________ 2: Fetching the NDVI history data for the study points _______________

# 2.1 - Preparation - Setting up Dates and Locations

# Ceate NDVI API Object.
owm = OpenWeatherMap()

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


# _______________ 3: Fetching the Weather history data for the study points _______________

# Create Weather API Object.
wwo = WorldWeatherOnline()

# 3.1 Downloading the Weather data for the last 5 years for each point using the API
# weather_data = wwo.get_weather_data_history(lat_dd, long_dd, date)

# Save weather data.
# np.save("weather_data.npy", weather_data)

# Load weather data.
weather_data = np.load("weather_data.npy", allow_pickle=True)

# 3.2 - Extracting measurements

# Separately extract all needed metrics.
avg_temp = np.array(wwo.get_avg_temp(weather_data))
avg_wind_speed = np.array(wwo.get_avg_wind_speed(weather_data))
avg_uv_index = np.array(wwo.get_uv_index(weather_data))
avg_precip = np.array(wwo.get_avg_precipitation(weather_data))
avg_humidity = np.array(wwo.get_avg_humidity(weather_data))


# _______________ 4: Fetching the Gas Emission history data for the study points _______________

# 4.1 Downloading the Weather data for the last 5 years for each point using the API
gas_emission_data = cait.get_gas_emission_data(lat_dd, long_dd, 2017)

# 4.2 - Extracting measurements
co2_emissions = np.array(cait.get_co2(gas_emission_data))
ch4_emissions = np.array(cait.get_ch4(gas_emission_data))

# _______________________ 5: Analyzing the magnometer data _______________________


# 5.1 - Preprocessing the data by applying noise filteration

# Create IMU API Object
imu = IMU()

# Create Noise Filteration Object
nf = NoiseFiltering()

# Apply Noise Filteration to Magnetic Intensity Data
magn_filtered_matrix = nf.noise_filter(
    magnX,
    magnY,
    magnZ,
    # Senstivity and Frequency are according to https://www.st.com/resource/en/datasheet/lsm9ds1.pdf
    # RMS Noise assumtion according to https://www.st.com/resource/en/datasheet/lis3mdl.pdf
    # which is a similar build
    sensitivity=0.043,
    frequency=20,
    rms=(3.2 * 10**-3)
)


# 5.2 - Calculating the resultant magnitude, the standard deviation, the mean
# and the auto correlation of the points
magn_resultant = imu.get_resultant(
    magn_filtered_matrix[:, 0],
    magn_filtered_matrix[:, 1],
    magn_filtered_matrix[:, 2]
)
magn_sd = imu.get_sd(magn_resultant)
magn_mean = imu.get_mean(magn_resultant)

# 5.3 - Extracting the magnetic field readings corresponding to the chosen indices for the study
magn_points_of_study = pd.DataFrame(
    {'col': magn_resultant}
).iloc[points_of_study].values.flatten(order='C')

# 5.4 - Get the magnometic values history for 5 years of each location
# Refrence for decay value:
# https://www.pnas.org/content/115/20/5111#:~:text=Abstract,since%201600%20or%20even%20earlier.
magn_history = imu.get_magn_history(magn_points_of_study, decay=0.0005)


# _______________________ 6: Plotting the data _______________________


# 6.1 -----------------------NDVI-----------------------

# 6.1.1 - NDVI - Time - All Locations
x_axis = np.array(years_of_study)
plt.title("NDVI - Time - All Locations")
for i, location in enumerate(locations):
    plt.plot(x_axis, mean_ndvi[i], label=location)
    plt.scatter(x_axis, mean_ndvi[i])
plt.xlabel("Year", labelpad=20)
plt.ylabel('Mean NDVI', labelpad=20)
plt.legend()
fig = plt.gcf()
fig.set_size_inches(16, 9)
plt.savefig("NDVI - Time - All Locations.png", dpi=500)
plt.show()

# 6.1.2 - NDVI - Gas Emissions

# 6.1.2.1 - NDVI - CO2 Emissions - All Locations
for i, location in enumerate(locations):
    plt.scatter(mean_ndvi[i][0], co2_emissions[i], label=f"{location}")
plt.title("NDVI - Carbon Dioxide Emissions 2017")
plt.xlabel("Mean NDVI")
plt.ylabel("Emissions/Kt")
plt.legend()
fig = plt.gcf()
fig.set_size_inches(16, 9)
plt.savefig("NDVI - Carbon Dioxide Emissions 2017.png", dpi=500)
plt.show()

# 6.1.2.2 - NDVI - CH4 Emissions - All Locations
for i, location in enumerate(locations):
    plt.scatter(mean_ndvi[i][0], ch4_emissions[i], label=f"{location}")
plt.title("NDVI - Methane Emissions 2017")
plt.xlabel("Mean NDVI")
plt.ylabel("Emissions/Kt")
plt.legend()
fig = plt.gcf()
fig.set_size_inches(16, 9)
plt.savefig("NDVI - Methane Emissions 2017.png", dpi=500)
plt.show()

# 6.1.3 - NDVI vs Climate

# 6.1.3.1 - NDVI - Temperature - All Locations
for i, location in enumerate(locations):
    plt.title(f"NDVI - Temperature - {location}")
    plt.scatter(mean_ndvi[i], avg_temp[i])
    plt.xlabel("Mean NDVI")
    plt.ylabel("Average Temperature/C")
    fig = plt.gcf()
    fig.set_size_inches(16, 9)
    plt.savefig(f"NDVI - Temperature - {location}.png", dpi=500)
    plt.show()

# 6.1.3.2 - NDVI - Wind Speed - All Locations
for i, location in enumerate(locations):
    plt.title(f"NDVI - Wind Speed - {location}")
    plt.scatter(mean_ndvi[i], avg_wind_speed[i])
    plt.xlabel("Mean NDVI")
    plt.ylabel("Average Wind Speed/KmHr")
    fig = plt.gcf()
    fig.set_size_inches(16, 9)
    plt.savefig(f"NDVI - Wind Speed - {location}.png", dpi=500)
    plt.show()

# 6.1.3.3 - NDVI - UV Index - All Locations
for i, location in enumerate(locations):
    plt.title(f"NDVI - UV Index - {location}")
    plt.scatter(mean_ndvi[i], avg_uv_index[i])
    plt.xlabel("Mean NDVI")
    plt.ylabel("Average UV index")
    fig = plt.gcf()
    fig.set_size_inches(16, 9)
    plt.savefig(f"NDVI - UV Index - {location}.png", dpi=500)
    plt.show()

# 6.1.3.4 - NDVI - Precipitation - All Locations
for i, location in enumerate(locations):
    plt.title(f"NDVI - Precipitation - {location}")
    plt.scatter(mean_ndvi[i], avg_precip[i])
    plt.xlabel("Mean NDVI")
    plt.ylabel("Average Precipitation/mm")
    fig = plt.gcf()
    fig.set_size_inches(16, 9)
    plt.savefig(f"NDVI - Precipitation - {location}.png", dpi=500)
    plt.show()

# 6.1.3.5 - NDVI - Humidity - All Locations
for i, location in enumerate(locations):
    plt.title(f"NDVI - Humidity - {location}")
    plt.scatter(mean_ndvi[i], avg_humidity[i])
    plt.xlabel("Mean NDVI")
    plt.ylabel("Average Humidity/%")
    fig = plt.gcf()
    fig.set_size_inches(16, 9)
    plt.savefig(f"NDVI - Humidity - {location}.png", dpi=500)
    plt.show()

# 6.1.4 - NDVI - Magnetic Intensity - All Locations
for i, location in enumerate(locations):
    plt.title(f"Magnetic Intensity - Mean NDVI - {location}")
    plt.scatter(mean_ndvi[i], magn_history[i])
    plt.xlabel("Mean NDVI")
    plt.ylabel("Magnetic Intensity/µT")
    fig = plt.gcf()
    fig.set_size_inches(16, 9)
    plt.savefig(f"Magnetic Intensity - Mean NDVI - {location}.png", dpi=500)
    plt.show()


# 6.2 -----------------------Magnetic Intensity-----------------------


# 6.2.1 - Magnetic Intensity - Time - All Locations
x_axis = np.array(years_of_study)
plt.title("Magnetic Intensity - Year - All Locations")
for i, location in enumerate(locations):
    plt.plot(x_axis, magn_history[i], label=location)
    plt.scatter(x_axis, magn_history[i])
plt.xlabel("Year", labelpad=20)
plt.ylabel('Magnetic Intensity/µT', labelpad=20)
plt.legend()
fig = plt.gcf()
fig.set_size_inches(16, 9)
plt.savefig("Magnetic Intensity - Year - All Locations.png", dpi=500)
plt.show()

# 6.2.2 - Magnetic Intensity - Climate

# 6.2.2.1 - Magnetic Intensity - Temperature - All Locations
for i, location in enumerate(locations):
    plt.title(f"Magnetic Intensity - Temperature - {location}")
    plt.scatter(magn_history[i], avg_temp[i])
    plt.xlabel("Magnetic Intensity/µT")
    plt.ylabel("Average Temperature/C")
    fig = plt.gcf()
    fig.set_size_inches(16, 9)
    plt.savefig(f"Magnetic Intensity - Temperature - {location}.png", dpi=500)
    plt.show()

# 6.2.2.2 - Magnetic Intensity - Wind Speed - All Locations
for i, location in enumerate(locations):
    plt.title(f"Magnetic Intensity - Wind Speed - {location}")
    plt.scatter(magn_history[i], avg_wind_speed[i])
    plt.xlabel("Magnetic Intensity/µT")
    plt.ylabel("Average Wind Speed/KmHr")
    fig = plt.gcf()
    fig.set_size_inches(16, 9)
    plt.savefig(f"Magnetic Intensity - Wind Speed - {location}.png", dpi=500)
    plt.show()

# 6.2.2.3 - Magnetic Intensity - UV Index - All Locations
for i, location in enumerate(locations):
    plt.title(f"Magnetic Intensity - UV Index - {location}")
    plt.scatter(magn_history[i], avg_uv_index[i])
    plt.xlabel("Magnetic Intensity/µT")
    plt.ylabel("Average UV index")
    fig = plt.gcf()
    fig.set_size_inches(16, 9)
    plt.savefig(f"Magnetic Intensity - UV Index - {location}.png", dpi=500)
    plt.show()

# 6.2.2.4 - Magnetic Intensity - Precipitation - All Locations
for i, location in enumerate(locations):
    plt.title(f"Magnetic Intensity - Precipitation - {location}")
    plt.scatter(magn_history[i], avg_precip[i])
    plt.xlabel("Magnetic Intensity/µT")
    plt.ylabel("Average Precipitation/mm")
    fig = plt.gcf()
    fig.set_size_inches(16, 9)
    plt.savefig(f"Magnetic Intensity - Precipitation - {location}.png", dpi=500)
    plt.show()

# 6.2.2.5 - Magnetic Intensity - Humidity - All Locations
for i, location in enumerate(locations):
    plt.title(f"Magnetic Intensity - Humidity - {location}")
    plt.scatter(magn_history[i], avg_humidity[i])
    plt.xlabel("Magnetic Intensity/µT")
    plt.ylabel("Average Humidity/%")
    fig = plt.gcf()
    fig.set_size_inches(16, 9)
    plt.savefig(f"Magnetic Intensity - Humidity - {location}.png", dpi=500)
    plt.show()
