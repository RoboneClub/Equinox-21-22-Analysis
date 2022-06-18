import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from api import ClimateAnalysisIndicatorsTool, OpenWeatherMap, WorldWeatherOnline
from magn import Magn, NoiseFiltering

"""_______________________ Part 0: Importing the experiment data _______________________"""
data = pd.read_csv('data.csv')

data_ndvi = pd.read_csv('xla.csv')

record_id = data["RecordID"]
time = data["Time"].values

magnX = data["MagX"].values
magnY = data["MagY"].values
magnZ = data["MagZ"].values

"""_______________________ Part 1: Extracting 6 points to preform the research on _______________________"""

''' 0-The chosen points: '''
#Indices of the chosen points:
points_of_study = [3978, 4207, 4341, 4848, 5315, 5409]
years_of_study = [2017, 2018, 2019, 2020, 2021, 2022]

'''1-Extracting the location of these points from the dataset'''

cait = ClimateAnalysisIndicatorsTool()

lat_dd = list(data.iloc[points_of_study]['Latitude'].values)
long_dd = list(data.iloc[points_of_study]['Longitude'].values)

locations = []
for lat, long in zip(lat_dd, long_dd):
    locations.append(cait.get_location(lat, long))

'''2-Extracting the image ids of these points from the dataset'''
img_ids = list(data.iloc[points_of_study]['ImgID'].values)


"""_______________________ Part 2: Fetching the NDVI history data for the study points _______________________"""

owm = OpenWeatherMap()

'''Importing the date for the Points'''
date = data.iloc[points_of_study]['Date'].values

'''Setting the dates for the requests'''
dates = owm.get_dates(date[0])

'''Setting the areas for each point'''
polys = owm.get_polys()

'''Downloading the NDVI data for the last 5 years for each point using the API'''
ndvi_data = owm.get_ndvi_data(polys, dates)

mean_ndvi = np.array(owm.get_mean_ndvi(ndvi_data))

'''Importing the 2022 NDVI collected on board the ISS'''
ndvi_data_2022 = pd.read_csv('xla.csv')

mean_ndvi_2022 = np.array(ndvi_data_2022.iloc[img_ids]["NDVI"])

'''Adding new data to mean NDVI dataset'''
mean_ndvi = np.concatenate((mean_ndvi, mean_ndvi_2022[:,None]),axis=1)



"""_______________________ Part 3: Fetching the Weather history data for the study points _______________________"""


wwo = WorldWeatherOnline()

weather_data = wwo.get_weather_data(lat_dd, long_dd, date)

avg_temp = np.array(wwo.get_avg_temp(weather_data))
avg_wind_speed = np.array(wwo.get_avg_wind_speed(weather_data))
avg_uv_index = np.array(wwo.get_uv_index(weather_data))
avg_precip = np.array(wwo.get_avg_precipitation(weather_data))
avg_humidity = np.array(wwo.get_avg_humidity(weather_data))


"""_______________________ Part 4: Fetching the Gas Emission history data for the study points _______________________"""

gas_emission_data = cait.get_gas_emission_data(lat_dd, long_dd, 2017)

co2_emissions = np.array(cait.get_co2(gas_emission_data))
ch4_emissions = np.array(cait.get_ch4(gas_emission_data))

"""_______________________ Part 5: Analyzing the magnometer data _______________________"""


''' 1-Preprocessing the data by applying noise filteration '''

magn = Magn()
nf = NoiseFiltering()

magn_filtered_matrix = nf.noise_filter(
    magnX,
    magnY,
    magnZ,
    sensitivity = 0.043,
    frequency = 20,
    rms = (3.2 * 10**-3)
)
# Senstivity and Frequency are according to https://www.st.com/resource/en/datasheet/lsm9ds1.pdf
# RMS Noise assumtion according to https://www.st.com/resource/en/datasheet/lis3mdl.pdf
# which is a similar build


''' 3- Calculating the resultant magnitude of the magnetic field, the standard deviation,the mean and the  auto corelation of the points'''

magn_resultant = magn.get_resultant(magn_filtered_matrix[:,0], magn_filtered_matrix[:, 1], magn_filtered_matrix[:,2])
magn_sd = magn.get_sd(magn_resultant)
magn_mean = magn.get_mean(magn_resultant)
#magn_autocorrelation = magn.autocor(magn_resultant) #A graph is plotted for the magnetic intensity autocorrelation in expirment 2



'''3-Extract the magnetic field readings corresponding to the chosen indices for the study:'''
magn_points_of_study = pd.DataFrame({'col':magn_resultant}).iloc[points_of_study].values.flatten(order='C')


'''4-Get the magnometic values history for 10 years of each location '''
#Refrence for decay value: https://www.pnas.org/content/115/20/5111#:~:text=Abstract,since%201600%20or%20even%20earlier.


magn_history = magn.get_magn_history(magn_points_of_study, decay = 0.0005)


"""_______________________ Part 6: Plotting the data _______________________"""

#"""

'''_______________________NDVI_______________________'''

'''NDVI - CO2 Emissions - All Locations'''
for i, location in enumerate(locations):
    plt.scatter(mean_ndvi[i][0], co2_emissions[i], label=f"{location}")
plt.title(f"NDVI - Carbon Dioxide Emissions 2017")
plt.ylabel("Emissions/ Kt")
plt.xlabel("Mean NDVI")
plt.legend()
plt.show()

'''NDVI - CH4 Emissions - All Locations'''
for i, location in enumerate(locations):
    plt.scatter(mean_ndvi[i][0], ch4_emissions[i], label=f"{location}")
plt.title(f"NDVI - Methane Emissions 2017")
plt.ylabel("Emissions/ Kt")
plt.xlabel("Mean NDVI")
plt.legend()
plt.show()

"""

'''NDVI - Time - All Locations'''
x_axis = np.array(years_of_study)
for i, location in enumerate(locations):
    plt.plot(x_axis, mean_ndvi[i], label=location)
    plt.scatter(x_axis, mean_ndvi[i])
plt.xlabel("Year", labelpad=20)
plt.ylabel('Mean NDVI', labelpad=20)
plt.legend()
plt.show()

'''NDVI - Temperature - All Locations'''
for i, location in enumerate(locations):
    plt.title(f"NDVI - Temperature - {location}")
    plt.scatter(mean_ndvi[i], avg_temp[i])
    plt.ylabel("Average Temperature/ C")
    plt.xlabel("Mean NDVI")
    plt.show()

'''NDVI - Wind Speed - All Locations'''
for i, location in enumerate(locations):
    plt.title(f"NDVI - Wind Speed - {location}")
    plt.scatter(mean_ndvi[i], avg_wind_speed[i])
    plt.ylabel("Average Wind Speed/ KmHr")
    plt.xlabel("Mean NDVI")
    plt.show()

'''NDVI - UV Index - All Locations'''
for i, location in enumerate(locations):
    plt.title(f"NDVI - UV Index - {location}")
    plt.scatter(mean_ndvi[i], avg_uv_index[i])
    plt.ylabel("Average UV index")
    plt.xlabel("Mean NDVI")
    plt.show()

'''NDVI - Precipitation - All Locations'''
for i, location in enumerate(locations):
    plt.title(f"NDVI - Precipitation - {location}")
    plt.scatter(mean_ndvi[i], avg_precip[i])
    plt.ylabel("Average Precipitation/mm")
    plt.xlabel("Mean NDVI")
    plt.show()

'''NDVI - Humidity - All Locations'''
for i, location in enumerate(locations):
    plt.title(f"NDVI - Humidity - {location}")
    plt.scatter(mean_ndvi[i], avg_humidity[i])
    plt.ylabel("Average Humidity/%")
    plt.xlabel("Mean NDVI")
    plt.show()

'''NDVI - Magnetic Intensity - All Locations'''
for i, location in enumerate(locations):
    plt.title(f"Magnetic Intensity - Mean NDVI - {location}")
    plt.scatter(mean_ndvi[i], magn_history[i])
    plt.ylabel("Magnetic Intensity/µT")
    plt.xlabel("Mean NDVI")
    plt.show()


'''_______________________Magnetic Intensity_______________________'''


'''Magnetic Intensity - Time - All Locations'''
x_axis = np.array(years_of_study)
for i, location in enumerate(locations):
    plt.plot(x_axis, magn_history[i], label=location)
    plt.scatter(x_axis, magn_history[i])
plt.xlabel("Year", labelpad=20)
plt.ylabel('Mean NDVI', labelpad=20)
plt.legend()
plt.show()

'''Magnetic Intensity - Temperature - All Locations'''
for i, location in enumerate(locations):
    plt.title(f"NDVI - Temperature - {location}")
    plt.scatter(magn_history[i], avg_temp[i])
    plt.ylabel("Average Temperature/ C")
    plt.xlabel("Mean NDVI")
    plt.show()

'''Magnetic Intensity - Wind Speed - All Locations'''
for i, location in enumerate(locations):
    plt.title(f"NDVI - Wind Speed - {location}")
    plt.scatter(magn_history[i], avg_wind_speed[i])
    plt.ylabel("Average Wind Speed/ KmHr")
    plt.xlabel("Mean NDVI")
    plt.show()

'''Magnetic Intensity - UV Index - All Locations'''
for i, location in enumerate(locations):
    plt.title(f"NDVI - UV Index - {location}")
    plt.scatter(magn_history[i], avg_uv_index[i])
    plt.ylabel("Average UV index")
    plt.xlabel("Mean NDVI")
    plt.show()

'''Magnetic Intensity - Precipitation - All Locations'''
for i, location in enumerate(locations):
    plt.title(f"NDVI - Precipitation - {location}")
    plt.scatter(magn_history[i], avg_precip[i])
    plt.ylabel("Average Precipitation/mm")
    plt.xlabel("Mean NDVI")
    plt.show()

'''Magnetic Intensity - Humidity - All Locations'''
for i, location in enumerate(locations):
    plt.title(f"NDVI - Humidity - {location}")
    plt.scatter(magn_history[i], avg_humidity[i])
    plt.ylabel("Average Humidity/%")
    plt.xlabel("Mean NDVI")
    plt.show()

# This belongs to Experiment 2.0 [ \/ ]
'''Magnetic Intensity '''
plt.title("Magnetic Intensity Readings")
plt.xlabel("Record ID")
plt.ylabel("Magnetic Intensity/µT")
plt.plot(record_id, magnX, label='MagnX')
plt.plot(record_id, magnY, label='MagnY')
plt.plot(record_id, magnZ, label='MagnZ')
plt.xticks(np.arange(min(record_id), max(record_id)+1, 500))
plt.legend()
plt.show()

plt.title("Magnetic Intensity Data")
plt.xlabel("Record ID")
plt.ylabel("Magnetic Intensity/µT")
plt.plot(record_id, magn_resultant, label='MagnResultant')
plt.plot(record_id, [magn_mean]*len(magnX), label=f'Mean = {round(magn_mean, 4)}')
plt.plot(record_id, [magn_sd]*len(magnX), label=f'Standard Deviation = {round(magn_sd, 4)}')
plt.xticks(np.arange(min(record_id), max(record_id)+1, 500))
plt.legend()
plt.show()

#"""