import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
from imu import Imu
from noise_filtering import noise_filtering



accX = pd.read_csv('data.csv', usecols=["AccX"], header=0)
accY = pd.read_csv('data.csv', usecols=["AccY"], header=0)
accZ = pd.read_csv('data.csv', usecols=["AccZ"], header=0)

gyroX = pd.read_csv('data.csv', usecols=["GyroX"], header=0)
gyroY = pd.read_csv('data.csv', usecols=["GyroY"], header=0)
gyroZ = pd.read_csv('data.csv', usecols=["GyroZ"], header=0)

elevation = pd.read_csv('data.csv', usecols=["Altitude"], header=0).to_numpy()
recordID = pd.read_csv('data.csv', usecols=["RecordID"], header=0).to_numpy()

acc_resultant = Imu().get_resultant(accX, accY, accZ)
gyro_resultant = Imu().get_resultant(gyroX, gyroY, gyroZ)

acc_filtered_matrix = noise_filtering(accX, accY, accZ, sensitivity=(0.000244*9.81), frequency=10, rms=(3.2*10**-3))
gyro_filtered_matrix = noise_filtering(gyroX,gyroY,gyroZ,sensitivity=(0.0175),frequency=476,rms=(3.2*10**-3))

acc_filtered_resultant = Imu().get_resultant(acc_filtered_matrix[:,0],acc_filtered_matrix[:,1],acc_filtered_matrix[:,2])

gyroX_filtered = gyro_filtered_matrix[:,0]
gyroY_filtered = gyro_filtered_matrix[:,1]
gyroZ_filtered = gyro_filtered_matrix[:,2]

gyroX_sd = Imu().get_sd(gyroX_filtered)
gyroY_sd = Imu().get_sd(gyroY_filtered)
gyroZ_sd = Imu().get_sd(gyroZ_filtered)
gyro_sd_mean = Imu().get_mean_3(gyroX_sd, gyroY_sd, gyroZ_sd)

gyroX_mean = Imu().get_mean(gyroX_filtered)
gyroY_mean = Imu().get_mean(gyroY_filtered)
gyroZ_mean = Imu().get_mean(gyroZ_filtered)
gyro_mean_mean = Imu().get_mean_3(gyroX_mean, gyroY_mean, gyroZ_mean)

acc_sd = Imu().get_sd(acc_filtered_resultant)
acc_mean = Imu().get_mean(acc_filtered_resultant)

#acc_autocorrelation = Imu().autocor(acc_filtered_resultant)
#acc_autocorrelation_pure = Imu().autocor(acc_resultant)

#print(len(acc_filtered_matrix[0][0]))
#print(acc_filtered_matrix[0])
#print(type(acc_filtered_matrix))
#print(len(elevation))

plt.scatter(recordID, acc_resultant, s=1, c=elevation)
plt.colorbar().set_label("Altitude")
plt.title("Absolute Acceleration VS Record ID")
plt.xlabel("Record ID")
plt.ylabel("Acceleration")
plt.show()


plt.scatter(recordID, accX, s=1, c=elevation)
plt.colorbar().set_label("Altitude")
plt.title("X Acceleration VS Record ID")
plt.xlabel("Record ID")
plt.ylabel("Acceleration")
plt.show()


plt.scatter(recordID, accY, s=1, c=elevation)
plt.colorbar().set_label("Altitude")
plt.title("Y Acceleration VS Record ID")
plt.xlabel("Record ID")
plt.ylabel("Acceleration")
plt.show()


plt.scatter(recordID, accZ, s=1, c=elevation)
plt.colorbar().set_label("Altitude")
plt.title("Z Acceleration VS Record ID")
plt.xlabel("Record ID")
plt.ylabel("Acceleration")
plt.show()
