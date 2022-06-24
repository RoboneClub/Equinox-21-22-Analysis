import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from api import WorldWeatherOnline



"""_______________________ Part 0: Importing the experiment data _______________________"""
data = pd.read_csv('data.csv')

ndvi_data = pd.read_csv('xla.csv')

record_id = data["RecordID"].values
time = data["Time"].values
date = data['Date'].values

lat_data = data["Latitude"].values
long_data = data["Longitude"].values
alt_data = data["Altitude"].values

wwo = WorldWeatherOnline()

#weather_data = wwo.get_weather_data_single(lat_data[6507:11796], long_data[6507:11796], date[6507:11796])

#np.save("weather_data_2022-part-2.npy", weather_data)

weather_data = np.load("weather_data_2022.npy", allow_pickle=True)
weather_data_2 = np.load("weather_data_2022-part-2.npy", allow_pickle=True)

weather_data_all = []
for reading in weather_data[0:6508]:
    weather_data_all.append(reading)
for reading in weather_data_2:
    weather_data_all.append(reading)

#np.save("weather_data_2022-full.npy", weather_data_all)
weather_data_all = np.load("weather_data_2022-full.npy", allow_pickle=True)


#weather_data = np.array(weather_data)
# Available weather data currently is record 0:6506, 6507 records

avg_temp = np.array(wwo.get_avg_temp_single(weather_data_all)).flatten()
avg_wind_speed = np.array(wwo.get_avg_wind_speed_single(weather_data_all)).flatten()
avg_uv_index = np.array(wwo.get_uv_index_single(weather_data_all)).flatten()
avg_precip = np.array(wwo.get_avg_precipitation_single(weather_data_all)).flatten()
avg_humidity = np.array(wwo.get_avg_humidity_single(weather_data_all)).flatten()


'''Temperature'''
plt.title(f"Temperature")
plt.plot(record_id[0:len(avg_temp)], avg_temp)
plt.ylabel("Average Temperature/ C")
plt.xlabel("Record ID")
plt.xticks(np.arange(min(record_id), max(record_id)+1, 500))
plt.show()
#"""

'''Wind Speed'''
plt.title(f"Wind Speed")
plt.plot(record_id[0:len(avg_wind_speed)], avg_wind_speed)
plt.ylabel("Average Wind Speed/ KmHr")
plt.xlabel("Record ID")
plt.xticks(np.arange(min(record_id), max(record_id)+1, 500))
plt.show()

'''UV Index'''
plt.title(f"UV Index")
plt.plot(record_id[0:len(avg_uv_index)], avg_uv_index)
plt.ylabel("Average UV index")
plt.xlabel("Record ID")
plt.xticks(np.arange(min(record_id), max(record_id)+1, 500))
plt.show()

'''Precipitation'''
plt.title(f"Precipitation")
plt.plot(record_id[0:len(avg_precip)], avg_precip)
plt.ylabel("Average Precipitation/mm")
plt.xlabel("Record ID")
plt.xticks(np.arange(min(record_id), max(record_id)+1, 500))
plt.show()

'''Humidity'''
plt.title(f"Humidity")
plt.plot(record_id[0:len(avg_humidity)], avg_humidity)
plt.ylabel("Average Humidity/%")
plt.xlabel("Record ID")
plt.xticks(np.arange(min(record_id), max(record_id)+1, 500))
plt.show()