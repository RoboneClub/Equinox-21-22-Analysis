"""
Developed by: Team Equinox
Description: Code responsible for running experiment 2.0
and producting its plots

References:
- TBD
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from api import WorldWeatherOnline
from imu import IMU
from noise_filtering import NoiseFiltering


# _______________________ 0: Importing the experiment data _______________________


data = pd.read_csv('data.csv')

ndvi_data = pd.read_csv('xla.csv')

record_id = data["RecordID"].values
time = data["Time"].values
date = data['Date'].values

lat_data = data["Latitude"].values
long_data = data["Longitude"].values
alt_data = data["Altitude"].values

pitch_data = data["Pitch"].values
roll_data = data["Roll"].values
yaw_data = data["Yaw"].values

gyroX = data["GyroX"].values
gyroY = data["GyroY"].values
gyroZ = data["GyroZ"].values

magnX = data["MagX"].values
magnY = data["MagY"].values
magnZ = data["MagZ"].values

accX = data["AccX"].values
accY = data["AccY"].values
accZ = data["AccZ"].values


# _______________________ 1: Analyzing the IMU sensor data _______________________


imu = IMU()
nf = NoiseFiltering()

# 1.1 - Preprocessing the data by applying noise filteration
gyro_filtered_matrix = nf.noise_filter(
    gyroX, gyroY, gyroZ,
    # Senstivity and Frequency are according to https://www.st.com/resource/en/datasheet/lsm9ds1.pdf
    # RMS Noise assumtion according to https://www.st.com/resource/en/datasheet/lis3mdl.pdf
    # which is a similar build
    sensitivity=(0.0175),
    frequency=476,
    rms=(3.2 * 10**-3)
)
magn_filtered_matrix = nf.noise_filter(
    magnX, magnY, magnZ,
    # Senstivity and Frequency are according to https://www.st.com/resource/en/datasheet/lsm9ds1.pdf
    # RMS Noise assumtion according to https://www.st.com/resource/en/datasheet/lis3mdl.pdf
    # which is a similar build
    sensitivity=0.043,
    frequency=20,
    rms=(3.2 * 10**-3)
)
acc_filtered_matrix = nf.noise_filter(
    accX, accY, accZ,
    # Senstivity and Frequency are according to https://www.st.com/resource/en/datasheet/lsm9ds1.pdf
    # RMS Noise assumtion according to https://www.st.com/resource/en/datasheet/lis3mdl.pdf
    # which is a similar build
    sensitivity=(0.000244 * 9.81),
    frequency=10,
    rms=(3.2 * 10**-3)
)

# 1.2 - Getting X, Y, Z, components for filtered matricies
gyroX_filtered = gyro_filtered_matrix[:, 0]
gyroY_filtered = gyro_filtered_matrix[:, 1]
gyroZ_filtered = gyro_filtered_matrix[:, 2]

magnX_filtered = magn_filtered_matrix[:, 0]
magnY_filtered = magn_filtered_matrix[:, 1]
magnZ_filtered = magn_filtered_matrix[:, 2]

accX_filtered = acc_filtered_matrix[:, 0]
accY_filtered = acc_filtered_matrix[:, 1]
accZ_filtered = acc_filtered_matrix[:, 2]

# 1.3 - Calculating the resultant magnitude, the standard deviation, the mean
# the correlation and the autocorrelation of the points
# for the filtered and unfiltered
# magnetic field intensity, acceleration, and angular velocity

# 1.3.1 - Unfiltered
# 1.3.1.1 - Magnetic Intensity
magn_resultant = imu.get_resultant(magnX, magnY, magnZ)

magnX_sd = imu.get_sd(magnX)
magnY_sd = imu.get_sd(magnY)
magnZ_sd = imu.get_sd(magnZ)
magn_sd = imu.get_sd(magn_resultant)

magnX_mean = imu.get_mean(magnX)
magnY_mean = imu.get_mean(magnY)
magnZ_mean = imu.get_mean(magnZ)
magn_mean = imu.get_mean(magn_resultant)

magn_autocorrelation = imu.correlate(magn_resultant, magn_resultant)

# 1.3.1.2 - Acceleration
acc_resultant = imu.get_resultant(accX, accY, accZ)

accX_sd = imu.get_sd(accX)
accY_sd = imu.get_sd(accY)
accZ_sd = imu.get_sd(accZ)
acc_sd = imu.get_sd(acc_resultant)

accX_mean = imu.get_mean(accX)
accY_mean = imu.get_mean(accY)
accZ_mean = imu.get_mean(accZ)
acc_mean = imu.get_mean(acc_resultant)

acc_autocorrelation = imu.correlate(acc_resultant, acc_resultant)

# 1.3.1.3 - Gyroscope Angular Velocity
gyro_resultant = imu.get_resultant(gyroX, gyroY, gyroZ)

gyroX_sd = imu.get_sd(gyroX)
gyroY_sd = imu.get_sd(gyroY)
gyroZ_sd = imu.get_sd(gyroZ)
gyro_sd = imu.get_sd(gyro_resultant)

gyroX_mean = imu.get_mean(gyroX)
gyroY_mean = imu.get_mean(gyroY)
gyroZ_mean = imu.get_mean(gyroZ)
gyro_mean = imu.get_mean(gyro_resultant)

gyro_autocorrelation = imu.correlate(gyro_resultant, gyro_resultant)

# 1.3.2 - Filtered
# 1.3.2.1 - Magnetic Intensity
magn_filtered_resultant = imu.get_resultant(magnX_filtered, magnY_filtered, magnZ_filtered)

magnX_filtered_sd = imu.get_sd(magnX_filtered)
magnY_filtered_sd = imu.get_sd(magnY_filtered)
magnZ_filtered_sd = imu.get_sd(magnZ_filtered)
magn_filtered_sd = imu.get_sd(magn_filtered_resultant)

magnX_filtered_mean = imu.get_mean(magnX_filtered)
magnY_filtered_mean = imu.get_mean(magnY_filtered)
magnZ_filtered_mean = imu.get_mean(magnZ_filtered)
magn_filtered_mean = imu.get_mean(magn_filtered_resultant)

magn_filtered_autocorrelation = imu.correlate(magn_filtered_resultant, magn_filtered_resultant)

# 1.3.2.2 - Acceleration
acc_filtered_resultant = imu.get_resultant(accX_filtered, accY_filtered, accZ_filtered)

accX_filtered_sd = imu.get_sd(accX_filtered)
accY_filtered_sd = imu.get_sd(accY_filtered)
accZ_filtered_sd = imu.get_sd(accZ_filtered)
acc_filtered_sd = imu.get_sd(acc_filtered_resultant)

accX_filtered_mean = imu.get_mean(accX_filtered)
accY_filtered_mean = imu.get_mean(accY_filtered)
accZ_filtered_mean = imu.get_mean(accZ_filtered)
acc_filtered_mean = imu.get_mean(acc_filtered_resultant)

acc_filtered_autocorrelation = imu.correlate(acc_filtered_resultant, acc_filtered_resultant)

# 1.3.2.3 - Gyroscope Angular Velocity
gyro_filtered_resultant = imu.get_resultant(gyroX_filtered, gyroY_filtered, gyroZ_filtered)

gyroX_filtered_sd = imu.get_sd(gyroX_filtered)
gyroY_filtered_sd = imu.get_sd(gyroY_filtered)
gyroZ_filtered_sd = imu.get_sd(gyroZ_filtered)
gyro_filtered_sd = imu.get_sd(gyro_filtered_resultant)

gyroX_filtered_mean = imu.get_mean(gyroX_filtered)
gyroY_filtered_mean = imu.get_mean(gyroY_filtered)
gyroZ_filtered_mean = imu.get_mean(gyroZ_filtered)
gyro_filtered_mean = imu.get_mean(gyro_filtered_resultant)

gyro_filtered_autocorrelation = imu.correlate(gyro_filtered_resultant, gyro_filtered_resultant)


# 1.3.3 - Correlating Data

# 1.3.3.1 - Unfiltered
magn_acc_cor = imu.correlate(magn_resultant, acc_resultant)
magn_gyro_cor = imu.correlate(magn_resultant, gyro_resultant)
acc_gyro_cor = imu.correlate(acc_resultant, gyro_resultant)

# 1.3.3.2 - Filtered
magn_acc_filtered_cor = imu.correlate(magn_filtered_resultant, acc_filtered_resultant)
magn_gyro_filtered_cor = imu.correlate(magn_filtered_resultant, gyro_filtered_resultant)
acc_gyro_filtered_cor = imu.correlate(acc_filtered_resultant, gyro_filtered_resultant)


# _______________ 2: Fetching the NDVI data for runtime orbit _______________


# 2.1 - Importing the 2022 NDVI collected on board the ISS
ndvi_data = pd.read_csv('xla.csv')

# 2.2 - Extracting Mean NDVI
mean_ndvi = np.array(
    [
        # List comprehension.
        # Get the NDVI value with an ImgID corresponding to the one in the current record,
        list(ndvi_data["NDVI"].loc[ndvi_data["ImgID"] == data["ImgID"].iloc[record]].values)[0]

        # If said value is not empty, else, set the value to numpy's NaN
        if list(ndvi_data["NDVI"].loc[ndvi_data["ImgID"] == data["ImgID"].iloc[record]].values)
        != [] else np.NaN

        # For each record in the main data dictionairy.
        for record in list([record for record in data["RecordID"].values])
    ]
)


# _______________________ 3: Fetching the weather data for runtime orbit _______________________


# Ceate Weather API Object.
wwo = WorldWeatherOnline()

# 3.1 - Fetching weather data

# Download weather data for all records.
# weather_data = wwo.get_weather_data_single(lat_data, long_data, date)

# Save weather data.
# np.save("weather_data_2022.npy", weather_data)

# Load weather data.
weather_data = np.load("weather_data_2022-full.npy", allow_pickle=True)

# 3.2 - Extracting measurements

# Separately extract all needed metrics.
avg_temp = np.array(wwo.get_avg_temp_single(weather_data)).flatten()
avg_wind_speed = np.array(wwo.get_avg_wind_speed_single(weather_data)).flatten()
avg_uv_index = np.array(wwo.get_uv_index_single(weather_data)).flatten()
avg_precip = np.array(wwo.get_avg_precipitation_single(weather_data)).flatten()
avg_humidity = np.array(wwo.get_avg_humidity_single(weather_data)).flatten()


# _______________________ 4: Plotting the data _______________________


# 4.1 -----------------------NDVI-----------------------

# 4.1.1 - NDVI - Record ID
plt.title("NDVI - Records")
plt.plot(record_id, mean_ndvi)
plt.xlabel("Record ID")
plt.ylabel("NDVI Index")
plt.xticks(np.arange(min(record_id), max(record_id) + 1, 500))
plt.yticks(np.arange(-1, 1.1, 0.1))
fig = plt.gcf()
fig.set_size_inches(16, 9)
plt.savefig("NDVI - Records.png", dpi=500)
plt.show()

# 4.1.2 - NDVI - Magnetic Intensity
plt.title("NDVI - Magnetic Intensity")
plt.scatter(mean_ndvi, magn_filtered_resultant)
plt.xlabel("NDVI Index")
plt.ylabel("Magnetic Intensity/µT")
plt.xticks(np.arange(-1, 1.1, 0.1))
fig = plt.gcf()
fig.set_size_inches(16, 9)
plt.savefig("NDVI - Magnetic Intensity.png", dpi=500)
plt.show()

# 4.1.3 - NDVI - Weather

# 4.1.3.1 - NDVI - Temperature
plt.title("NDVI - Temperature")
plt.scatter(mean_ndvi, avg_temp)
plt.xlabel("NDVI Index")
plt.ylabel("Average Temperature/C")
plt.xticks(np.arange(-1, 1.1, 0.1))
fig = plt.gcf()
fig.set_size_inches(16, 9)
plt.savefig("NDVI - Temperature.png", dpi=500)
plt.show()

# 4.1.3.2 - NDVI - Wind Speed
plt.title("NDVI - Wind Speed")
plt.scatter(mean_ndvi, avg_wind_speed)
plt.xlabel("NDVI Index")
plt.ylabel("Average Wind Speed/KmHr")
plt.xticks(np.arange(-1, 1.1, 0.1))
fig = plt.gcf()
fig.set_size_inches(16, 9)
plt.savefig("NDVI - Wind Speed.png", dpi=500)
plt.show()

# 4.1.3.3 - NDVI - UV Index
plt.title("NDVI - UV Index")
plt.scatter(mean_ndvi, avg_uv_index)
plt.xlabel("NDVI Index")
plt.ylabel("Average UV Index")
plt.xticks(np.arange(-1, 1.1, 0.1))
fig = plt.gcf()
fig.set_size_inches(16, 9)
plt.savefig("NDVI - UV Index.png", dpi=500)
plt.show()

# 4.1.3.4 - NDVI - Precipitation
plt.title("NDVI - Precipitation")
plt.scatter(mean_ndvi, avg_precip)
plt.xlabel("NDVI Index")
plt.ylabel("Average Precipitation/mm")
plt.xticks(np.arange(-1, 1.1, 0.1))
fig = plt.gcf()
fig.set_size_inches(16, 9)
plt.savefig("NDVI - Precipitation.png", dpi=500)
plt.show()

# 4.1.3.5 - NDVI - Humidity
plt.title("NDVI - Humidity")
plt.scatter(mean_ndvi, avg_humidity)
plt.xlabel("NDVI Index")
plt.ylabel("Average Humidity/%")
plt.xticks(np.arange(-1, 1.1, 0.1))
fig = plt.gcf()
fig.set_size_inches(16, 9)
plt.savefig("NDVI - Humidity.png", dpi=500)
plt.show()

# 4.2 -----------------------Magnetic Intensity-----------------------

# 4.2.1 - Filtered Magnetic Intensity - Record ID
plt.title("Filtered Magnetic Intensity - Record")

plt.plot(record_id, magn_filtered_resultant, label="Resultant Magnitude")
plt.plot(record_id, magnX_filtered, label="Magnetic Intensity X")
plt.plot(record_id, magnY_filtered, label="Magnetic Intensity Y")
plt.plot(record_id, magnZ_filtered, label="Magnetic Intensity Z")

plt.xlabel("Record ID", labelpad=20)
plt.ylabel('Magnetic Intensity/µT', labelpad=20)
plt.xticks(np.arange(min(record_id), max(record_id) + 1, 500))
plt.legend()
fig = plt.gcf()
fig.set_size_inches(16, 9)
plt.savefig("Filtered Magnetic Intensity - Record.png", dpi=500)
plt.show()

# 4.2.2 - Magnetic Intensity - Weather

# 4.2.2.1 - Magnetic Intensity - Temperature
plt.title("Magnetic Intensity - Temperature")
plt.scatter(magn_filtered_resultant, avg_temp)
plt.xlabel("Magnetic Intensity/µT")
plt.ylabel("Average Temperature/C")
fig = plt.gcf()
fig.set_size_inches(16, 9)
plt.savefig("Magnetic Intensity - Temperature.png", dpi=500)
plt.show()

# 4.2.2.2 - Magnetic Intensity - Wind Speed
plt.title("Magnetic Intensity - Wind Speed")
plt.scatter(magn_filtered_resultant, avg_wind_speed)
plt.xlabel("Magnetic Intensity/µT")
plt.ylabel("Average Wind Speed/KmHr")
fig = plt.gcf()
fig.set_size_inches(16, 9)
plt.savefig("Magnetic Intensity - Wind Speed.png", dpi=500)
plt.show()

# 4.2.2.3 - Magnetic Intensity - UV Index
plt.title("Magnetic Intensity - UV Index")
plt.scatter(magn_filtered_resultant, avg_uv_index)
plt.xlabel("Magnetic Intensity/µT")
plt.ylabel("Average UV Index")
fig = plt.gcf()
fig.set_size_inches(16, 9)
plt.savefig("Magnetic Intensity - UV Index.png", dpi=500)
plt.show()

# 4.2.2.4 - Magnetic Intensity - Precipitation
plt.title("Magnetic Intensity - Precipitation")
plt.scatter(magn_filtered_resultant, avg_precip)
plt.xlabel("Magnetic Intensity/µT")
plt.ylabel("Average Precipitation/mm")
fig = plt.gcf()
fig.set_size_inches(16, 9)
plt.savefig("Magnetic Intensity - Precipitation.png", dpi=500)
plt.show()

# 4.2.2.5 - Magnetic Intensity - Humidity
plt.title("Magnetic Intensity - Humidity")
plt.scatter(magn_filtered_resultant, avg_humidity)
plt.xlabel("Magnetic Intensity/µT")
plt.ylabel("Average Humidity/%")
fig = plt.gcf()
fig.set_size_inches(16, 9)
plt.savefig("Magnetic Intensity - Humidity.png", dpi=500)
plt.show()

# 4.3 -----------------------IMU Data-----------------------

# 4.3.1 - Unfiltered

# 4.3.1.1 - Magnetic Intensity
plt.title("Magnetic Intensity Unfiltered Readings")
plt.xlabel("Record ID")
plt.ylabel("Magnetic Intensity/µT")
plt.plot(record_id, magnX, label='MagnX')
plt.plot(record_id, magnY, label='MagnY')
plt.plot(record_id, magnZ, label='MagnZ')
plt.xticks(np.arange(min(record_id), max(record_id) + 1, 500))
plt.legend()
fig = plt.gcf()
fig.set_size_inches(16, 9)
plt.savefig("Magnetic Intensity Unfiltered Readings.png", dpi=500)
plt.show()

plt.title("Magnetic Intensity Unfiltered Data")
plt.xlabel("Record ID")
plt.ylabel("Magnetic Intensity/µT")
plt.plot(record_id, magn_resultant, label='Resultant Magnetic Intensity')
plt.plot(
    record_id, [magn_mean] * len(record_id),
    label=f'Mean = {round(magn_mean, 3)}'
)
plt.plot(
    record_id, [magn_sd] * len(record_id),
    label=f'Standard Deviation = {round(magn_sd, 3)}'
)
plt.xticks(np.arange(min(record_id), max(record_id) + 1, 500))
plt.legend()
fig = plt.gcf()
fig.set_size_inches(16, 9)
plt.savefig("Magnetic Intensity Unfiltered Data.png", dpi=500)
plt.show()

# 4.3.1.2 - Acceleration
plt.title("Acceleration Unfiltered Readings")
plt.xlabel("Record ID")
plt.ylabel("Acceleration/g")
plt.plot(record_id, accX, label='AccX')
plt.plot(record_id, accY, label='AccY')
plt.plot(record_id, accZ, label='AccZ')
plt.xticks(np.arange(min(record_id), max(record_id) + 1, 500))
plt.legend()
fig = plt.gcf()
fig.set_size_inches(16, 9)
plt.savefig("Acceleration Unfiltered Readings.png", dpi=500)
plt.show()

plt.title("Acceleration Unfiltered Data")
plt.xlabel("Record ID")
plt.ylabel("Acceleration/g")
plt.plot(record_id, acc_resultant, label='Resultant Acceleration')
plt.plot(
    record_id, [acc_mean] * len(record_id),
    label=f'Mean = {round(acc_mean, 3)}'
)
plt.plot(
    record_id, [acc_sd] * len(record_id),
    label=f'Standard Deviation = {round(acc_sd, 3)}'
)
plt.xticks(np.arange(min(record_id), max(record_id) + 1, 500))
plt.legend()
fig = plt.gcf()
fig.set_size_inches(16, 9)
plt.savefig("Acceleration Unfiltered Data.png", dpi=500)
plt.show()

# 4.3.1.3 - Angular Velocity
plt.title("Angular Velocity Unfiltered Readings")
plt.xlabel("Record ID")
plt.ylabel("Angular Velocity/rad/s")
plt.plot(record_id, gyroX, label='GyroX')
plt.plot(record_id, gyroY, label='GyorY')
plt.plot(record_id, gyroZ, label='GyroZ')
plt.xticks(np.arange(min(record_id), max(record_id) + 1, 500))
plt.legend()
fig = plt.gcf()
fig.set_size_inches(16, 9)
plt.savefig("Angular Velocity Unfiltered Readings.png", dpi=500)
plt.show()

plt.title("Angular Velocity Unfiltered Data")
plt.xlabel("Record ID")
plt.ylabel("Angular Velocity/rad/s")
plt.plot(record_id, gyro_resultant, label='Resultant Angular Velocity')
plt.plot(
    record_id, [gyro_mean] * len(record_id),
    label=f'Mean = {round(gyro_mean, 3)}'
)
plt.plot(
    record_id, [gyro_sd] * len(record_id),
    label=f'Standard Deviation = {round(gyro_sd, 3)}'
)
plt.xticks(np.arange(min(record_id), max(record_id) + 1, 500))
plt.legend()
fig = plt.gcf()
fig.set_size_inches(16, 9)
plt.savefig("Angular Velocity Unfiltered Data.png", dpi=500)
plt.show()

# 4.3.2 - Filtered

# 4.3.2.1 - Magnetic Intensity
plt.title("Magnetic Intensity Filtered Readings")
plt.xlabel("Record ID")
plt.ylabel("Magnetic Intensity/µT")
plt.plot(record_id, magnX_filtered, label='MagnX')
plt.plot(record_id, magnY_filtered, label='MagnY')
plt.plot(record_id, magnZ_filtered, label='MagnZ')
plt.xticks(np.arange(min(record_id), max(record_id) + 1, 500))
plt.legend()
fig = plt.gcf()
fig.set_size_inches(16, 9)
plt.savefig("Magnetic Intensity Filtered Readings.png", dpi=500)
plt.show()

plt.title("Magnetic Intensity Filtered Data")
plt.xlabel("Record ID")
plt.ylabel("Magnetic Intensity/µT")
plt.plot(record_id, magn_filtered_resultant, label='Resultant Magnetic Intensity')
plt.plot(
    record_id, [magn_filtered_mean] * len(record_id),
    label=f'Mean = {round(magn_filtered_mean, 3)}'
)
plt.plot(
    record_id, [magn_filtered_sd] * len(record_id),
    label=f'Standard Deviation = {round(magn_filtered_sd, 3)}'
)
plt.xticks(np.arange(min(record_id), max(record_id) + 1, 500))
plt.legend()
fig = plt.gcf()
fig.set_size_inches(16, 9)
plt.savefig("Magnetic Intensity Filtered Data.png", dpi=500)
plt.show()

# 4.3.2.2 - Acceleration
plt.title("Acceleration Filtered Readings")
plt.xlabel("Record ID")
plt.ylabel("Acceleration/g")
plt.plot(record_id, accX_filtered, label='AccX')
plt.plot(record_id, accY_filtered, label='AccY')
plt.plot(record_id, accZ_filtered, label='AccZ')
plt.xticks(np.arange(min(record_id), max(record_id) + 1, 500))
plt.legend()
fig = plt.gcf()
fig.set_size_inches(16, 9)
plt.savefig("Acceleration Filtered Readings.png", dpi=500)
plt.show()

plt.title("Acceleration Filtered Data")
plt.xlabel("Record ID")
plt.ylabel("Acceleration/g")
plt.plot(record_id, acc_filtered_resultant, label='Resultant Acceleration')
plt.plot(
    record_id, [acc_filtered_mean] * len(record_id),
    label=f'Mean = {round(acc_filtered_mean, 3)}'
)
plt.plot(
    record_id, [acc_filtered_sd] * len(record_id),
    label=f'Standard Deviation = {round(acc_filtered_sd, 3)}'
)
plt.xticks(np.arange(min(record_id), max(record_id) + 1, 500))
plt.legend()
fig = plt.gcf()
fig.set_size_inches(16, 9)
plt.savefig("Acceleration Filtered Data.png", dpi=500)
plt.show()

# 4.3.2.3 - Angular Velocity
plt.title("Angular Velocity Filtered Readings")
plt.xlabel("Record ID")
plt.ylabel("Angular Velocity/rad/s")
plt.plot(record_id, gyroX_filtered, label='GyroX')
plt.plot(record_id, gyroY_filtered, label='GyorY')
plt.plot(record_id, gyroZ_filtered, label='GyroZ')
plt.xticks(np.arange(min(record_id), max(record_id) + 1, 500))
plt.legend()
fig = plt.gcf()
fig.set_size_inches(16, 9)
plt.savefig("Angular Velocity Filtered Readings.png", dpi=500)
plt.show()

plt.title("Angular Velocity Filtered Data")
plt.xlabel("Record ID")
plt.ylabel("Angular Velocity/rad/s")
plt.plot(record_id, gyro_filtered_resultant, label='Resultant Angular Velocity')
plt.plot(
    record_id, [gyro_filtered_mean] * len(record_id),
    label=f'Mean = {round(gyro_filtered_mean, 3)}'
)
plt.plot(
    record_id, [gyro_filtered_sd] * len(record_id),
    label=f'Standard Deviation = {round(gyro_filtered_sd, 3)}'
)
plt.xticks(np.arange(min(record_id), max(record_id) + 1, 500))
plt.legend()
fig = plt.gcf()
fig.set_size_inches(16, 9)
plt.savefig("Angular Velocity Filtered Data.png", dpi=500)
plt.show()

# 4.4 -----------------------IMU Correlations-----------------------

# 4.4.1 - Auto-Correlations

# 4.4.1.1 - Unfiltered
plt.title("Resultant Magnetic Intensity Autocorrelation")
plt.xlabel("Record ID")
plt.ylabel("Correlation Coefficient")
plt.plot(record_id, magn_autocorrelation)
plt.xticks(np.arange(min(record_id), max(record_id) + 1, 500))
fig = plt.gcf()
fig.set_size_inches(16, 9)
plt.savefig("Resultant Magnetic Intensity Autocorrelation.png", dpi=500)
plt.show()

plt.title("Resultant Acceleration Autocorrelation")
plt.xlabel("Record ID")
plt.ylabel("Correlation Coefficient")
plt.plot(record_id, acc_autocorrelation)
plt.xticks(np.arange(min(record_id), max(record_id) + 1, 500))
fig = plt.gcf()
fig.set_size_inches(16, 9)
plt.savefig("Resultant Acceleration Autocorrelation.png", dpi=500)
plt.show()

plt.title("Resultant Angular Velocity Autocorrelation")
plt.xlabel("Record ID")
plt.ylabel("Correlation Coefficient")
plt.plot(record_id, gyro_autocorrelation)
plt.xticks(np.arange(min(record_id), max(record_id) + 1, 500))
fig = plt.gcf()
fig.set_size_inches(16, 9)
plt.savefig("Resultant Angular Velocity Autocorrelation.png", dpi=500)
plt.show()

# 4.4.1.2 - Filtered
plt.title("Resultant Filtered Magnetic Intensity Autocorrelation")
plt.xlabel("Record ID")
plt.ylabel("Correlation Coefficient")
plt.plot(record_id, magn_filtered_autocorrelation)
plt.xticks(np.arange(min(record_id), max(record_id) + 1, 500))
fig = plt.gcf()
fig.set_size_inches(16, 9)
plt.savefig("Resultant Filtered Magnetic Intensity Autocorrelation.png", dpi=500)
plt.show()

plt.title("Resultant Filtered Acceleration Autocorrelation")
plt.xlabel("Record ID")
plt.ylabel("Correlation Coefficient")
plt.plot(record_id, acc_filtered_autocorrelation)
plt.xticks(np.arange(min(record_id), max(record_id) + 1, 500))
fig = plt.gcf()
fig.set_size_inches(16, 9)
plt.savefig("Resultant Filtered Acceleration Autocorrelation.png", dpi=500)
plt.show()

plt.title("Resultant Filtered Angular Velocity Autocorrelation")
plt.xlabel("Record ID")
plt.ylabel("Correlation Coefficient")
plt.plot(record_id, gyro_filtered_autocorrelation)
plt.xticks(np.arange(min(record_id), max(record_id) + 1, 500))
fig = plt.gcf()
fig.set_size_inches(16, 9)
plt.savefig("Resultant Filtered Angular Velocity Autocorrelation.png", dpi=500)
plt.show()

# 4.4.2 - Correlations

# 4.4.2.1 - Unfiltered
plt.title("Resultant Magnetic Intensity - Resultant Acceleration - Correlation")
plt.xlabel("Record ID")
plt.ylabel("Correlation Coefficient")
plt.plot(record_id, magn_acc_cor)
plt.xticks(np.arange(min(record_id), max(record_id) + 1, 500))
fig = plt.gcf()
fig.set_size_inches(16, 9)
plt.savefig("Resultant Magnetic Intensity - Resultant Acceleration - Correlation.png", dpi=500)
plt.show()

plt.title("Resultant Magnetic Intensity - Resultant Angular Velocity - Correlation")
plt.xlabel("Record ID")
plt.ylabel("Correlation Coefficient")
plt.plot(record_id, magn_gyro_cor)
plt.xticks(np.arange(min(record_id), max(record_id) + 1, 500))
fig = plt.gcf()
fig.set_size_inches(16, 9)
plt.savefig("Resultant Magnetic Intensity - Resultant Angular Velocity - Correlation.png", dpi=500)
plt.show()

plt.title("Resultant Acceleration - Resultant Angular Velocity - Correlation")
plt.xlabel("Record ID")
plt.ylabel("Correlation Coefficient")
plt.plot(record_id, acc_gyro_cor)
plt.xticks(np.arange(min(record_id), max(record_id) + 1, 500))
fig = plt.gcf()
fig.set_size_inches(16, 9)
plt.savefig("Resultant Acceleration - Resultant Angular Velocity - Correlation.png", dpi=500)
plt.show()

# 4.4.2.2 - Filtered
plt.title(
    "Filtered Resultant Magnetic Intensity - Filtered Resultant Acceleration - Correlation"
)
plt.xlabel("Record ID")
plt.ylabel("Correlation Coefficient")
plt.plot(record_id, magn_acc_filtered_cor)
plt.xticks(np.arange(min(record_id), max(record_id) + 1, 500))
fig = plt.gcf()
fig.set_size_inches(16, 9)
plt.savefig(
    "Filtered Resultant Magnetic Intensity - Filtered Resultant Acceleration - Correlation.png",
    dpi=500
)
plt.show()

plt.title(
    "Filtered Resultant Magnetic Intensity - Filtered Resultant Angular Velocity - Correlation"
)
plt.xlabel("Record ID")
plt.ylabel("Correlation Coefficient")
plt.plot(record_id, magn_gyro_filtered_cor)
plt.xticks(np.arange(min(record_id), max(record_id) + 1, 500))
fig = plt.gcf()
fig.set_size_inches(16, 9)
plt.savefig(
    "Filtered Resultant Magnetic Intensity - Filtered Resultant Angular Velocity - Correlation.png",
    dpi=500
)
plt.show()

plt.title(
    "Filtered Resultant Acceleration - Filtered Resultant Angular Velocity - Correlation"
)
plt.xlabel("Record ID")
plt.ylabel("Correlation Coefficient")
plt.plot(record_id, acc_gyro_filtered_cor)
plt.xticks(np.arange(min(record_id), max(record_id) + 1, 500))
fig = plt.gcf()
fig.set_size_inches(16, 9)
plt.savefig(
    "Filtered Resultant Acceleration - Filtered Resultant Angular Velocity - Correlation.png",
    dpi=500
)
plt.show()
